from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Mapping

from app.core.config import settings


def _safe_slug(value: str) -> str:
    value = (value or "thumbnail-guide").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80] or "thumbnail-guide"


def _load_json_list(value: str | None) -> list[str]:
    try:
        parsed = json.loads(value or "[]")
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except Exception:
        pass
    return []


def _shorten(text: str, limit: int = 26) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    words = text.split()
    out: list[str] = []
    for word in words:
        candidate = " ".join(out + [word])
        if len(candidate) > limit:
            break
        out.append(word)
    return " ".join(out) or text[:limit].rstrip()


def _topic_keyword(topic: str) -> str:
    topic = re.sub(r"^(why|what|how|when|where|does|do|is|are)\s+", "", topic.strip(), flags=re.I)
    topic = topic.replace("?", "")
    return _shorten(topic.title(), 22)


def _thumbnail_texts(package: Mapping) -> list[str]:
    topic = str(package.get("topic") or "This Concept")
    keyword = _topic_keyword(topic)
    subject = str(package.get("subject") or "Study")
    tone = str(package.get("tone") or "Curious").lower()

    ideas = [
        f"Why {keyword}?",
        f"{keyword} Explained",
        f"Most Students Miss This",
        f"Easy {subject} Trick",
        f"Understand This Fast",
    ]
    if "exam" in tone:
        ideas.insert(0, f"Exam Trick: {keyword}")
    if "mistake" in tone:
        ideas.insert(0, "Don't Make This Mistake")
    return list(dict.fromkeys([_shorten(item, 30) for item in ideas]))[:6]


def _layout_guide(package: Mapping, text_ideas: list[str]) -> str:
    topic = package.get("topic", "the concept")
    title = text_ideas[0] if text_ideas else _shorten(str(topic), 30)
    return f"""# Thumbnail Layout Guide

## Main thumbnail text

{title}

## Layout

- Format: vertical-friendly 9:16 thumbnail or square crop-safe design.
- Top area: big curiosity text, max 3-5 words.
- Center: one clear diagram/object related to **{topic}**.
- Bottom: small brand tag or subject label.
- Keep background simple. Avoid too many labels.

## Visual direction

- Use one strong object or diagram, not a crowded classroom scene.
- Use arrows/question marks only if they explain the hook.
- Make text readable on a phone screen.
- Do not use copied textbook page screenshots.

## Manual Canva/CapCut steps

1. Create a 1080x1920 or 1080x1080 design.
2. Add main text: `{title}`.
3. Add one visual connected to the concept.
4. Add small subject label: `{package.get('subject', 'Education')}`.
5. Export PNG/JPG and use it for Shorts/playlist branding.
"""


def _canva_prompt(package: Mapping, text_ideas: list[str]) -> str:
    topic = package.get("topic", "educational topic")
    subject = package.get("subject", "education")
    class_level = package.get("class_level", "school students")
    main_text = text_ideas[0] if text_ideas else _shorten(str(topic), 30)
    return (
        f"Create a clean educational YouTube Shorts thumbnail for {class_level} about '{topic}'. "
        f"Use big readable text: '{main_text}'. Show one simple visual object or diagram related to {subject}. "
        "Use a bright clean learning style, high contrast, minimal clutter, phone-readable typography, "
        "no copied textbook pages, no excessive text."
    )


def generate_thumbnail_guide(package: Mapping) -> dict:
    """Create a practical thumbnail guide without requiring image generation."""
    settings.thumbnail_dir.mkdir(parents=True, exist_ok=True)

    package_id = int(package["id"])
    topic = str(package.get("topic") or "content")
    text_ideas = _thumbnail_texts(package)
    title_options = _load_json_list(str(package.get("title_options") or "[]"))
    hashtags = _load_json_list(str(package.get("hashtags") or "[]"))
    layout_guide = _layout_guide(package, text_ideas)
    canva_prompt = _canva_prompt(package, text_ideas)

    guide_markdown = f"""# Thumbnail Helper: {topic}

## Thumbnail text ideas

{chr(10).join(f'- {idea}' for idea in text_ideas)}

## Recommended title connection

{chr(10).join(f'- {title}' for title in title_options[:5]) or '- Use the best title generated in the package.'}

## Canva / CapCut prompt

{canva_prompt}

{layout_guide}

## Hashtag context

{' '.join(hashtags)}

## Quality checklist

- [ ] Can the main text be read in 1 second?
- [ ] Does the image match the Short's first hook?
- [ ] Is there only one main idea?
- [ ] Is the design different enough from previous thumbnails?
- [ ] Does it avoid copied textbook screenshots?
"""

    slug = _safe_slug(topic)
    file_name = f"thumbnail-guide-{package_id}-{slug}.md"
    file_path = settings.thumbnail_dir / file_name
    file_path.write_text(guide_markdown, encoding="utf-8")

    return {
        "status": "generated",
        "file_path": str(file_path),
        "file_name": file_name,
        "mime_type": "text/markdown",
        "thumbnail_mode": "manual_canva_capcut_guide",
        "text_ideas": json.dumps(text_ideas, ensure_ascii=False),
        "layout_guide": layout_guide,
        "canva_prompt": canva_prompt,
        "provider_notes": "Generated a manual thumbnail guide. This does not require image generation or paid tools.",
    }
