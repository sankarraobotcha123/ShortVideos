from __future__ import annotations

import json
import re
from typing import Any, Mapping

from app.core.config import settings


def _clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _safe_slug(value: str) -> str:
    value = (value or "learning-output").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80] or "learning-output"


def _sentences(text: str, limit: int = 6) -> list[str]:
    parts = [
        _clean(part).rstrip(".")
        for part in re.split(r"(?<=[.!?])\s+|;", _clean(text))
        if _clean(part)
    ]
    return parts[:limit]


def _load_json_list(value: str | None) -> list[str]:
    try:
        parsed = json.loads(value or "[]")
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except Exception:
        pass
    return []


def _topic_keyword(topic: str) -> str:
    topic = re.sub(r"^(why|what|how|when|where|does|do|is|are)\s+", "", topic.strip(), flags=re.I)
    topic = topic.replace("?", "")
    return _clean(topic.title()) or "This Concept"


def _source_facts(package: Mapping[str, Any]) -> list[str]:
    facts = _sentences(str(package.get("source_notes") or ""), 6)
    if not facts:
        facts = _sentences(str(package.get("script_text") or ""), 6)
    if not facts:
        facts = [f"Understand the main idea behind {package.get('topic', 'this concept')}"]
    return facts


def _revision_notes(package: Mapping[str, Any], facts: list[str]) -> str:
    topic = str(package.get("topic") or "Untitled topic")
    class_level = str(package.get("class_level") or "school level")
    subject = str(package.get("subject") or "subject")
    titles = _load_json_list(str(package.get("title_options") or "[]"))
    key_title = titles[0] if titles else f"{topic} explained simply"

    fact_lines = "\n".join(f"- {fact}." for fact in facts[:5])
    memory_trick = (
        f"Think of **{_topic_keyword(topic)}** as one simple cause-and-effect idea: "
        "first understand the reason, then remember the visible result."
    )
    return f"""# Revision Notes: {topic}

## Best short title

{key_title}

## Class / Subject

- Level: {class_level}
- Subject: {subject}

## Main idea

{_clean(package.get('hook'))}

## Key points

{fact_lines}

## Simple explanation

{_clean(package.get('script_text'))}

## Memory trick

{memory_trick}

## One-line revision

{topic} becomes easy when you connect the reason with one clear real-life example.

## Quick self-check

{package.get('quiz_question') or f'Explain {topic} in one sentence.'}
"""


def _flashcards(package: Mapping[str, Any], facts: list[str]) -> list[dict[str, str]]:
    topic = str(package.get("topic") or "this concept")
    cards: list[dict[str, str]] = [
        {
            "front": f"What is the main idea of {topic}?",
            "back": f"The main idea is to understand the reason behind {topic}, not just memorize the wording.",
        },
        {
            "front": "What should you remember first?",
            "back": facts[0] if facts else f"Start with one clear fact about {topic}.",
        },
    ]
    for idx, fact in enumerate(facts[1:4], start=3):
        cards.append({"front": f"Key fact {idx - 1}", "back": fact})
    cards.append({"front": "How can you revise this fast?", "back": f"Explain {topic} in one simple sentence using your own words."})
    return cards[:6]


def _quiz_questions(package: Mapping[str, Any], facts: list[str]) -> list[dict[str, Any]]:
    topic = str(package.get("topic") or "this concept")
    keyword = _topic_keyword(topic)
    first_fact = facts[0] if facts else f"{keyword} has one clear reason."
    second_fact = facts[1] if len(facts) > 1 else "A real-life example makes the concept easier to remember."
    return [
        {
            "type": "short_answer",
            "question": f"Explain {topic} in one sentence.",
            "answer": f"A good answer should mention: {first_fact}",
        },
        {
            "type": "fill_blank",
            "question": f"The easiest way to understand {keyword} is to connect the reason with a ____ example.",
            "answer": "real-life",
        },
        {
            "type": "true_false",
            "question": f"True or False: Memorizing only the definition is enough to understand {topic}.",
            "answer": "False",
        },
        {
            "type": "short_answer",
            "question": "Write one key fact from this lesson.",
            "answer": second_fact,
        },
        {
            "type": "challenge",
            "question": f"Create your own example or analogy for {topic}.",
            "answer": "Answers may vary. Check whether the example explains the concept clearly and correctly.",
        },
    ]


def _worksheet(package: Mapping[str, Any], facts: list[str]) -> str:
    topic = str(package.get("topic") or "Untitled topic")
    subject = str(package.get("subject") or "Subject")
    class_level = str(package.get("class_level") or "Level")
    quiz = _quiz_questions(package, facts)
    question_lines = "\n".join(f"{idx}. {item['question']}" for idx, item in enumerate(quiz, start=1))
    answer_lines = "\n".join(f"{idx}. {item['answer']}" for idx, item in enumerate(quiz, start=1))
    return f"""# Worksheet: {topic}

## Student details

Name: ____________________    Class: ____________________    Date: ____________________

## Topic

- Subject: {subject}
- Level: {class_level}
- Concept: {topic}

## Part A — Quick Revision

Read the key idea and underline the most important words:

> {_clean(package.get('hook'))}

## Part B — Questions

{question_lines}

## Part C — Draw / Visual Thinking

Draw one simple diagram, arrow flow, or symbol that explains **{topic}**.

## Part D — Answer Key / Teacher Notes

{answer_lines}
"""


def generate_learning_output(package: Mapping[str, Any]) -> dict[str, Any]:
    """Generate reusable notes, flashcards, quiz, and worksheet from a package."""
    settings.learning_output_dir.mkdir(parents=True, exist_ok=True)

    package_id = int(package["id"])
    topic = str(package.get("topic") or "content")
    facts = _source_facts(package)
    revision_notes = _revision_notes(package, facts)
    flashcards = _flashcards(package, facts)
    quiz_questions = _quiz_questions(package, facts)
    worksheet = _worksheet(package, facts)

    flashcards_json = json.dumps(flashcards, ensure_ascii=False, indent=2)
    quiz_json = json.dumps(quiz_questions, ensure_ascii=False, indent=2)

    markdown = f"""# Learning Output Pack: {topic}

This pack is designed for reuse beyond Shorts. Use it for revision notes, flashcards, quiz practice, and a simple worksheet.

---

{revision_notes}

---

# Flashcards

{chr(10).join(f"## Card {idx}{chr(10)}Front: {card['front']}{chr(10)}Back: {card['back']}" for idx, card in enumerate(flashcards, start=1))}

---

# Quiz Questions

{chr(10).join(f"{idx}. [{item['type']}] {item['question']}{chr(10)}   Answer: {item['answer']}" for idx, item in enumerate(quiz_questions, start=1))}

---

{worksheet}
"""

    slug = _safe_slug(topic)
    file_name = f"learning-output-{package_id}-{slug}.md"
    file_path = settings.learning_output_dir / file_name
    file_path.write_text(markdown, encoding="utf-8")

    return {
        "status": "generated",
        "output_mode": "notes_quiz_flashcards_worksheet",
        "revision_notes_markdown": revision_notes,
        "flashcards_json": flashcards_json,
        "quiz_json": quiz_json,
        "worksheet_markdown": worksheet,
        "file_path": str(file_path),
        "file_name": file_name,
        "mime_type": "text/markdown",
        "provider_notes": "Generated from the reviewed package using local deterministic templates. No Ollama or external AI required.",
    }
