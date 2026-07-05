from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from app.core.config import settings


def _clamp_score(value: float | int) -> int:
    return max(0, min(100, int(round(float(value)))))


def _word_count(text: str) -> int:
    return len(re.findall(r"\b\w+\b", text or ""))


def _sentence_count(text: str) -> int:
    return max(1, len([item for item in re.split(r"[.!?]+", text or "") if item.strip()]))


def _latest_source_safety(source_safety_reviews: Sequence[Mapping[str, Any]] | None) -> Mapping[str, Any] | None:
    reviews = list(source_safety_reviews or [])
    return reviews[0] if reviews else None


def _score_from_source_safety(source_safety: Mapping[str, Any] | None, package: Mapping[str, Any]) -> tuple[int, list[dict[str, Any]]]:
    checklist: list[dict[str, Any]] = []

    source_name_ok = bool(str(package.get("source_name") or "").strip())
    source_license_ok = bool(str(package.get("source_license_type") or "").strip())
    transformation_ok = bool(str(package.get("transformation_notes") or "").strip())
    copied_text_used = bool(package.get("copied_text_used"))

    checklist.append({"label": "Source name is present", "passed": source_name_ok})
    checklist.append({"label": "Source/license type is present", "passed": source_license_ok})
    checklist.append({"label": "Transformation notes explain the original teaching flow", "passed": transformation_ok})
    checklist.append({"label": "No copied textbook wording is marked as used", "passed": not copied_text_used})

    score = 100
    if not source_name_ok:
        score -= 15
    if not source_license_ok:
        score -= 15
    if not transformation_ok:
        score -= 15
    if copied_text_used:
        score -= 30

    if source_safety:
        similarity = float(source_safety.get("similarity_score") or 0)
        risk = str(source_safety.get("risk_level") or "medium")
        checklist.append({"label": f"Source safety risk is {risk}", "passed": risk == "low"})
        checklist.append({"label": f"Similarity score is {similarity}%", "passed": similarity < 55})
        if risk == "high":
            score -= 30
        elif risk == "medium":
            score -= 12
        if similarity >= 70:
            score -= 25
        elif similarity >= 55:
            score -= 15
        elif similarity >= 40:
            score -= 6
    else:
        checklist.append({"label": "Source safety review has been generated", "passed": False})
        score -= 12

    return _clamp_score(score), checklist


def _score_factual_accuracy(package: Mapping[str, Any], source_safety: Mapping[str, Any] | None) -> tuple[int, list[dict[str, Any]]]:
    checklist: list[dict[str, Any]] = []
    source_notes_words = _word_count(str(package.get("source_notes") or ""))
    script_words = _word_count(str(package.get("script_text") or ""))
    has_source_notes = source_notes_words >= 8
    has_script = script_words >= 30
    has_quiz = bool(str(package.get("quiz_question") or "").strip())
    source_risk_ok = not source_safety or str(source_safety.get("risk_level") or "") != "high"

    checklist.extend([
        {"label": "Source notes contain usable facts", "passed": has_source_notes},
        {"label": "Script has enough explanation to review", "passed": has_script},
        {"label": "Quiz question exists for learning check", "passed": has_quiz},
        {"label": "Latest source safety review is not high risk", "passed": source_risk_ok},
    ])

    score = 90
    if not has_source_notes:
        score -= 25
    if not has_script:
        score -= 20
    if not has_quiz:
        score -= 8
    if not source_risk_ok:
        score -= 20
    return _clamp_score(score), checklist


def _score_age_appropriateness(package: Mapping[str, Any]) -> tuple[int, list[dict[str, Any]]]:
    script = str(package.get("script_text") or "")
    sentences = _sentence_count(script)
    words = _word_count(script)
    avg_sentence_len = words / sentences if sentences else words
    long_sentence_ok = avg_sentence_len <= 18
    duration = int(package.get("duration_seconds") or 60)
    duration_ok = 20 <= duration <= 90
    simple_language_ok = not re.search(r"\b(therefore|henceforth|notwithstanding|aforementioned|photosynthetic apparatus)\b", script, re.I)

    checklist = [
        {"label": f"Average sentence length is about {avg_sentence_len:.1f} words", "passed": long_sentence_ok},
        {"label": f"Duration is {duration} seconds", "passed": duration_ok},
        {"label": "Language avoids unnecessarily complex wording", "passed": simple_language_ok},
    ]

    score = 92
    if not long_sentence_ok:
        score -= min(25, int((avg_sentence_len - 18) * 2))
    if not duration_ok:
        score -= 15
    if not simple_language_ok:
        score -= 10
    return _clamp_score(score), checklist


