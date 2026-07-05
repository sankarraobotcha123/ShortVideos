from __future__ import annotations

import json
import re
import shutil
import subprocess
import textwrap
from pathlib import Path
from typing import Any, Mapping, Sequence

from app.core.config import settings
from app.services.assembly_service import generate_assembly_plan


VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
SAFE_X = 90


def _safe_slug(value: str) -> str:
    value = (value or "video-draft").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:80] or "video-draft"


def _clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _latest_generated_audio(audio_assets: Sequence[Mapping[str, Any]] | None) -> Mapping[str, Any] | None:
    for asset in audio_assets or []:
        path = Path(str(asset.get("file_path") or ""))
        if asset.get("status") == "generated" and path.exists() and path.is_file():
            return asset
    return None


def _load_scenes(package: Mapping[str, Any], audio_assets: Sequence[Mapping[str, Any]], assembly_plans: Sequence[Mapping[str, Any]] | None) -> list[dict[str, Any]]:
    if assembly_plans:
        latest = assembly_plans[0]
        try:
            parsed = json.loads(str(latest.get("plan_json") or "{}"))
            scenes = parsed.get("scenes") or []
            if scenes:
                return [dict(scene) for scene in scenes]
        except Exception:
            pass
    generated = generate_assembly_plan(package, audio_assets)
    parsed = json.loads(generated["plan_json"])
    return [dict(scene) for scene in parsed.get("scenes") or []]


def _font(size: int):
    from PIL import ImageFont

    candidates = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)
    return ImageFont.load_default()


def _wrap_text(draw, text: str, font, max_width: int, max_lines: int = 8) -> list[str]:
    words = _clean(text).split()
    if not words:
        return [""]
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join([*current, word]).strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
        if len(lines) >= max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(" ".join(current))
    if len(lines) == max_lines and len(" ".join(words)) > len(" ".join(lines)):
        lines[-1] = lines[-1].rstrip(" .") + "..."
    return lines


def _draw_wrapped(draw, xy: tuple[int, int], text: str, font, fill, max_width: int, max_lines: int = 8, line_spacing: int = 16) -> int:
    x, y = xy
    lines = _wrap_text(draw, text, font, max_width=max_width, max_lines=max_lines)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y


def _create_scene_card(package: Mapping[str, Any], scene: Mapping[str, Any], index: int, total: int, output_path: Path) -> None:
    from PIL import Image, ImageDraw

    topic = _clean(str(package.get("topic") or "Educational Short"))
    scene_name = _clean(str(scene.get("scene_name") or f"Scene {index}"))
    on_screen_text = _clean(str(scene.get("on_screen_text") or scene.get("subtitle_text") or topic))
    script_segment = _clean(str(scene.get("script_segment") or scene.get("subtitle_text") or ""))
    visual = _clean(str(scene.get("visual_direction") or "Use a simple diagram or icon that matches the explanation."))
    time_label = f"{scene.get('start_time', '00:00')}–{scene.get('end_time', '00:00')}"

    img = Image.new("RGB", (VIDEO_WIDTH, VIDEO_HEIGHT), (17, 24, 39))
    draw = ImageDraw.Draw(img)

    # Soft vertical background blocks. These are plain generated cards, not final branded visuals.
    draw.rectangle((0, 0, VIDEO_WIDTH, 350), fill=(30, 41, 59))
    draw.rectangle((0, 1480, VIDEO_WIDTH, VIDEO_HEIGHT), fill=(15, 23, 42))
    draw.rounded_rectangle((60, 420, VIDEO_WIDTH - 60, 1280), radius=42, fill=(241, 245, 249))
    draw.rounded_rectangle((60, 1320, VIDEO_WIDTH - 60, 1450), radius=28, fill=(30, 64, 175))

    title_font = _font(56)
    hero_font = _font(74)
    body_font = _font(42)
    small_font = _font(32)
    micro_font = _font(28)

    draw.text((SAFE_X, 80), f"Scene {index}/{total} • {scene_name}", font=small_font, fill=(226, 232, 240))
    _draw_wrapped(draw, (SAFE_X, 145), topic, title_font, (255, 255, 255), VIDEO_WIDTH - SAFE_X * 2, max_lines=2, line_spacing=12)
    draw.text((SAFE_X, 300), time_label, font=micro_font, fill=(203, 213, 225))

    draw.text((SAFE_X, 470), "ON-SCREEN TEXT", font=micro_font, fill=(71, 85, 105))
    _draw_wrapped(draw, (SAFE_X, 530), on_screen_text, hero_font, (15, 23, 42), VIDEO_WIDTH - SAFE_X * 2, max_lines=3, line_spacing=18)

    draw.text((SAFE_X, 880), "NARRATION", font=micro_font, fill=(71, 85, 105))
    _draw_wrapped(draw, (SAFE_X, 935), script_segment, body_font, (30, 41, 59), VIDEO_WIDTH - SAFE_X * 2, max_lines=5, line_spacing=14)

    draw.text((SAFE_X, 1355), "VISUAL NOTE", font=micro_font, fill=(219, 234, 254))
    _draw_wrapped(draw, (SAFE_X, 1390), visual, small_font, (255, 255, 255), VIDEO_WIDTH - SAFE_X * 2, max_lines=2, line_spacing=10)

    draw.text((SAFE_X, 1560), "Draft preview only — replace scene cards with final visuals in CapCut later.", font=micro_font, fill=(148, 163, 184))
    draw.text((SAFE_X, 1640), "9:16 vertical • captions safe-area checked • script timing draft", font=micro_font, fill=(148, 163, 184))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)


