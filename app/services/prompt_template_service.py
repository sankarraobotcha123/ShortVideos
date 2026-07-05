from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any, Mapping

from app.services.content_generator import ContentInput, build_srt


DEFAULT_PROMPT_TEMPLATES: list[dict[str, str | int]] = [
    {
        "name": "Curiosity Short Script",
        "task_type": "script",
        "style_key": "curiosity",
        "active": 1,
        "notes": "Best default for attention-first Science curiosity Shorts.",
        "template_text": """{hook}\n\nHere is the simple idea: {top_fact}.\n\nMost students only remember the word, but the real meaning is this: {simple_meaning}.\n\nImagine it like this: {analogy}.\n\nSo remember: {memory_line}.\n\nChallenge: explain {topic_lower} in one sentence without difficult words.""",
    },
    {
        "name": "Mistake Correction Script",
        "task_type": "script",
        "style_key": "mistake_correction",
        "active": 1,
        "notes": "Use when the Short corrects a common student misunderstanding.",
        "template_text": """Most students get {topic_lower} wrong because they memorize it without understanding it.\n\nThe mistake is thinking it is only a definition. Actually, {top_fact}.\n\nIn simple words: {simple_meaning}.\n\nThink of it like this: {analogy}.\n\nSo the correct idea is: {memory_line}.\n\nComment one example where you see this in real life.""",
    },
    {
        "name": "Exam-Focused Script",
        "task_type": "script",
        "style_key": "exam_focused",
        "active": 1,
        "notes": "Use for Shorts that should convert into revision playlists and notes.",
        "template_text": """If you understand {topic_lower}, this chapter becomes easier in exams.\n\nPoint one: {top_fact}.\n\nPoint two: {simple_meaning}.\n\nEasy memory trick: {memory_line}.\n\nExample: {analogy}.\n\nQuick quiz: why is {topic_lower} important? Answer in one sentence.""",
    },
    {
        "name": "Story / Analogy Script",
        "task_type": "script",
        "style_key": "story_analogy",
        "active": 1,
        "notes": "Use when the concept is abstract and needs a visual story.",
        "template_text": """Imagine you are watching {topic_lower} happen like a small story.\n\nFirst, {top_fact}.\n\nThen, {simple_meaning}.\n\nNow picture this: {analogy}.\n\nThat picture helps you remember one thing: {memory_line}.\n\nSave this Short and try explaining the story to a friend.""",
    },
    {
        "name": "Quick Revision Script",
        "task_type": "script",
        "style_key": "quick_revision",
        "active": 1,
        "notes": "Use for fast revision Shorts after you already have attention topics.",
        "template_text": """Quick revision: {topic}.\n\nMain fact: {top_fact}.\n\nMeaning: {simple_meaning}.\n\nMemory line: {memory_line}.\n\nExample: {analogy}.\n\nNow test yourself: can you explain this in 10 seconds?""",
    },
]


@dataclass
class PromptTemplateRenderResult:
    script_text: str
    hook: str
    prompt_template_id: int | None
    prompt_template_name: str
    prompt_template_style: str
    prompt_template_snapshot: str