def _score_simplicity(package: Mapping[str, Any]) -> tuple[int, list[dict[str, Any]]]:
    script = str(package.get("script_text") or "")
    has_example = bool(re.search(r"\b(example|imagine|like|think of|for example)\b", script, re.I))
    has_hook = bool(str(package.get("hook") or "").strip())
    single_learning_point = _word_count(script) <= 180
    checklist = [
        {"label": "Script has a hook", "passed": has_hook},
        {"label": "Script includes an example or analogy", "passed": has_example},
        {"label": "Script stays focused for a Short", "passed": single_learning_point},
    ]
    score = 88
    if not has_hook:
        score -= 12
    if not has_example:
        score -= 14
    if not single_learning_point:
        score -= 12
    return _clamp_score(score), checklist


def _score_visual_clarity(package: Mapping[str, Any]) -> tuple[int, list[dict[str, Any]]]:
    storyboard = str(package.get("storyboard_markdown") or "")
    visuals = str(package.get("visual_prompts_markdown") or "")
    scene_count = len(re.findall(r"\bscene\b", storyboard, re.I)) or len(re.findall(r"^[-*]", storyboard, re.M))
    has_storyboard = scene_count >= 3
    has_visual_prompts = _word_count(visuals) >= 12
    checklist = [
        {"label": f"Storyboard has at least 3 scenes (found {scene_count})", "passed": has_storyboard},
        {"label": "Visual prompts are present", "passed": has_visual_prompts},
    ]
    score = 86
    if not has_storyboard:
        score -= 20
    if not has_visual_prompts:
        score -= 18
    return _clamp_score(score), checklist


def _score_engagement(package: Mapping[str, Any]) -> tuple[int, list[dict[str, Any]]]:
    hook = str(package.get("hook") or "")
    script = str(package.get("script_text") or "")
    has_question_hook = "?" in hook or bool(re.search(r"\bwhy|how|did you|ever wonder\b", hook, re.I))
    has_challenge = bool(re.search(r"\b(challenge|try|comment|next|remember)\b", script, re.I))
    hook_short = _word_count(hook) <= 18
    checklist = [
        {"label": "Hook creates curiosity", "passed": has_question_hook},
        {"label": "Hook is short enough for the first 3 seconds", "passed": hook_short},
        {"label": "Ending gives a challenge or reason to continue", "passed": has_challenge},
    ]
    score = 84
    if not has_question_hook:
        score -= 15
    if not hook_short:
        score -= 8
    if not has_challenge:
        score -= 10
    return _clamp_score(score), checklist


def _recommendation(overall: int) -> tuple[str, bool]:
    if overall >= 85:
        return "Safe for normal human review. Check final visuals/subtitles before publishing.", False
    if overall >= 70:
        return "Needs careful human review. Fix weak checklist items before publishing.", True
    return "Rewrite or regenerate before publishing. This package is not ready for Shorts.", True


def _write_markdown(package_id: int, payload: Mapping[str, Any]) -> tuple[str, str]:
    settings.trust_review_dir.mkdir(parents=True, exist_ok=True)
    file_name = f"package-{package_id}-teacher-trust-review.md"
    path = settings.trust_review_dir / file_name
    checklist = json.loads(str(payload.get("checklist_json") or "[]"))
    checklist_lines = "\n".join(
        f"- [{'x' if item.get('passed') else ' '}] {item.get('label')}" for item in checklist
    )
    markdown = f"""# Teacher Trust Score Review

## Overall

- Overall Trust Score: {payload['overall_trust_score']}
- Recommendation: {payload['recommendation']}
- Approval Required: {'Yes' if payload['approval_required'] else 'No'}

## Score Breakdown

| Area | Score |
|---|---:|
| Factual accuracy | {payload['factual_accuracy_score']} |
| Age appropriateness | {payload['age_appropriateness_score']} |
| Simplicity | {payload['simplicity_score']} |
| Visual clarity | {payload['visual_clarity_score']} |
| Engagement | {payload['engagement_score']} |
| Source safety | {payload['source_safety_score']} |
| Reviewer confidence | {payload['reviewer_confidence_score']} |

## Checklist

{checklist_lines}

## Reviewer Notes

{payload.get('reviewer_notes') or ''}
"""
    path.write_text(markdown, encoding="utf-8")
    return str(path), file_name


