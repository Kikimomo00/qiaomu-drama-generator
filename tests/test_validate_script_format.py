#!/usr/bin/env python3
"""Backward-compatible checks for scripts/validate_script_format.py."""

from __future__ import annotations

import contextlib
import importlib.util
import tempfile
import unittest
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_script_format.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_script_format", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALID = """测试剧
一、剧本
主角在开场就被抢走证据，观众等着看她当众翻盘。
二、正文剧本
测试剧

第 1 集
1-1 客厅 日内
人物：甲，乙
甲站在桌边。
△ 乙放下杯子。
甲：证据在你那儿。
乙：现在不能给。

第 2 集
2-1 走廊 夜内
人物：甲，乙
△ 甲拦住乙。
甲：明天庭上见。
乙：你带不走证人。
"""

GAP = """测试剧
一、剧本
简介。
二、正文剧本
测试剧

第 1 集
1-1 客厅 日内
人物：甲
△ 甲推开门。
甲：人呢？

第 3 集
3-1 走廊 夜内
人物：乙
△ 乙停下。
乙：晚了。
"""

SHORT_OPENING = """测试剧
一、剧本
简介。
二、正文剧本
测试剧

第 1 集
1-1 客厅 日内
人物：甲
△ 甲回头。
甲：谁？
"""


class ValidateScriptFormatTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_validator()

    def write_txt(self, content: str) -> str:
        handle = tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False)
        handle.write(content)
        handle.close()
        self.addCleanup(lambda: Path(handle.name).unlink(missing_ok=True))
        return handle.name

    def test_default_valid_script_passes(self):
        path = self.write_txt(VALID)
        buffer = StringIO()
        with contextlib.redirect_stdout(buffer):
            code = self.mod.main([path])
        self.assertEqual(code, 0)
        self.assertEqual(buffer.getvalue(), "format check ok\n")
        self.assertEqual(self.mod.validate(VALID), [])

    def test_default_missing_section_fails(self):
        errors = self.mod.validate("第 1 集\n1-1 客厅 日内\n")
        self.assertIn("missing section: 一、剧本", errors)
        self.assertIn("missing section: 二、正文剧本", errors)

    def test_episode_gap_stays_valid_without_structure_flag(self):
        path = self.write_txt(GAP)
        self.assertEqual(self.mod.validate(GAP), [])
        self.assertEqual(self.mod.main([path]), 0)

    def test_structure_flag_reports_gap_and_keeps_format_ok(self):
        path = self.write_txt(GAP)
        buffer = StringIO()
        with contextlib.redirect_stdout(buffer):
            code = self.mod.main(["--structure", path])
        output = buffer.getvalue()
        self.assertEqual(code, 1)
        self.assertIn("format check ok", output)
        self.assertIn("episode number is not sequential: 第 1 集 -> 第 3 集", output)
        self.assertIn("methodology-review.md", output)

    def test_structure_accepts_continuation_that_starts_after_episode_one(self):
        text = VALID.split("第 1 集", 1)[1]
        continuation = "测试剧\n一、剧本\n简介。\n二、正文剧本\n测试剧\n\n第 2 集" + text.split("第 2 集", 1)[1]
        errors, _notes = self.mod.structure_check(continuation)
        self.assertEqual(errors, [])

    def test_structure_flags_noncontiguous_scenes(self):
        text = """测试剧
一、剧本
简介。
二、正文剧本
测试剧

第 2 集
2-1 客厅 日内
人物：甲
△ 甲坐下。
甲：开始。
2-3 门口 日外
人物：甲，乙
△ 乙进来。
乙：停。
"""
        errors, _notes = self.mod.structure_check(text)
        self.assertIn("scene index is not contiguous: 第 2 集 1 -> 3", errors)

    def test_structure_flags_scene_index_and_missing_dialogue(self):
        text = """测试剧
一、剧本
简介。
二、正文剧本
测试剧

第 5 集
5-2 客厅 日内
人物：甲，乙
△ 甲坐下。
"""
        errors, _notes = self.mod.structure_check(text)
        self.assertIn("scene index does not start at 1: 第 5 集", errors)
        self.assertIn("episode missing dialogue: 第 5 集", errors)

    def test_short_episode_one_is_a_note_not_an_error(self):
        errors, notes = self.mod.structure_check(SHORT_OPENING)
        self.assertEqual(errors, [])
        self.assertTrue(any("四项任务" in note for note in notes))

    def test_unknown_option_and_missing_path(self):
        self.assertEqual(self.mod.main(["--json", "x.txt"]), 2)
        self.assertEqual(self.mod.main([]), 2)

    def test_non_txt_still_rejected(self):
        with self.assertRaises(SystemExit):
            self.mod.read_text(Path("draft.pdf"))


if __name__ == "__main__":
    unittest.main()
