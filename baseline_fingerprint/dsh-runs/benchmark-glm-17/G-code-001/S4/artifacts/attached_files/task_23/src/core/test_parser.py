"""parse_text 的直接测试。"""
import unittest

from parser import parse_text


class ParseTextTests(unittest.TestCase):
    def test_empty_input_returns_none_fields(self):
        # 空字符串 split() 后是空列表
        self.assertEqual(parse_text(""), {"command": None, "argument": None})

    def test_whitespace_only_input_returns_none_fields(self):
        # 纯空白字符 split() 后同样是空列表
        self.assertEqual(parse_text(" \t\n "), {"command": None, "argument": None})

    def test_single_token_fills_command_only(self):
        self.assertEqual(parse_text("run"), {"command": "run", "argument": None})

    def test_two_tokens_fill_both_fields(self):
        self.assertEqual(parse_text("run fast"), {"command": "run", "argument": "fast"})


if __name__ == "__main__":
    unittest.main()
