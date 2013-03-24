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
        self._test('-1',     [('-1', 'number')])
        self._test('1',      [('1', 'number')])
        self._test('1.0',    [('1.0', 'number')])
        self._test('1.0e10', [('1.0e10', 'number')])
        self._test('1e10.0', [('1e10.0', 'number')])

        self._test('-100 0 1e10 2.02 3.33e33.3', [('-100', 'number'),('0', 'number'),('1e10', 'number'),('2.02', 'number'),('3.33e33.3', 'number')])

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
        with self.assertRaises(SyntaxError):
            parse_arguments('"hello')

        with self.assertRaises(SyntaxError):
            parse_arguments("'hello\\'")

        with self.assertRaises(SyntaxError):
            parse_arguments("1.0.1")

        with self.assertRaises(SyntaxError):
            parse_arguments("1e.0.1")

        with self.assertRaises(SyntaxError):
            parse_arguments("1e1e1")

        with self.assertRaises(SyntaxError):
            parse_arguments("[ 1, 2, 3 ")

        with self.assertRaises(SyntaxError):
            parse_arguments("{ 'key': 'value'")

        with self.assertRaises(SyntaxError):
            parse_arguments("bareword")

if __name__ == '__main__':
    unittest.main()