def seed_default_prompt_templates(conn) -> int:
    """Create default prompt templates only when the table is empty."""
    row = conn.execute("SELECT COUNT(*) AS total FROM prompt_templates").fetchone()
    total = int(dict(row or {}).get("total") or 0)
    if total > 0:
        return 0
    created = 0
    for item in DEFAULT_PROMPT_TEMPLATES:
        conn.execute(
            """
            INSERT INTO prompt_templates (name, task_type, style_key, template_text, active, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item["name"],
                item["task_type"],
                item["style_key"],
                item["template_text"],
                int(item["active"]),
                item["notes"],
            ),
        )
        created += 1
    return created


def list_prompt_templates(conn, task_type: str | None = None) -> list[dict[str, Any]]:
    seed_default_prompt_templates(conn)
    if task_type:
        rows = conn.execute(
            "SELECT * FROM prompt_templates WHERE task_type = ? ORDER BY active DESC, id DESC",
            (task_type,),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM prompt_templates ORDER BY task_type, active DESC, id DESC").fetchall()
    return [dict(row) for row in rows]


def get_prompt_template(conn, template_id: int) -> dict[str, Any] | None:
    seed_default_prompt_templates(conn)
    row = conn.execute("SELECT * FROM prompt_templates WHERE id = ?", (template_id,)).fetchone()
    return dict(row) if row is not None else None


def apply_script_prompt_template(
    inp: ContentInput,
    base_package: Mapping[str, Any],
    template: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Apply a selected script template without breaking provider fallback.

    This does not call external AI. It gives the creator repeatable prompt styles
    and lets future LLM providers use the same DB-backed template snapshot.
    """
    if not template:
        return dict(base_package)

    template_text = str(template.get("template_text") or "").strip()
    if not template_text:
        return dict(base_package)

    context = _build_context(inp, base_package)
    script_text = _safe_format(template_text, context)
    script_text = _limit_words(script_text, inp.duration_seconds)
    hook = _first_nonempty_line(script_text) or str(base_package.get("hook") or "")

    updated = dict(base_package)
    updated["script_text"] = script_text
    updated["hook"] = hook
    updated["subtitle_srt"] = build_srt(script_text, inp.duration_seconds)
    updated["prompt_template_id"] = int(template.get("id") or 0) or None
    updated["prompt_template_name"] = str(template.get("name") or "")
    updated["prompt_template_style"] = str(template.get("style_key") or "")
    updated["prompt_template_snapshot"] = template_text

    provider_notes = str(updated.get("provider_notes") or "")
    updated["provider_notes"] = (provider_notes + "\n" if provider_notes else "") + (
        f"Applied prompt template: {updated['prompt_template_name']} ({updated['prompt_template_style']})."
    )
    return updated


def build_prompt_preview(inp: ContentInput, base_package: Mapping[str, Any], template: Mapping[str, Any]) -> dict[str, Any]:
    context = _build_context(inp, base_package)
    return {
        "template_id": template.get("id"),
        "template_name": template.get("name"),
        "task_type": template.get("task_type"),
        "style_key": template.get("style_key"),
        "rendered_text": _safe_format(str(template.get("template_text") or ""), context),
        "available_placeholders": sorted(context.keys()),
    }


def _build_context(inp: ContentInput, base_package: Mapping[str, Any]) -> dict[str, str]:
    facts = _split_facts(inp.source_notes)
    top_fact = facts[0] if facts else f"{inp.topic} can be explained using one clear source fact."
    simple_meaning = _simple_meaning(inp.topic, facts)
    analogy = _analogy(inp.topic, inp.subject)
    memory_line = _memory_line(inp.topic)
    title_options = _json_list(base_package.get("title_options"))
    hashtags = _json_list(base_package.get("hashtags"))
    return {
        "topic": inp.topic.strip(),
        "topic_lower": _lower_first(inp.topic.strip()),
        "subject": inp.subject.strip(),
        "class_level": inp.class_level.strip(),
        "audience": inp.audience.strip(),
        "language": inp.language.strip(),
        "duration_seconds": str(inp.duration_seconds),
        "tone": inp.tone.strip(),
        "source_notes": inp.source_notes.strip(),
        "source_name": inp.source_name.strip(),
        "source_license_type": inp.source_license_type.strip(),
        "hook": str(base_package.get("hook") or f"Did you ever wonder about {inp.topic}?"),
        "top_fact": top_fact,
        "facts_json": json.dumps(facts, ensure_ascii=False),
        "simple_meaning": simple_meaning,
        "analogy": analogy,
        "memory_line": memory_line,
        "title_options": "; ".join(title_options),
        "hashtags": " ".join(hashtags),
    }


def _safe_format(template: str, context: Mapping[str, str]) -> str:
    class SafeDict(dict):
        def __missing__(self, key):
            return "{" + key + "}"

    try:
        return template.format_map(SafeDict(context)).strip()
    except Exception:
        # Keep the raw template usable instead of failing generation.
        return template.strip()


def _split_facts(source_notes: str) -> list[str]:
    text = re.sub(r"\s+", " ", source_notes or "").strip()
    if not text:
        return []
    parts = re.split(r"(?<=[.!?])\s+|;", text)
    return [p.strip().rstrip(".") for p in parts if p.strip()][:5]


def _json_list(value: Any) -> list[str]:
    try:
        parsed = json.loads(value or "[]")
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except Exception:
        pass
    return []


def _lower_first(value: str) -> str:
    return value[:1].lower() + value[1:] if value else value


def _simple_meaning(topic: str, facts: list[str]) -> str:
    if len(facts) >= 2:
        return facts[1]
    return f"{topic.lower()} becomes easy when we connect the reason, the process, and the result."


def _analogy(topic: str, subject: str) -> str:
    subject_lower = (subject or "").lower()
    if "science" in subject_lower:
        return "a tiny cause-and-effect machine where one small part creates a visible result"
    if "math" in subject_lower:
        return "a shortcut path: once you know the rule, every similar problem becomes easier"
    if "english" in subject_lower or "grammar" in subject_lower:
        return "a sentence puzzle where each word has a job"
    return f"a small story that makes {topic.lower()} easier to remember"


def _memory_line(topic: str) -> str:
    return f"do not memorize {topic.lower()}; understand why it happens."


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        cleaned = line.strip(" #*-\t")
        if cleaned:
            return cleaned
    return ""


def _limit_words(script: str, duration_seconds: int) -> str:
    words = script.split()
    max_words = max(80, min(155, int(duration_seconds * 2.35)))
    if len(words) <= max_words:
        return script
    return " ".join(words[:max_words]).rstrip(" ,.;") + "."
