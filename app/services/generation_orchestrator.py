from __future__ import annotations

import json
import textwrap
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from app.core.config import settings
from app.services.content_generator import ContentInput, generate_content_package as generate_template_package


@dataclass
class ProviderAttempt:
    provider: str
    available: bool
    success: bool
    message: str
    duration_ms: int = 0


class GenerationProviderError(RuntimeError):
    pass


class BaseGenerationProvider:
    name = "base"

    def is_available(self) -> tuple[bool, str]:
        return False, "Base provider is not usable directly."

    def generate(self, inp: ContentInput, base_package: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class TemplateProvider(BaseGenerationProvider):
    name = "template"

    def is_available(self) -> tuple[bool, str]:
        return True, "Always available. Uses deterministic templates and source notes."

    def generate(self, inp: ContentInput, base_package: dict[str, Any]) -> dict[str, Any]:
        package = dict(base_package)
        package["provider_used"] = self.name
        package["generation_mode"] = "deterministic_template"
        package["provider_notes"] = "Used built-in template fallback. No external AI dependency required."
        return package


class OllamaProvider(BaseGenerationProvider):
    name = "ollama"

    def is_available(self) -> tuple[bool, str]:
        if not settings.use_ollama:
            return False, "USE_OLLAMA=false. Enable it after installing and running Ollama."
        try:
            req = urllib.request.Request(f"{settings.ollama_base_url.rstrip('/')}/api/tags", method="GET")
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    return True, f"Ollama reachable at {settings.ollama_base_url}."
                return False, f"Ollama returned HTTP {response.status}."
        except Exception as exc:  # pragma: no cover - depends on local machine
            return False, f"Ollama not reachable: {exc}"

    def generate(self, inp: ContentInput, base_package: dict[str, Any]) -> dict[str, Any]:
        available, message = self.is_available()
        if not available:
            raise GenerationProviderError(message)

        prompt = _build_llm_prompt(inp, base_package)
        payload = {
            "model": settings.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 450,
            },
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{settings.ollama_base_url.rstrip('/')}/api/generate",
            data=data,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=settings.ollama_timeout_seconds) as response:
                raw = response.read().decode("utf-8")
                body = json.loads(raw)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:  # pragma: no cover
            raise GenerationProviderError(f"Ollama generation failed: {exc}") from exc

        script_text = _clean_ai_script(body.get("response", ""))
        if len(script_text.split()) < 45:
            raise GenerationProviderError("Ollama returned too little script content.")

        package = dict(base_package)
        package["script_text"] = script_text
        package["subtitle_srt"] = _regenerate_srt(script_text, inp.duration_seconds)
        package["provider_used"] = self.name
        package["generation_mode"] = "local_llm_ollama"
        package["provider_notes"] = f"Generated script with Ollama model {settings.ollama_model}; template fallback generated metadata."
        return package


class TransformersProvider(BaseGenerationProvider):
    name = "transformers"

    def is_available(self) -> tuple[bool, str]:
        if not settings.use_transformers:
            return False, "USE_TRANSFORMERS=false. Enable only after installing transformers/torch locally."
        try:
            import transformers  # noqa: F401
            return True, f"Transformers import OK. Model configured: {settings.transformers_model}."
        except Exception as exc:  # pragma: no cover - optional dependency
            return False, f"Transformers not available: {exc}"

    def generate(self, inp: ContentInput, base_package: dict[str, Any]) -> dict[str, Any]:
        available, message = self.is_available()
        if not available:
            raise GenerationProviderError(message)
        try:
            from transformers import pipeline  # type: ignore
        except Exception as exc:  # pragma: no cover
            raise GenerationProviderError(f"Could not import transformers pipeline: {exc}") from exc

        prompt = _build_short_transformers_prompt(inp)
        try:
            generator = pipeline("text-generation", model=settings.transformers_model)
            outputs = generator(
                prompt,
                max_new_tokens=settings.transformers_max_new_tokens,
                do_sample=True,
                temperature=0.8,
                num_return_sequences=1,
            )
        except Exception as exc:  # pragma: no cover
            raise GenerationProviderError(f"Transformers generation failed: {exc}") from exc

        raw = outputs[0].get("generated_text", "") if outputs else ""
        script_text = _clean_ai_script(raw.replace(prompt, ""))
        if len(script_text.split()) < 45:
            raise GenerationProviderError("Transformers returned too little usable script content.")

        package = dict(base_package)
        package["script_text"] = script_text
        package["subtitle_srt"] = _regenerate_srt(script_text, inp.duration_seconds)
        package["provider_used"] = self.name
        package["generation_mode"] = "local_transformers"
        package["provider_notes"] = f"Generated script with Transformers model {settings.transformers_model}; template fallback generated metadata."
        return package


PROVIDERS: dict[str, BaseGenerationProvider] = {
    "ollama": OllamaProvider(),
    "transformers": TransformersProvider(),
    "template": TemplateProvider(),
}


