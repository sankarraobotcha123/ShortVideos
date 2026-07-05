from __future__ import annotations

import json
import re
from typing import Any, Mapping, Sequence


def _clean(text: str | None) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _sentences(text: str | None) -> list[str]:
    raw = (text or "").replace("\n", " ")
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", raw) if p.strip()]
    if not parts and raw.strip():
        parts = [raw.strip()]
    return parts


def _fmt(seconds: int) -> str:
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02}:{seconds % 60:02}"


def _short_text(text: str, max_words: int = 8) -> str:
    words = re.findall(r"[A-Za-z0-9]+", text or "")
    if not words:
        return "Key idea"
    result = " ".join(words[:max_words])
    return result + ("..." if len(words) > max_words else "")


def _visual_prompt_lines(markdown: str | None) -> list[str]:
    lines = []
    for line in (markdown or "").splitlines():
        cleaned = line.strip().lstrip("-0123456789. ").strip()
        if cleaned and not cleaned.lower().startswith("#"):
            lines.append(cleaned)
    return lines


def _scene_script_segments(script: str) -> list[str]:
    parts = _sentences(script)
    if not parts:
        return ["Add narration script here."] * 5
    while len(parts) < 5:
        parts.append(parts[-1])
    return [
        parts[0],
        parts[1],
        " ".join(parts[2:-2]) or parts[2],
        parts[-2],
        parts[-1],
    ]


def _timeline(duration: int) -> list[tuple[int, int]]:
    total = max(20, min(int(duration or 60), 90))
    cuts = [0, round(total * 0.08), round(total * 0.18), round(total * 0.65), round(total * 0.88), total]
    # Ensure every scene has at least two seconds.
    for i in range(1, len(cuts)):
        if cuts[i] <= cuts[i - 1]:
            cuts[i] = cuts[i - 1] + 2
    cuts[-1] = total
    return [(cuts[i], cuts[i + 1]) for i in range(5)]


def _audio_instruction(audio_assets: Sequence[Mapping[str, Any]] | None) -> str:
    assets = list(audio_assets or [])
    if not assets:
        return "No backend narration asset yet. Use browser voice preview or record the script manually in CapCut."
    latest = assets[0]
    if latest.get("status") == "generated":
        return f"Import audio file: {latest.get('file_name', 'generated narration')} and align scene cuts to voice timing."
    return f"Use manual guide: {latest.get('file_name', 'recording guide')}. Record voice in CapCut, then align cuts to narration."


def generate_assembly_plan(package: Mapping[str, Any], audio_assets: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Build a practical CapCut/manual editing plan for the current package.

    This is intentionally deterministic. It gives a usable editing timeline even when
    automatic video generation is not ready.
    """
    topic = str(package.get("topic") or "Untitled topic")
    duration = int(package.get("duration_seconds") or 60)
    script = str(package.get("script_text") or "")
    visual_prompts = _visual_prompt_lines(str(package.get("visual_prompts_markdown") or ""))
    segments = _scene_script_segments(script)
    times = _timeline(duration)
    audio_instruction = _audio_instruction(audio_assets)

    scene_names = ["Hook", "Setup", "Explanation", "Memory trick / example", "Challenge / next video reason"]
    transitions = ["Fast zoom-in", "Cut on beat", "Simple push transition", "Quick pop/scale transition", "End card fade"]
    visual_defaults = [
        f"Large bold question text about {topic}; show curiosity symbol or student face.",
        f"Show the real object/situation for {topic}; keep the background clean.",
        f"Use arrows/icons to explain the main cause → process → result for {topic}.",
        f"Show one analogy or simple example related to {topic}.",
        f"Show final question/challenge screen for {topic}; leave space for comments prompt.",
    ]

    scenes: list[dict[str, Any]] = []
    for index, (start, end) in enumerate(times, start=1):
        segment = _clean(segments[index - 1])
        visual = visual_prompts[index - 1] if index - 1 < len(visual_prompts) else visual_defaults[index - 1]
        scenes.append(
            {
                "scene_number": index,
                "scene_name": scene_names[index - 1],
                "start_time": _fmt(start),
                "end_time": _fmt(end),
                "duration_seconds": max(1, end - start),
                "script_segment": segment,
                "subtitle_text": segment,
                "on_screen_text": _short_text(segment, 7),
                "visual_direction": visual,
                "transition": transitions[index - 1],
                "audio_instruction": audio_instruction if index == 1 else "Continue same narration track; cut visuals to match this script segment.",
                "capcut_note": (
                    "Use 9:16 canvas, large readable text, safe margins, and no long intro. "
                    "Keep text under 7 words where possible."
                ),
            }
        )

    markdown_lines = [
        f"# CapCut / Manual Assembly Plan: {topic}",
        "",
        "## Project setup",
        "",
        "- Canvas: 9:16 vertical video",
        f"- Target duration: {duration} seconds",
        "- Recommended resolution: 1080x1920",
        "- Editing style: fast, clear, student-friendly, no long intro",
        f"- Audio: {audio_instruction}",
        "- Subtitle rule: large readable captions, 1–2 lines maximum",
        "",
        "## Scene timeline",
    ]

    for scene in scenes:
        markdown_lines.extend(
            [
                "",
                f"### Scene {scene['scene_number']} — {scene['scene_name']} ({scene['start_time']}–{scene['end_time']})",
                f"- Duration: {scene['duration_seconds']} sec",
                f"- Narration/script: {scene['script_segment']}",
                f"- Subtitle: {scene['subtitle_text']}",
                f"- On-screen text: {scene['on_screen_text']}",
                f"- Visual: {scene['visual_direction']}",
                f"- Transition: {scene['transition']}",
                f"- Audio instruction: {scene['audio_instruction']}",
                f"- CapCut note: {scene['capcut_note']}",
            ]
        )

    markdown_lines.extend(
        [
            "",
            "## Export checklist",
            "",
            "- [ ] First 3 seconds create curiosity",
            "- [ ] Captions are readable on mobile",
            "- [ ] Visuals match the explanation",
            "- [ ] No copied textbook screenshot/text is used without permission",
            "- [ ] Final challenge gives viewers a reason to comment or watch next video",
            "- [ ] Export as 1080x1920 MP4",
        ]
    )

    plan_json = {
        "topic": topic,
        "target_duration_seconds": duration,
        "canvas": "9:16 vertical",
        "recommended_resolution": "1080x1920",
        "audio_instruction": audio_instruction,
        "scenes": scenes,
    }

    return {
        "plan_markdown": "\n".join(markdown_lines).strip() + "\n",
        "plan_json": json.dumps(plan_json, indent=2, ensure_ascii=False),
        "scene_count": len(scenes),
        "estimated_duration_seconds": duration,
        "assembly_mode": "capcut_manual_plan",
        "provider_notes": "Deterministic manual assembly plan generated from script, visual prompts, duration, and narration status.",
    }
