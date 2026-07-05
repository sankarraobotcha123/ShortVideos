from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any, Mapping, Sequence

from fastapi import UploadFile

from app.core.config import settings

ALLOWED_IMAGE_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/jpg",
    "image/webp",
    "image/gif",
}
ALLOWED_IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def safe_slug(value: str, fallback: str = "asset") -> str:
    value = (value or fallback).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80] or fallback


def normalize_tags(value: str | Sequence[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        parts = re.split(r"[,#\n]", value)
    else:
        parts = list(value)
    tags: list[str] = []
    seen: set[str] = set()
    for part in parts:
        tag = re.sub(r"\s+", " ", str(part or "")).strip().lower()
        if tag and tag not in seen:
            tags.append(tag)
            seen.add(tag)
    return tags


def tags_to_text(tags: Sequence[str]) -> str:
    return ", ".join(normalize_tags(tags))


def validate_asset_upload(upload: UploadFile) -> str:
    filename = upload.filename or "asset"
    suffix = Path(filename).suffix.lower()
    content_type = (upload.content_type or "").lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS and content_type not in ALLOWED_IMAGE_MIME_TYPES:
        allowed = ", ".join(sorted(ALLOWED_IMAGE_EXTENSIONS))
        raise ValueError(f"Only image assets are supported for now: {allowed}")
    return suffix if suffix in ALLOWED_IMAGE_EXTENSIONS else ".png"


def save_uploaded_asset(upload: UploadFile, title: str, tags: str) -> dict[str, Any]:
    suffix = validate_asset_upload(upload)
    tag_slug = safe_slug(normalize_tags(tags)[0] if normalize_tags(tags) else title, "asset")
    title_slug = safe_slug(title or Path(upload.filename or "asset").stem, "asset")
    target_dir = settings.asset_library_dir / tag_slug
    target_dir.mkdir(parents=True, exist_ok=True)

    # Keep names deterministic enough to read, but avoid overwriting existing files.
    base_name = f"{title_slug}{suffix}"
    target = target_dir / base_name
    counter = 2
    while target.exists():
        target = target_dir / f"{title_slug}-{counter}{suffix}"
        counter += 1

    with target.open("wb") as file_obj:
        shutil.copyfileobj(upload.file, file_obj)

    return {
        "file_path": str(target),
        "file_name": target.name,
        "mime_type": upload.content_type or "application/octet-stream",
    }


def _asset_keywords(asset: Mapping[str, Any]) -> set[str]:
    text = " ".join(
        str(asset.get(key) or "")
        for key in ["title", "tags", "description", "notes", "source_type"]
    ).lower()
    words = {word for word in re.findall(r"[a-z0-9]+", text) if len(word) >= 3}
    words.update(normalize_tags(str(asset.get("tags") or "")))
    return words


def _scene_keywords(scene: Mapping[str, Any], package: Mapping[str, Any]) -> set[str]:
    text = " ".join(
        str(value or "")
        for value in [
            package.get("topic"),
            package.get("subject"),
            package.get("source_notes"),
            scene.get("scene_name"),
            scene.get("on_screen_text"),
            scene.get("script_segment"),
            scene.get("visual_direction"),
            scene.get("subtitle_text"),
        ]
    ).lower()
    return {word for word in re.findall(r"[a-z0-9]+", text) if len(word) >= 3}


def rank_assets_for_scene(scene: Mapping[str, Any], package: Mapping[str, Any], assets: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    scene_words = _scene_keywords(scene, package)
    ranked: list[dict[str, Any]] = []
    for asset in assets:
        asset_words = _asset_keywords(asset)
        overlap = scene_words.intersection(asset_words)
        score = len(overlap)
        # Common science-short words get a tiny boost when the topic is visual.
        if str(package.get("subject") or "").lower() in asset_words:
            score += 1
        if score <= 0:
            continue
        item = dict(asset)
        item["match_score"] = score
        item["matched_terms"] = sorted(overlap)[:8]
        ranked.append(item)
    return sorted(ranked, key=lambda item: (-int(item.get("match_score") or 0), -int(item.get("reuse_count") or 0), str(item.get("title") or "")))


def choose_scene_assets(package: Mapping[str, Any], scenes: Sequence[Mapping[str, Any]], assets: Sequence[Mapping[str, Any]]) -> list[dict[str, Any] | None]:
    chosen: list[dict[str, Any] | None] = []
    used_ids: set[int] = set()
    for scene in scenes:
        ranked = rank_assets_for_scene(scene, package, assets)
        selected = None
        for asset in ranked:
            asset_id = int(asset.get("id") or 0)
            if asset_id not in used_ids:
                selected = asset
                used_ids.add(asset_id)
                break
        if selected is None and ranked:
            selected = ranked[0]
        chosen.append(selected)
    return chosen


def asset_public_url(asset_id: int) -> str:
    return f"/assets/{asset_id}/download"
