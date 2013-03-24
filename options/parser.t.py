from parser import parse_arguments
import unittest

class TestParser(unittest.TestCase):
    def _test(self, string, expected):
        tokens = parse_arguments(string)
        self.assertEqual(tokens, expected)

    def test_string(self):
        self._test("'hello'",               [("'hello'", 'string')])
        self._test('"hello"',               [('"hello"', 'string')])
        self._test("'hello' \"world\"",     [("'hello'", 'string'), ('"world"', 'string')])
        self._test("'hello \\\'world\\\''", [("'hello \\\'world\\\''", 'string')])

    def test_number(self):
        pass

    def test_token(self):
        self._test("[1, 2, 3]",                                [("[1, 2, 3]", 'token')])
        self._test("{ 'key': 'value' }",                       [("{ 'key': 'value' }", 'token')])
        self._test("{ 'key': [1, 2, 3] }",                     [("{ 'key': [1, 2, 3] }", 'token')])
        self._test("{ 'key': [1, 2, { 'key': 'value' } ] }",   [("{ 'key': [1, 2, { 'key': 'value' } ] }", 'token')])
        self._test("[1, 2, 3] { 'key': 'value' } [ 4, 5, 6 ]", [("[1, 2, 3]", 'token'),("{ 'key': 'value' }", 'token'),("[ 4, 5, 6 ]", 'token')])

    def test_operator(self):
        self._test('==', [('==', 'operator')])
        self._test('=',  [('=', 'operator')])
        self._test('>',  [('>', 'operator')])
        self._test('<',  [('<', 'operator')])
        self._test('~',  [('~', 'operator')])
        self._test('!',  [('!', 'operator')])
        self._test(':',  [(':', 'operator')])

        self._test('>>>', [('>', 'operator'),('>', 'operator'),('>', 'operator')])

    def test_invalid(self):
        pass

if __name__ == '__main__':
    unittest.main()
