from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Mapping, Sequence

from app.core.config import settings


def _safe_slug(value: str) -> str:
    value = (value or "content-package").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80] or "content-package"


def export_package(
    row: Mapping,
    audio_assets: Sequence[Mapping] | None = None,
    assembly_plans: Sequence[Mapping] | None = None,
    video_drafts: Sequence[Mapping] | None = None,
    visual_assets: Sequence[Mapping] | None = None,
    thumbnail_guides: Sequence[Mapping] | None = None,
    source_safety_reviews: Sequence[Mapping] | None = None,
    trust_reviews: Sequence[Mapping] | None = None,
    learning_outputs: Sequence[Mapping] | None = None,
) -> Path:
    settings.export_dir.mkdir(parents=True, exist_ok=True)
    package_id = row["id"]
    slug = _safe_slug(row["topic"])
    package_dir = settings.export_dir / f"package-{package_id}-{slug}"
    package_dir.mkdir(parents=True, exist_ok=True)

    titles = json.loads(row["title_options"] or "[]")
    hashtags = json.loads(row["hashtags"] or "[]")
    audio_assets = list(audio_assets or [])
    assembly_plans = list(assembly_plans or [])
    video_drafts = list(video_drafts or [])
    visual_assets = list(visual_assets or [])
    thumbnail_guides = list(thumbnail_guides or [])
    source_safety_reviews = list(source_safety_reviews or [])
    trust_reviews = list(trust_reviews or [])
    learning_outputs = list(learning_outputs or [])

    asset_summary = "No reusable visual assets saved yet. Upload assets in the Visual Assets page to reuse icons/diagrams in MP4 drafts."
    if visual_assets:
        asset_summary = "\n".join(
            f"- {asset.get('title')} | tags: {asset.get('tags', '')} | file: {asset.get('file_name')}"
            for asset in visual_assets[:20]
        )

    audio_summary = "No narration asset generated yet. Use the app's Generate narration button or record manually."
    if audio_assets:
        lines = []
        for asset in audio_assets:
            lines.append(
                f"- {asset.get('file_name')} | {asset.get('status')} | {asset.get('provider_used')} | {asset.get('duration_seconds', 0)} sec"
            )
        audio_summary = "\n".join(lines)

    assembly_summary = "No CapCut/manual assembly plan generated yet. Use the app's Generate assembly plan button."
    latest_assembly = assembly_plans[0] if assembly_plans else None
    if latest_assembly:
        assembly_summary = (
            f"Latest plan: {latest_assembly.get('scene_count', 0)} scenes | "
            f"{latest_assembly.get('estimated_duration_seconds', row.get('duration_seconds', 60))} sec | "
            f"{latest_assembly.get('assembly_mode', 'capcut_manual_plan')}"
        )

    video_summary = "No MP4 draft generated yet. Use the app's Generate video draft button."
    if video_drafts:
        video_lines = []
        for draft in video_drafts:
            video_lines.append(
                f"- {draft.get('file_name')} | {draft.get('status')} | {draft.get('draft_mode')} | {draft.get('duration_seconds', 0)} sec"
            )
        video_summary = "\n".join(video_lines)

    thumbnail_summary = "No thumbnail guide generated yet. Use the app's Generate thumbnail helper button."
    latest_thumbnail = thumbnail_guides[0] if thumbnail_guides else None
    if latest_thumbnail:
        thumbnail_summary = (
            f"Latest guide: {latest_thumbnail.get('file_name')} | "
            f"{latest_thumbnail.get('thumbnail_mode', 'manual_canva_capcut_guide')}"
        )

    source_safety_summary = "No source safety review generated yet. Use the app's Generate source safety review button before publishing."
    latest_source_safety = source_safety_reviews[0] if source_safety_reviews else None
    if latest_source_safety:
        source_safety_summary = (
            f"Latest review: risk={latest_source_safety.get('risk_level')} | "
            f"similarity={latest_source_safety.get('similarity_score')}% | "
            f"status={latest_source_safety.get('status')}"
        )

    trust_review_summary = "No Teacher Trust Score review generated yet. Use the app's Generate trust review button before approving this Short."
    latest_trust_review = trust_reviews[0] if trust_reviews else None
    if latest_trust_review:
        trust_review_summary = (
            f"Latest trust review: score={latest_trust_review.get('overall_trust_score')} | "
            f"decision={latest_trust_review.get('reviewer_decision')} | "
            f"approval_required={'Yes' if latest_trust_review.get('approval_required') else 'No'}"
        )

    learning_output_summary = "No notes/quiz/flashcards/worksheet pack generated yet. Use Generate learning outputs after review."
    latest_learning_output = learning_outputs[0] if learning_outputs else None
    if latest_learning_output:
        learning_output_summary = (
            f"Latest learning output: {latest_learning_output.get('file_name')} | "
            f"{latest_learning_output.get('output_mode', 'notes_quiz_flashcards_worksheet')}"
        )

    markdown = f"""# Content Package: {row['topic']}

## Input

- Board/Source: {row['board_source']}
- Class/Level: {row['class_level']}
- Subject: {row['subject']}
- Audience: {row['audience']}
- Language: {row['language']}
- Duration: {row['duration_seconds']} seconds
- Output Type: {row['output_type']}
- Tone: {row['tone']}

## Hook

{row['hook']}

## Script

{row['script_text']}

## Storyboard

{row['storyboard_markdown']}

## Visual Prompts

{row['visual_prompts_markdown']}

## Reusable Visual Assets

{asset_summary}

## Narration Audio

{audio_summary}

## CapCut / Manual Assembly

{assembly_summary}

## Video Drafts

{video_summary}

## Thumbnail Helper

{thumbnail_summary}

## Source Safety & Originality Review

{source_safety_summary}

## Teacher Trust Score Review

{trust_review_summary}

## Learning Outputs

{learning_output_summary}

## Title Options

{chr(10).join(f'- {title}' for title in titles)}

## Description

{row['description']}

## Hashtags

{' '.join(hashtags)}

## Quiz Question

{row['quiz_question']}

## Review

- Status: {row['review_status']}
- Teacher Trust Score: {row['trust_score']}
- Reviewer Notes: {row['reviewer_notes'] or ''}

## AI Provider

- Provider Used: {row.get('provider_used', 'template')}
- Generation Mode: {row.get('generation_mode', 'deterministic_template')}
- Provider Chain: {row.get('provider_chain', 'template')}
- Provider Notes: {row.get('provider_notes', '')}

## Source Safety

- Source Name: {row['source_name'] or ''}
- Source License Type: {row['source_license_type'] or ''}
- Page/Section: {row['page_or_section_reference'] or ''}
- Copied Text Used: {'Yes' if row['copied_text_used'] else 'No'}
- Transformation Notes: {row['transformation_notes'] or ''}
"""

    (package_dir / "content_package.md").write_text(markdown, encoding="utf-8")
    (package_dir / "subtitles.srt").write_text(row["subtitle_srt"], encoding="utf-8")
    (package_dir / "script.txt").write_text(row["script_text"], encoding="utf-8")
    (package_dir / "storyboard.md").write_text(row["storyboard_markdown"], encoding="utf-8")
    (package_dir / "visual_prompts.md").write_text(row["visual_prompts_markdown"], encoding="utf-8")

    visual_asset_manifest = []
    asset_files_dir = package_dir / "visual_assets"
    asset_files_dir.mkdir(exist_ok=True)
    for asset in visual_assets:
        source = Path(asset.get("file_path") or "")
        visual_asset_manifest.append(dict(asset))
        if source.exists() and source.is_file():
            target_name = f"asset_{asset.get('id', 'item')}_{source.name}"
            target = asset_files_dir / target_name
            target.write_bytes(source.read_bytes())
    (package_dir / "visual_assets.json").write_text(json.dumps(visual_asset_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    audio_manifest = []
    for asset in audio_assets:
        source = Path(asset.get("file_path") or "")
        audio_manifest.append(dict(asset))
        if source.exists() and source.is_file():
            target_name = f"audio_{asset.get('id', 'asset')}_{source.name}"
            target = package_dir / target_name
            target.write_bytes(source.read_bytes())

    (package_dir / "audio_assets.json").write_text(json.dumps(audio_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    assembly_manifest = [dict(plan) for plan in assembly_plans]
    if latest_assembly:
        (package_dir / "capcut_assembly_plan.md").write_text(str(latest_assembly.get("plan_markdown") or ""), encoding="utf-8")
        (package_dir / "assembly_plan.json").write_text(str(latest_assembly.get("plan_json") or "{}"), encoding="utf-8")
    (package_dir / "assembly_plans.json").write_text(json.dumps(assembly_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    video_manifest = []
    for draft in video_drafts:
        source = Path(draft.get("file_path") or "")
        video_manifest.append(dict(draft))
        if source.exists() and source.is_file():
            target_name = f"video_draft_{draft.get('id', 'draft')}_{source.name}"
            target = package_dir / target_name
            target.write_bytes(source.read_bytes())
    (package_dir / "video_drafts.json").write_text(json.dumps(video_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    thumbnail_manifest = []
    for guide in thumbnail_guides:
        source = Path(guide.get("file_path") or "")
        thumbnail_manifest.append(dict(guide))
        if source.exists() and source.is_file():
            target_name = f"thumbnail_guide_{guide.get('id', 'guide')}_{source.name}"
            target = package_dir / target_name
            target.write_bytes(source.read_bytes())
    if latest_thumbnail:
        (package_dir / "thumbnail_guide.md").write_text(str(latest_thumbnail.get("layout_guide") or ""), encoding="utf-8")
        (package_dir / "thumbnail_canva_prompt.txt").write_text(str(latest_thumbnail.get("canva_prompt") or ""), encoding="utf-8")
    (package_dir / "thumbnail_guides.json").write_text(json.dumps(thumbnail_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    source_safety_manifest = [dict(review) for review in source_safety_reviews]
    if latest_source_safety:
        (package_dir / "source_safety_review.md").write_text(str(latest_source_safety.get("review_markdown") or ""), encoding="utf-8")
        (package_dir / "source_safety_checklist.json").write_text(str(latest_source_safety.get("checklist_json") or "[]"), encoding="utf-8")
    (package_dir / "source_safety_reviews.json").write_text(json.dumps(source_safety_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    trust_review_manifest = []
    for review in trust_reviews:
        source = Path(review.get("file_path") or "")
        trust_review_manifest.append(dict(review))
        if source.exists() and source.is_file():
            target_name = f"teacher_trust_review_{review.get('id', 'review')}_{source.name}"
            target = package_dir / target_name
            target.write_bytes(source.read_bytes())
    if latest_trust_review:
        latest_path = Path(latest_trust_review.get("file_path") or "")
        if latest_path.exists() and latest_path.is_file():
            (package_dir / "teacher_trust_review.md").write_text(latest_path.read_text(encoding="utf-8"), encoding="utf-8")
        (package_dir / "teacher_trust_checklist.json").write_text(str(latest_trust_review.get("checklist_json") or "[]"), encoding="utf-8")
    (package_dir / "teacher_trust_reviews.json").write_text(json.dumps(trust_review_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    learning_output_manifest = []
    for output in learning_outputs:
        source = Path(output.get("file_path") or "")
        learning_output_manifest.append(dict(output))
        if source.exists() and source.is_file():
            target_name = f"learning_output_{output.get('id', 'output')}_{source.name}"
            target = package_dir / target_name
            target.write_bytes(source.read_bytes())
    if latest_learning_output:
        (package_dir / "revision_notes.md").write_text(str(latest_learning_output.get("revision_notes_markdown") or ""), encoding="utf-8")
        (package_dir / "flashcards.json").write_text(str(latest_learning_output.get("flashcards_json") or "[]"), encoding="utf-8")
        (package_dir / "quiz_questions.json").write_text(str(latest_learning_output.get("quiz_json") or "[]"), encoding="utf-8")
        (package_dir / "worksheet.md").write_text(str(latest_learning_output.get("worksheet_markdown") or ""), encoding="utf-8")
    (package_dir / "learning_outputs.json").write_text(json.dumps(learning_output_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    payload = dict(row)
    payload["audio_assets"] = audio_manifest
    payload["assembly_plans"] = assembly_manifest
    payload["video_drafts"] = video_manifest
    payload["visual_assets"] = visual_asset_manifest
    payload["thumbnail_guides"] = thumbnail_manifest
    payload["source_safety_reviews"] = source_safety_manifest
    payload["teacher_trust_reviews"] = trust_review_manifest
    payload["learning_outputs"] = learning_output_manifest
    (package_dir / "package.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    zip_path = settings.export_dir / f"package-{package_id}-{slug}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in package_dir.rglob("*"):
            if file.is_file():
                zf.write(file, arcname=file.relative_to(package_dir))
    return zip_path
