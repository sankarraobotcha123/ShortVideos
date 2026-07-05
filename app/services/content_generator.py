from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import List


HOOK_TEMPLATES = {
    "curious": "Did you ever wonder why {topic_lower}?",
    "simple": "Here is the easiest way to understand {topic_lower}.",
    "exam-focused": "If you understand this, {topic_lower} becomes easy in exams.",
    "story-based": "Imagine this: {topic_lower} is happening right in front of you.",
    "mistake correction": "Most students misunderstand {topic_lower}. Let us fix it in one minute.",
}


@dataclass
class ContentInput:
    board_source: str
    class_level: str
    subject: str
    topic: str
    audience: str
    language: str
    duration_seconds: int
    output_type: str
    tone: str
    source_notes: str = ""
    source_name: str = ""
    source_license_type: str = ""
    page_or_section_reference: str = ""
    copied_text_used: bool = False
    transformation_notes: str = ""


def _clean_sentence(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _split_facts(source_notes: str) -> List[str]:
    notes = _clean_sentence(source_notes)
    if not notes:
        return []
    parts = re.split(r"(?<=[.!?])\s+|;", notes)
    facts = [_clean_sentence(p).rstrip(".") for p in parts if _clean_sentence(p)]
    return facts[:5]


def _hook(topic: str, tone: str) -> str:
    key = (tone or "curious").strip().lower()
    template = HOOK_TEMPLATES.get(key, HOOK_TEMPLATES["curious"])
    return template.format(topic=topic, topic_lower=topic[:1].lower() + topic[1:])


def _script(inp: ContentInput, facts: List[str], hook: str) -> str:
    topic = inp.topic.strip()
    if facts:
        fact_lines = " ".join(facts[:3])
        explanation = (
            f"{fact_lines}. In simple words, this means {topic.lower()} is not just a line from the textbook; "
            f"it is an idea we can see in real life."
        )
    else:
        explanation = (
            f"To explain {topic.lower()}, start with one clear fact from your source notes. "
            f"Then connect it to a simple real-life example so students can remember it easily."
        )

    analogy = (
        "Think of it like a small story: one cause creates one visible result, and that result helps us remember the concept."
    )
    challenge = f"Now your challenge: explain {topic.lower()} in one sentence without using difficult words."

    script = f"""{hook}

{explanation}

{analogy}

So the main point is: understand the reason, not just the definition.

{challenge}"""
    # Keep it short for Shorts; roughly 130-150 words max.
    words = script.split()
    max_words = max(80, min(150, int(inp.duration_seconds * 2.3)))
    if len(words) > max_words:
        script = " ".join(words[:max_words]).rstrip(" ,.;") + "."
    return script


def _storyboard(script: str, topic: str) -> str:
    scenes = [
        ("0–3 sec", "Hook", f"Large bold text: '{topic}'. Fast zoom-in. Show a question mark or curious student."),
        ("3–10 sec", "Setup", "Show the real-life object or situation related to the concept."),
        ("10–35 sec", "Explanation", "Use simple icons/arrows to show cause → process → result."),
        ("35–50 sec", "Memory trick", "Show one analogy or example with minimal text."),
        ("50–60 sec", "Challenge", "End with one question and a reason to watch the next video."),
    ]
    lines = ["# Storyboard"]
    for i, (time_range, title, visual) in enumerate(scenes, start=1):
        lines.append(f"\n## Scene {i}: {title}")
        lines.append(f"- Time: {time_range}")
        lines.append(f"- Visual: {visual}")
        lines.append("- On-screen text: Keep it under 7 words.")
    return "\n".join(lines)


def _visual_prompts(topic: str) -> str:
    prompts = [
        f"Educational vertical 9:16 illustration for school students about {topic}, clean background, simple icons, high clarity, no clutter.",
        f"Animated explainer scene showing cause and effect for {topic}, arrows, labels, child-friendly style.",
        f"Minimal science classroom diagram about {topic}, readable labels, bright but not distracting.",
        f"Final challenge screen for {topic}, bold question text, friendly educational design, vertical short format.",
    ]
    return "# Visual Prompts\n\n" + "\n".join(f"{i}. {p}" for i, p in enumerate(prompts, start=1))


def _titles(topic: str, tone: str) -> list[str]:
    return [
        f"Why {topic}? Explained in 60 Seconds",
        f"The Simple Reason Behind {topic}",
        f"Most Students Miss This: {topic}",
        f"Understand {topic} With One Easy Example",
        f"{topic}: Quick School Science Short",
    ]


def _description(topic: str, subject: str, class_level: str) -> str:
    return (
        f"Learn {topic} in a simple, visual way. This Short is made for {class_level} learners studying {subject}. "
        "Save it for quick revision and try the challenge at the end."
    )


def _hashtags(subject: str, topic: str, class_level: str) -> list[str]:
    cleaned_topic = re.sub(r"[^A-Za-z0-9]+", "", topic.title())[:30] or "Learning"
    cleaned_subject = re.sub(r"[^A-Za-z0-9]+", "", subject.title())[:20] or "Education"
    cleaned_class = re.sub(r"[^A-Za-z0-9]+", "", class_level.title())[:20] or "Students"
    return ["#Shorts", "#Education", f"#{cleaned_subject}", f"#{cleaned_topic}", f"#{cleaned_class}"]


def _quiz(topic: str, facts: List[str]) -> str:
    if facts:
        return f"Quiz: Which key fact helps explain {topic}? Answer using one sentence."
    return f"Quiz: What is the simplest explanation of {topic}?"


def build_srt(script: str, duration_seconds: int) -> str:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", script.replace("\n", " ")) if s.strip()]
    if not sentences:
        sentences = [script.strip() or "Add script text here."]
    total = max(20, min(duration_seconds, 90))
    chunk_len = max(3, total // len(sentences))
    entries = []
    current = 0
    for idx, sentence in enumerate(sentences, start=1):
        start = current
        end = min(total, current + chunk_len)
        if idx == len(sentences):
            end = total
        entries.append(f"{idx}\n{_fmt_time(start)} --> {_fmt_time(end)}\n{sentence}\n")
        current = end
        if current >= total:
            break
    return "\n".join(entries).strip() + "\n"


def _fmt_time(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02},000"


def _teacher_trust_score(inp: ContentInput, script: str, facts: List[str]) -> int:
    score = 50
    if facts:
        score += 20
    if inp.source_name:
        score += 8
    if inp.source_license_type:
        score += 5
    if inp.transformation_notes:
        score += 5
    if not inp.copied_text_used:
        score += 5
    word_count = len(script.split())
    if 70 <= word_count <= 150:
        score += 7
    return max(0, min(100, score))


def generate_content_package(inp: ContentInput) -> dict:
    facts = _split_facts(inp.source_notes)
    hook = _hook(inp.topic, inp.tone)
    script = _script(inp, facts, hook)
    title_options = _titles(inp.topic, inp.tone)
    hashtags = _hashtags(inp.subject, inp.topic, inp.class_level)
    trust_score = _teacher_trust_score(inp, script, facts)

    return {
        "hook": hook,
        "script_text": script,
        "storyboard_markdown": _storyboard(script, inp.topic),
        "subtitle_srt": build_srt(script, inp.duration_seconds),
        "visual_prompts_markdown": _visual_prompts(inp.topic),
        "title_options": json.dumps(title_options, ensure_ascii=False),
        "description": _description(inp.topic, inp.subject, inp.class_level),
        "hashtags": json.dumps(hashtags, ensure_ascii=False),
        "quiz_question": _quiz(inp.topic, facts),
        "trust_score": trust_score,
        "provider_used": "template",
        "generation_mode": "deterministic_template",
        "provider_chain": "template",
        "provider_notes": "Used built-in template fallback. No external AI dependency required.",
        "provider_attempts": "[]",
    }
