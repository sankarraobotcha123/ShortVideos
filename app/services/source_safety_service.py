from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Mapping

from app.core.config import settings


def _clean_text(value: str | None) -> str:
    value = value or ""
    value = re.sub(r"\s+", " ", value.strip())
    return value


def _tokenize(value: str | None) -> set[str]:
    words = re.findall(r"[a-zA-Z0-9]+", (value or "").lower())
    stop = {
        "the", "a", "an", "and", "or", "to", "of", "in", "is", "are", "was", "were", "for", "with",
        "this", "that", "it", "as", "by", "on", "from", "be", "can", "will", "so", "if", "you", "your",
    }
    return {word for word in words if len(word) > 2 and word not in stop}


def _sequence_similarity(a: str, b: str) -> float:
    a = _clean_text(a).lower()
    b = _clean_text(b).lower()
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio() * 100


def _token_overlap(a: str, b: str) -> float:
    left = _tokenize(a)
    right = _tokenize(b)
    if not left or not right:
        return 0.0
    intersection = len(left & right)
    base = max(1, min(len(left), len(right)))
    return min(100.0, (intersection / base) * 100)


def _risk_level(similarity_score: float, copied_text_used: bool, source_license_type: str, source_name: str, transformation_notes: str) -> str:
    license_text = (source_license_type or "").lower()
    source_text = (source_name or "").lower()
    transform_text = (transformation_notes or "").strip()

    if copied_text_used:
        return "high"
    if similarity_score >= 70:
        return "high"
    if similarity_score >= 50:
        return "medium"
    if not transform_text:
        return "medium"
    if source_text and not license_text:
        return "medium"
    if "textbook" in source_text and "open" not in license_text and "self" not in license_text:
        return "medium"
    return "low"


def _recommendation(risk_level: str, similarity_score: float, copied_text_used: bool) -> str:
    if risk_level == "high":
        if copied_text_used:
            return "Do not publish yet. Remove copied wording, rewrite with original analogy/examples, and regenerate the safety review."
        return "Careful rewrite needed. Similarity is high, so make the script more original before publishing."
    if risk_level == "medium":
        return "Human review required. Improve transformation notes, verify source license, and make sure the script is not just a rewritten paragraph."
    if similarity_score <= 35:
        return "Low risk for MVP review. Still verify facts and source metadata before publishing."
    return "Looks acceptable for normal review, but keep source metadata and human approval."


def generate_source_safety_review(package: Mapping) -> dict[str, str | int | float]:
    """Create a lightweight source/originality review without external services.

    This is not a legal verdict or plagiarism engine. It is a practical MVP guardrail:
    it warns when source notes and script are too similar, copied text was marked,
    source/license fields are missing, or transformation notes are weak.
    """

    source_notes = _clean_text(str(package.get("source_notes") or ""))
    script_text = _clean_text(str(package.get("script_text") or ""))
    source_name = _clean_text(str(package.get("source_name") or ""))
    source_license_type = _clean_text(str(package.get("source_license_type") or ""))
    page_or_section_reference = _clean_text(str(package.get("page_or_section_reference") or ""))
    transformation_notes = _clean_text(str(package.get("transformation_notes") or ""))
    copied_text_used = bool(package.get("copied_text_used"))

    sequence_score = _sequence_similarity(source_notes, script_text)
    overlap_score = _token_overlap(source_notes, script_text)
    similarity_score = round((sequence_score * 0.55) + (overlap_score * 0.45), 1)
    risk_level = _risk_level(similarity_score, copied_text_used, source_license_type, source_name, transformation_notes)
    recommendation = _recommendation(risk_level, similarity_score, copied_text_used)

    checklist = [
        {
            "key": "source_name_present",
            "label": "Source name is recorded",
            "passed": bool(source_name),
            "fix": "Add source name such as Self-written notes, NCERT chapter, or open educational source.",
        },
        {
            "key": "license_present",
            "label": "Source license/type is recorded",
            "passed": bool(source_license_type),
            "fix": "Add license/type such as Self-written, Open educational resource, Public domain, or Permission required.",
        },
        {
            "key": "not_copied",
            "label": "No direct copied wording used",
            "passed": not copied_text_used,
            "fix": "Rewrite copied wording into original explanation, analogy, and scene flow.",
        },
        {
            "key": "similarity_ok",
            "label": "Similarity score is below 50",
            "passed": similarity_score < 50,
            "fix": "Rework the script so it teaches the idea differently instead of following source wording closely.",
        },
        {
            "key": "transformation_notes_present",
            "label": "Transformation notes explain what changed",
            "passed": len(transformation_notes) >= 20,
            "fix": "Describe how source facts became an original hook, analogy, example, and visual flow.",
        },
        {
            "key": "reference_present_when_needed",
            "label": "Page/section reference is present when using external sources",
            "passed": bool(page_or_section_reference) or "self" in (source_license_type or "").lower() or "self" in (source_name or "").lower(),
            "fix": "Add page number, chapter section, URL section, or note that it is self-written.",
        },
    ]

    status = "needs_rewrite" if risk_level == "high" else "needs_human_review" if risk_level == "medium" else "passed"
    approval_required = risk_level in {"high", "medium"}

    settings.source_safety_dir.mkdir(parents=True, exist_ok=True)
    package_id = package.get("id", "package")
    file_name = f"package-{package_id}-source-safety-review.md"
    file_path = settings.source_safety_dir / file_name

    checklist_markdown = "\n".join(
        f"- [{'x' if item['passed'] else ' '}] {item['label']}" + ("" if item["passed"] else f" — Fix: {item['fix']}")
        for item in checklist
    )

    markdown = f"""# Source Safety & Originality Review

## Package

- Package ID: {package.get('id')}
- Topic: {package.get('topic')}
- Subject: {package.get('subject')}
- Class/Level: {package.get('class_level')}

## Source Metadata

- Source Name: {source_name or 'Not provided'}
- Source License/Type: {source_license_type or 'Not provided'}
- Page/Section Reference: {page_or_section_reference or 'Not provided'}
- Direct Copied Text Used: {'Yes' if copied_text_used else 'No'}
- Transformation Notes: {transformation_notes or 'Not provided'}

## Originality Signals

- Sequence Similarity: {sequence_score:.1f}%
- Keyword Overlap: {overlap_score:.1f}%
- Overall Similarity Score: {similarity_score:.1f}%
- Risk Level: {risk_level.upper()}
- Status: {status}
- Approval Required: {'Yes' if approval_required else 'No'}

## Checklist

{checklist_markdown}

## Recommendation

{recommendation}

## MVP Rule

Never publish content that is only a rewritten textbook paragraph. Convert the source into an original explanation, analogy, example, visual teaching flow, and student challenge.
"""
    file_path.write_text(markdown, encoding="utf-8")

    return {
        "status": status,
        "risk_level": risk_level,
        "similarity_score": similarity_score,
        "sequence_similarity": round(sequence_score, 1),
        "keyword_overlap": round(overlap_score, 1),
        "approval_required": int(approval_required),
        "copied_text_used": int(copied_text_used),
        "checklist_json": json.dumps(checklist, ensure_ascii=False),
        "recommendation": recommendation,
        "review_markdown": markdown,
        "file_path": str(file_path),
        "file_name": file_name,
        "mime_type": "text/markdown",
    }