def build_trust_review(package: Mapping[str, Any], source_safety_reviews: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    source_safety = _latest_source_safety(source_safety_reviews)
    factual_score, factual_checks = _score_factual_accuracy(package, source_safety)
    age_score, age_checks = _score_age_appropriateness(package)
    simplicity_score, simplicity_checks = _score_simplicity(package)
    visual_score, visual_checks = _score_visual_clarity(package)
    engagement_score, engagement_checks = _score_engagement(package)
    source_score, source_checks = _score_from_source_safety(source_safety, package)
    reviewer_confidence_score = 80

    scores = [
        factual_score * 0.25,
        age_score * 0.15,
        simplicity_score * 0.15,
        visual_score * 0.12,
        engagement_score * 0.13,
        source_score * 0.15,
        reviewer_confidence_score * 0.05,
    ]
    overall = _clamp_score(sum(scores))
    recommendation, approval_required = _recommendation(overall)
    checklist = factual_checks + age_checks + simplicity_checks + visual_checks + engagement_checks + source_checks

    payload = {
        "status": "generated",
        "factual_accuracy_score": factual_score,
        "age_appropriateness_score": age_score,
        "simplicity_score": simplicity_score,
        "visual_clarity_score": visual_score,
        "engagement_score": engagement_score,
        "source_safety_score": source_score,
        "reviewer_confidence_score": reviewer_confidence_score,
        "overall_trust_score": overall,
        "approval_required": int(approval_required),
        "recommendation": recommendation,
        "checklist_json": json.dumps(checklist, ensure_ascii=False),
        "reviewer_notes": "",
        "reviewer_decision": "pending",
        "mime_type": "text/markdown",
    }
    file_path, file_name = _write_markdown(int(package["id"]), payload)
    payload["file_path"] = file_path
    payload["file_name"] = file_name
    return payload


def rebuild_trust_review_from_manual_scores(
    package_id: int,
    factual_accuracy_score: int,
    age_appropriateness_score: int,
    simplicity_score: int,
    visual_clarity_score: int,
    engagement_score: int,
    source_safety_score: int,
    reviewer_confidence_score: int,
    reviewer_notes: str,
    reviewer_decision: str,
    checklist_json: str = "[]",
) -> dict[str, Any]:
    factual_accuracy_score = _clamp_score(factual_accuracy_score)
    age_appropriateness_score = _clamp_score(age_appropriateness_score)
    simplicity_score = _clamp_score(simplicity_score)
    visual_clarity_score = _clamp_score(visual_clarity_score)
    engagement_score = _clamp_score(engagement_score)
    source_safety_score = _clamp_score(source_safety_score)
    reviewer_confidence_score = _clamp_score(reviewer_confidence_score)
    overall = _clamp_score(
        factual_accuracy_score * 0.25
        + age_appropriateness_score * 0.15
        + simplicity_score * 0.15
        + visual_clarity_score * 0.12
        + engagement_score * 0.13
        + source_safety_score * 0.15
        + reviewer_confidence_score * 0.05
    )
    recommendation, approval_required = _recommendation(overall)
    payload = {
        "status": "reviewed" if reviewer_decision != "pending" else "generated",
        "factual_accuracy_score": factual_accuracy_score,
        "age_appropriateness_score": age_appropriateness_score,
        "simplicity_score": simplicity_score,
        "visual_clarity_score": visual_clarity_score,
        "engagement_score": engagement_score,
        "source_safety_score": source_safety_score,
        "reviewer_confidence_score": reviewer_confidence_score,
        "overall_trust_score": overall,
        "approval_required": int(approval_required),
        "recommendation": recommendation,
        "checklist_json": checklist_json or "[]",
        "reviewer_notes": reviewer_notes,
        "reviewer_decision": reviewer_decision,
        "mime_type": "text/markdown",
    }
    file_path, file_name = _write_markdown(package_id, payload)
    payload["file_path"] = file_path
    payload["file_name"] = file_name
    return payload
