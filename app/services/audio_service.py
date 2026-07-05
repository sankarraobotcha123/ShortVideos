from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping

from app.core.config import settings


def _safe_slug(value: str) -> str:
    value = (value or "narration").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:70] or "narration"


def _estimate_duration_seconds(text: str) -> float:
    # 150 spoken words per minute is a reasonable Shorts narration estimate.
    words = len(re.findall(r"\b\w+\b", text or ""))
    return round(max(words / 2.5, 1.0), 1)


def _clean_script_for_tts(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    # Keep script short enough for the MVP TTS button. Full long-form support can be chunked later.
    return text[:6000]


def audio_provider_status() -> list[dict[str, Any]]:
    chain = set(settings.tts_provider_chain)
    powershell = shutil.which("powershell") or shutil.which("pwsh")
    status = [
        {
            "name": "windows_sapi",
            "available": bool(settings.use_windows_sapi and platform.system().lower() == "windows" and powershell),
            "enabled": settings.use_windows_sapi,
            "in_chain": "windows_sapi" in chain,
            "message": (
                "Windows offline speech is ready." if settings.use_windows_sapi and platform.system().lower() == "windows" and powershell
                else "Works only on Windows with PowerShell/System.Speech available."
            ),
        },
        {
            "name": "pyttsx3",
            "available": _pyttsx3_importable() if settings.use_pyttsx3 else False,
            "enabled": settings.use_pyttsx3,
            "in_chain": "pyttsx3" in chain,
            "message": "Optional offline Python TTS. Enable USE_PYTTSX3_TTS=true after installing/confirming system voice support.",
        },
        {
            "name": "manual_recording",
            "available": True,
            "enabled": True,
            "in_chain": "manual_recording" in chain or "manual" in chain,
            "message": "Always available. Creates a narration recording guide if speech generation is not ready.",
        },
    ]
    return status


def generate_audio_asset(package: Mapping[str, Any]) -> dict[str, Any]:
    """Try configured TTS providers and always return a usable audio asset record payload.

    Success providers create a .wav file. The manual fallback creates a .txt recording guide,
    so the user can record in phone/CapCut/browser and keep publishing.
    """
    settings.audio_dir.mkdir(parents=True, exist_ok=True)
    text = _clean_script_for_tts(str(package.get("script_text") or ""))
    package_id = int(package["id"])
    slug = _safe_slug(str(package.get("topic") or f"package-{package_id}"))
    attempts: list[dict[str, Any]] = []

    for provider in settings.tts_provider_chain:
        provider = provider.strip().lower()
        if provider in {"manual", "manual_recording"}:
            result = _manual_recording_fallback(package, text, attempts)
            return result
        if provider == "windows_sapi":
            result = _try_windows_sapi(package_id, slug, text, attempts)
            if result:
                return result
        elif provider == "pyttsx3":
            result = _try_pyttsx3(package_id, slug, text, attempts)
            if result:
                return result
        else:
            attempts.append({"provider": provider, "success": False, "message": "Unknown TTS provider skipped."})

    return _manual_recording_fallback(package, text, attempts)


def _try_windows_sapi(package_id: int, slug: str, text: str, attempts: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not settings.use_windows_sapi:
        attempts.append({"provider": "windows_sapi", "success": False, "message": "Disabled by USE_WINDOWS_SAPI_TTS=false."})
        return None
    if platform.system().lower() != "windows":
        attempts.append({"provider": "windows_sapi", "success": False, "message": "Skipped because this is not Windows."})
        return None
    powershell = shutil.which("powershell") or shutil.which("pwsh")
    if not powershell:
        attempts.append({"provider": "windows_sapi", "success": False, "message": "PowerShell was not found."})
        return None

    output_path = settings.audio_dir / f"package-{package_id}-{slug}-narration.wav"
    escaped_text = text.replace("`", "``").replace('"', '`"')
    escaped_path = str(output_path).replace("`", "``").replace('"', '`"')
    script = f'''
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = 0
$synth.SetOutputToWaveFile("{escaped_path}")
$synth.Speak("{escaped_text}")
$synth.Dispose()
'''.strip()
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".ps1", delete=False, encoding="utf-8") as tmp:
            tmp.write(script)
            ps1_path = tmp.name
        completed = subprocess.run(
            [powershell, "-ExecutionPolicy", "Bypass", "-File", ps1_path],
            capture_output=True,
            text=True,
            timeout=120,
        )
        Path(ps1_path).unlink(missing_ok=True)
        if completed.returncode != 0 or not output_path.exists():
            attempts.append({
                "provider": "windows_sapi",
                "success": False,
                "message": (completed.stderr or completed.stdout or "Windows SAPI failed.")[:400],
            })
            return None
        attempts.append({"provider": "windows_sapi", "success": True, "message": "Generated WAV using Windows offline speech."})
        return {
            "provider_used": "windows_sapi",
            "status": "generated",
            "file_path": str(output_path),
            "file_name": output_path.name,
            "mime_type": "audio/wav",
            "voice_id": settings.tts_voice_id,
            "duration_seconds": _estimate_duration_seconds(text),
            "script_snapshot": text,
            "provider_notes": "Generated using Windows built-in speech synthesis.",
            "provider_attempts": json.dumps(attempts, ensure_ascii=False),
        }
    except Exception as exc:
        attempts.append({"provider": "windows_sapi", "success": False, "message": f"Windows SAPI error: {exc}"})
        return None


def _pyttsx3_importable() -> bool:
    try:
        import pyttsx3  # noqa: F401
        return True
    except Exception:
        return False


def _try_pyttsx3(package_id: int, slug: str, text: str, attempts: list[dict[str, Any]]) -> dict[str, Any] | None:
    if not settings.use_pyttsx3:
        attempts.append({"provider": "pyttsx3", "success": False, "message": "Disabled by USE_PYTTSX3_TTS=false."})
        return None
    try:
        import pyttsx3

        output_path = settings.audio_dir / f"package-{package_id}-{slug}-narration.wav"
        engine = pyttsx3.init()
        engine.setProperty("rate", settings.tts_rate)
        engine.save_to_file(text, str(output_path))
        engine.runAndWait()
        if not output_path.exists() or output_path.stat().st_size == 0:
            attempts.append({"provider": "pyttsx3", "success": False, "message": "pyttsx3 did not create a usable file."})
            return None
        attempts.append({"provider": "pyttsx3", "success": True, "message": "Generated WAV using pyttsx3."})
        return {
            "provider_used": "pyttsx3",
            "status": "generated",
            "file_path": str(output_path),
            "file_name": output_path.name,
            "mime_type": "audio/wav",
            "voice_id": settings.tts_voice_id,
            "duration_seconds": _estimate_duration_seconds(text),
            "script_snapshot": text,
            "provider_notes": "Generated using optional pyttsx3 offline TTS.",
            "provider_attempts": json.dumps(attempts, ensure_ascii=False),
        }
    except Exception as exc:
        attempts.append({"provider": "pyttsx3", "success": False, "message": f"pyttsx3 error: {exc}"})
        return None


def _manual_recording_fallback(package: Mapping[str, Any], text: str, attempts: list[dict[str, Any]]) -> dict[str, Any]:
    package_id = int(package["id"])
    slug = _safe_slug(str(package.get("topic") or f"package-{package_id}"))
    guide_path = settings.audio_dir / f"package-{package_id}-{slug}-recording-guide.txt"
    duration = _estimate_duration_seconds(text)
    attempts.append({"provider": "manual_recording", "success": True, "message": "Created manual recording guide fallback."})

    guide = f"""Narration Recording Guide
==========================

Topic: {package.get('topic', '')}
Target duration: {package.get('duration_seconds', '')} seconds
Estimated spoken duration: {duration} seconds
Language: {package.get('language', 'English')}
Tone: {package.get('tone', 'Curious')}

How to use this fallback:
1. Read the script below using your phone, laptop mic, or CapCut voice recorder.
2. Keep the first 3 seconds energetic because Shorts need a strong hook.
3. Export the voice as WAV/MP3 and place it in storage/audio/.
4. Later, replace this guide with generated TTS when Windows SAPI/pyttsx3/Ollama desktop support is ready.

Script
------
{text}
"""
    guide_path.write_text(guide, encoding="utf-8")
    return {
        "provider_used": "manual_recording",
        "status": "manual_required",
        "file_path": str(guide_path),
        "file_name": guide_path.name,
        "mime_type": "text/plain",
        "voice_id": "manual",
        "duration_seconds": duration,
        "script_snapshot": text,
        "provider_notes": "No local speech engine was used. Manual recording guide created so publishing can continue.",
        "provider_attempts": json.dumps(attempts, ensure_ascii=False),
    }
