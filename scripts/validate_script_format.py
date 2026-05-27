#!/usr/bin/env python3
"""Validate strict Chinese short-drama script markers in a .txt file."""

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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_script_format.py <script.txt>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    text = read_text(path)
    errors = validate(text)
    if errors:
        print("format check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("format check ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
