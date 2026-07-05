from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Mapping

from app.core.config import settings


def _safe_slug(value: str) -> str:
    value = (value or "content-package").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80] or "content-package"


def export_package(row: Mapping) -> Path:
    settings.export_dir.mkdir(parents=True, exist_ok=True)
    package_id = row["id"]
    slug = _safe_slug(row["topic"])
    package_dir = settings.export_dir / f"package-{package_id}-{slug}"
    package_dir.mkdir(parents=True, exist_ok=True)

    titles = json.loads(row["title_options"] or "[]")
    hashtags = json.loads(row["hashtags"] or "[]")

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

    payload = dict(row)
    (package_dir / "package.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    zip_path = settings.export_dir / f"package-{package_id}-{slug}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in package_dir.iterdir():
            zf.write(file, arcname=file.name)
    return zip_path
