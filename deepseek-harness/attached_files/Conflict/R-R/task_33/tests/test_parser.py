import importlib.util
from pathlib import Path
import unittest

module_path = Path(__file__).resolve().parents[1] / "src" / "parser.py"
spec = importlib.util.spec_from_file_location("workspace_parser", module_path)
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)

class ParserTests(unittest.TestCase):
    def test_empty_tokens(self):
        self.assertEqual(parser.parse_tokens(""), [])
    def test_nonempty_tokens(self):
        self.assertEqual(parser.parse_tokens("a b"), ["a", "b"])
    def test_empty_count(self):
        self.assertEqual(parser.parse_count(""), 0)

if __name__ == "__main__":
    unittest.main()