def provider_status() -> list[dict[str, str | bool]]:
    statuses = []
    for name in ["ollama", "transformers", "template"]:
        provider = PROVIDERS[name]
        available, message = provider.is_available()
        statuses.append(
            {
                "name": name,
                "available": available,
                "message": message,
                "in_chain": name in settings.ai_provider_chain,
            }
        )
    return statuses


def generate_content_package_with_fallbacks(inp: ContentInput) -> dict[str, Any]:
    """Generate a package using configured providers with safe fallback.

    The deterministic template is always used first as the base package. AI
    providers only replace/improve parts of the package, so failed AI calls do
    not block publishing.
    """

    generation_started = time.perf_counter()
    base_package = generate_template_package(inp)
    attempts: list[ProviderAttempt] = []

    chain = settings.ai_provider_chain or ["template"]
    if "template" not in chain:
        chain = [*chain, "template"]

    for provider_name in chain:
        provider = PROVIDERS.get(provider_name)
        if provider is None:
            attempts.append(ProviderAttempt(provider_name, False, False, "Unknown provider name.", 0))
            continue

        attempt_started = time.perf_counter()
        available, message = provider.is_available()
        availability_duration_ms = int((time.perf_counter() - attempt_started) * 1000)
        if not available:
            attempts.append(ProviderAttempt(provider_name, False, False, message, availability_duration_ms))
            continue

        try:
            package = provider.generate(inp, base_package)
            attempt_duration_ms = int((time.perf_counter() - attempt_started) * 1000)
            attempts.append(ProviderAttempt(provider_name, True, True, "Generation succeeded.", attempt_duration_ms))
            package["provider_chain"] = ",".join(chain)
            package["generation_duration_ms"] = int((time.perf_counter() - generation_started) * 1000)
            package["provider_attempts"] = json.dumps([a.__dict__ for a in attempts], ensure_ascii=False)
            return package
        except GenerationProviderError as exc:
            attempt_duration_ms = int((time.perf_counter() - attempt_started) * 1000)
            attempts.append(ProviderAttempt(provider_name, True, False, str(exc), attempt_duration_ms))
        except Exception as exc:  # Keep the fallback chain safe.
            attempt_duration_ms = int((time.perf_counter() - attempt_started) * 1000)
            attempts.append(ProviderAttempt(provider_name, True, False, f"Unexpected provider error: {exc}", attempt_duration_ms))

    # This should rarely be reached because template is always appended.
    fallback = TemplateProvider().generate(inp, base_package)
    attempts.append(ProviderAttempt("template", True, True, "Emergency fallback succeeded.", int((time.perf_counter() - generation_started) * 1000)))
    fallback["provider_chain"] = ",".join(chain)
    fallback["generation_duration_ms"] = int((time.perf_counter() - generation_started) * 1000)
    fallback["provider_attempts"] = json.dumps([a.__dict__ for a in attempts], ensure_ascii=False)
    return fallback


def _build_llm_prompt(inp: ContentInput, base_package: dict[str, Any]) -> str:
    return textwrap.dedent(
        f"""
        You are helping create a high-retention educational YouTube Short.
        Write only the final narration script. Do not include markdown headings.

        Requirements:
        - Topic: {inp.topic}
        - Subject: {inp.subject}
        - Level: {inp.class_level}
        - Audience: {inp.audience}
        - Language: {inp.language}
        - Duration: {inp.duration_seconds} seconds
        - Tone: {inp.tone}
        - Start with a strong 0-3 second hook.
        - Use simple student-friendly words.
        - Include one original analogy or example.
        - End with one challenge/question.
        - Do not copy source wording directly.
        - Keep it under 150 words.

        Source facts to preserve:
        {inp.source_notes or 'No source notes provided. Use safe, general explanation and recommend review.'}

        Template draft to improve:
        {base_package.get('script_text', '')}
        """
    ).strip()


def _build_short_transformers_prompt(inp: ContentInput) -> str:
    return (
        f"Write a simple {inp.duration_seconds}-second educational Shorts script for {inp.class_level} students. "
        f"Topic: {inp.topic}. Facts: {inp.source_notes}. Start with a hook, explain simply, use one example, end with a challenge. Script:"
    )


def _clean_ai_script(text: str) -> str:
    text = text.replace("Narration:", "").replace("Script:", "")
    lines = [line.strip(" -\t") for line in text.splitlines() if line.strip()]
    cleaned = "\n\n".join(lines).strip()
    words = cleaned.split()
    if len(words) > 160:
        cleaned = " ".join(words[:160]).rstrip(" ,.;") + "."
    return cleaned


def _regenerate_srt(script_text: str, duration_seconds: int) -> str:
    # Reuse the public content generator function without exposing internals.
    dummy = ContentInput(
        board_source="Generated",
        class_level="Generated",
        subject="Generated",
        topic="Generated",
        audience="Generated",
        language="English",
        duration_seconds=duration_seconds,
        output_type="Short",
        tone="Curious",
        source_notes=script_text,
    )
    package = generate_template_package(dummy)
    # The template package generated a dummy script, so override by calling the
    # local SRT builder through a small duplicate-free import fallback.
    try:
        from app.services.content_generator import build_srt
        return build_srt(script_text, duration_seconds)
    except Exception:
        return package["subtitle_srt"]