def _ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        ffmpeg = shutil.which("ffmpeg")
        if ffmpeg:
            return ffmpeg
        raise RuntimeError("FFmpeg is not available. Install imageio-ffmpeg or system FFmpeg.")


def _seconds(scene: Mapping[str, Any], fallback: int) -> float:
    try:
        return max(1.0, float(scene.get("duration_seconds") or fallback))
    except Exception:
        return float(fallback)


def _write_concat_file(scene_images: list[Path], scenes: list[Mapping[str, Any]], concat_path: Path, fallback_duration: int) -> None:
    lines: list[str] = []
    default_scene_duration = max(2, int(fallback_duration / max(1, len(scene_images))))
    for image_path, scene in zip(scene_images, scenes):
        path = image_path.resolve().as_posix().replace("'", "'\\''")
        lines.append(f"file '{path}'")
        lines.append(f"duration {_seconds(scene, default_scene_duration):.2f}")
    # FFmpeg concat needs the final file repeated so the last duration is honored.
    if scene_images:
        last = scene_images[-1].resolve().as_posix().replace("'", "'\\''")
        lines.append(f"file '{last}'")
    concat_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-3000:] or "FFmpeg command failed")


def _manual_video_guide(package: Mapping[str, Any], output_path: Path, error: str) -> None:
    topic = _clean(str(package.get("topic") or "Untitled"))
    script = _clean(str(package.get("script_text") or ""))
    guide = f"""# Manual Video Draft Guide: {topic}

The backend could not generate an MP4 draft automatically.

Reason:

```text
{error}
```

Use this fallback workflow:

1. Open CapCut or Canva.
2. Create a 9:16 vertical project.
3. Paste the script below as narration/captions.
4. Use the CapCut/manual assembly plan from this package.
5. Export as 1080x1920 MP4.

## Script

{script}
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(guide, encoding="utf-8")


def generate_video_draft(
    package: Mapping[str, Any],
    audio_assets: Sequence[Mapping[str, Any]] | None = None,
    assembly_plans: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Generate a simple vertical MP4 draft for review.

    This is not final production video generation. It creates scene cards that
    help you preview pacing and narration before replacing visuals in CapCut.
    If video rendering fails, it creates a manual guide instead of blocking.
    """
    package_id = int(package.get("id") or 0)
    topic = str(package.get("topic") or "content")
    slug = _safe_slug(topic)
    duration = int(package.get("duration_seconds") or 60)
    output_dir = settings.video_draft_dir / f"package-{package_id}-{slug}"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        scenes = _load_scenes(package, list(audio_assets or []), assembly_plans)
        if not scenes:
            raise RuntimeError("No scenes were available to render.")

        image_paths: list[Path] = []
        for index, scene in enumerate(scenes, start=1):
            image_path = output_dir / f"scene-{index:02d}.png"
            _create_scene_card(package, scene, index, len(scenes), image_path)
            image_paths.append(image_path)

        ffmpeg = _ffmpeg_exe()
        concat_path = output_dir / "concat.txt"
        silent_video_path = output_dir / f"package-{package_id}-{slug}-silent-draft.mp4"
        final_video_path = output_dir / f"package-{package_id}-{slug}-draft.mp4"
        _write_concat_file(image_paths, scenes, concat_path, duration)

        _run([
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_path),
            "-vf",
            "fps=24,format=yuv420p",
            "-movflags",
            "+faststart",
            str(silent_video_path),
        ])

        audio = _latest_generated_audio(audio_assets)
        has_audio = False
        provider_notes = "Silent vertical MP4 draft generated from scene cards."
        output_path = silent_video_path
        if audio:
            audio_path = Path(str(audio.get("file_path") or ""))
            try:
                _run([
                    ffmpeg,
                    "-y",
                    "-i",
                    str(silent_video_path),
                    "-i",
                    str(audio_path),
                    "-c:v",
                    "copy",
                    "-c:a",
                    "aac",
                    "-shortest",
                    "-movflags",
                    "+faststart",
                    str(final_video_path),
                ])
                output_path = final_video_path
                has_audio = True
                provider_notes = f"Vertical MP4 draft generated with narration audio: {audio.get('file_name')}"
            except Exception as audio_error:
                provider_notes = f"Silent MP4 draft generated. Audio merge failed: {audio_error}"

        return {
            "status": "generated",
            "file_path": str(output_path),
            "file_name": output_path.name,
            "mime_type": "video/mp4",
            "draft_mode": "scene_card_mp4_with_audio" if has_audio else "scene_card_silent_mp4",
            "duration_seconds": duration,
            "scene_count": len(scenes),
            "has_audio": has_audio,
            "provider_notes": provider_notes,
        }
    except Exception as error:
        guide_path = output_dir / f"package-{package_id}-{slug}-manual-video-guide.md"
        _manual_video_guide(package, guide_path, str(error))
        return {
            "status": "manual_required",
            "file_path": str(guide_path),
            "file_name": guide_path.name,
            "mime_type": "text/markdown",
            "draft_mode": "manual_video_guide",
            "duration_seconds": duration,
            "scene_count": 0,
            "has_audio": False,
            "provider_notes": f"Automatic MP4 generation failed; manual guide created. Reason: {error}",
        }
