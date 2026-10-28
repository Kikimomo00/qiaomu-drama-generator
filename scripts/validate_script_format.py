#!/usr/bin/env python3
"""Validate strict Chinese short-drama script markers in a .txt file.

Default mode checks format markers only. Pass --structure to also check
episode sequence, scene numbering, and per-episode dialogue. Structure mode
does not judge story expectation, information gaps, or cliffhanger quality.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


EPISODE_RE = re.compile(r"^第\s*\d+\s*集$")
SCENE_RE = re.compile(r"^(\d+)-(\d+)\s+.+\s+(日内|日外|夜内|夜外|昏内|昏外)(【字幕：.+】)?$")
CHARACTER_RE = re.compile(r"^人物：.+")
DIALOGUE_RE = re.compile(r"^[^：\s]{1,20}(（[^）]+）)?：.+")
ACTION_RE = re.compile(r"^(△|Δ)\s*.+")


def read_text(path: Path) -> str:
    if path.suffix.lower() != ".txt":
        raise SystemExit("Only .txt validation is supported. Export PDF text to .txt before validating.")
    return path.read_text(encoding="utf-8")


def validate(text: str) -> list[str]:
    errors: list[str] = []
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    if "一、剧本" not in lines:
        errors.append("missing section: 一、剧本")
    if "二、正文剧本" not in lines:
        errors.append("missing section: 二、正文剧本")

    episode_indices = [i for i, line in enumerate(lines) if EPISODE_RE.match(line)]
    if not episode_indices:
        errors.append("missing episode marker: 第 N 集")

    scene_indices = [i for i, line in enumerate(lines) if SCENE_RE.match(line)]
    if not scene_indices:
        errors.append("missing scene marker: N-M 场景名 日内/日外/夜内/夜外/昏内/昏外")

    for scene_i in scene_indices:
        window = lines[scene_i + 1 : scene_i + 5]
        if not any(CHARACTER_RE.match(line) for line in window):
            errors.append(f"scene missing nearby 人物： line: {lines[scene_i]}")

    if not any(DIALOGUE_RE.match(line) for line in lines):
        errors.append("missing dialogue line: 人物名：对白")

    if not any(ACTION_RE.match(line) for line in lines):
        errors.append("missing marked action line: △ / Δ")

    for current_i, line in enumerate(lines):
        scene_match = SCENE_RE.match(line)
        if scene_match:
            episode_no = int(scene_match.group(1))
            previous_episode = next(
                (
                    int(re.search(r"\d+", lines[i]).group(0))
                    for i in range(current_i, -1, -1)
                    if EPISODE_RE.match(lines[i])
                ),
                None,
            )
            if previous_episode is not None and episode_no != previous_episode:
                errors.append(f"scene episode number mismatch: {line}")

    return errors


def _episode_number(line: str) -> int:
    match = re.search(r"\d+", line)
    if match is None:
        raise ValueError(f"episode marker has no number: {line}")
    return int(match.group(0))


def _is_spoken_line(line: str) -> bool:
    return bool(DIALOGUE_RE.match(line)) and not line.startswith("人物：")


def structure_check(text: str) -> tuple[list[str], list[str]]:
    """Optional continuity checks. Empty when the file has no episode markers."""
    errors: list[str] = []
    notes: list[str] = [
        "mechanical checks do not judge 核心期待, 信息差, or 卡点质量; use references/methodology-review.md"
    ]
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    episodes: list[dict[str, int]] = []
    for index, line in enumerate(lines):
        if EPISODE_RE.match(line):
            episodes.append({"no": _episode_number(line), "start": index, "end": len(lines)})

    for index, episode in enumerate(episodes[:-1]):
        episode["end"] = episodes[index + 1]["start"]

    for previous, current in zip(episodes, episodes[1:]):
        if current["no"] != previous["no"] + 1:
            errors.append(
                f"episode number is not sequential: 第 {previous['no']} 集 -> 第 {current['no']} 集"
            )

    for episode in episodes:
        block = lines[episode["start"] + 1 : episode["end"]]
        scene_indexes: list[int] = []
        for line in block:
            scene_match = SCENE_RE.match(line)
            if scene_match:
                scene_indexes.append(int(scene_match.group(2)))
        if not scene_indexes:
            errors.append(f"episode missing scene: 第 {episode['no']} 集")
        else:
            if scene_indexes[0] != 1:
                errors.append(f"scene index does not start at 1: 第 {episode['no']} 集")
            for previous_index, current_index in zip(scene_indexes, scene_indexes[1:]):
                if current_index != previous_index + 1:
                    errors.append(
                        "scene index is not contiguous: "
                        f"第 {episode['no']} 集 {previous_index} -> {current_index}"
                    )
        if not any(_is_spoken_line(line) for line in block):
            errors.append(f"episode missing dialogue: 第 {episode['no']} 集")
        if episode["no"] == 1 and len(block) < 6:
            notes.append("第 1 集正文较短，需人工确认四项任务：停下来、看懂、起情绪、承诺后续")

    return errors, notes


def _print_result(heading: str, errors: list[str]) -> bool:
    if errors:
        print(f"{heading} failed:")
        for error in errors:
            print(f"- {error}")
        return True
    print(f"{heading} ok")
    return False


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    structure = False
    paths: list[str] = []
    for arg in args:
        if arg == "--structure":
            structure = True
        elif arg.startswith("-"):
            print(f"unknown option: {arg}", file=sys.stderr)
            print("usage: validate_script_format.py [--structure] <script.txt>", file=sys.stderr)
            return 2
        else:
            paths.append(arg)

    if len(paths) != 1:
        print("usage: validate_script_format.py [--structure] <script.txt>", file=sys.stderr)
        return 2

    path = Path(paths[0])
    text = read_text(path)
    failed = _print_result("format check", validate(text))
    if structure:
        structure_errors, notes = structure_check(text)
        failed = _print_result("structure check", structure_errors) or failed
        if notes:
            print("structure notes:")
            for note in notes:
                print(f"- {note}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
