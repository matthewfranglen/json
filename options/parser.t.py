from parser import parse_arguments
from rule import Rule
import unittest

class TestParser(unittest.TestCase):
    def _test(self, string, expected):
        tokens = parse_arguments(string)
        self.assertEqual(tokens, expected)

    def test_string(self):
        self._test("'hello'", [Rule("'hello'", Rule.TYPE_STRING)])
        self._test('"hello"', [Rule('"hello"', Rule.TYPE_STRING)])

        for escapes in range(10):
            escape = '\\\\' * escapes

            self._test("'hello%s' \"world%s\"" % (escape, escape),
                    [Rule("'hello%s'" % escape, Rule.TYPE_STRING), Rule('"world%s"' % escape, Rule.TYPE_STRING)])

            self._test("'hello %s\\'world%s\\''" % (escape, escape),
                    [Rule("'hello %s\\'world%s\\''" % (escape, escape), Rule.TYPE_STRING)])

            self._test("'hello %s\\\\'\"world%s\\\\\"" % (escape, escape),
                    [Rule("'hello %s\\\\'" % escape, Rule.TYPE_STRING), Rule('"world%s\\\\"' % escape, Rule.TYPE_STRING)])

    def test_number(self):
        self._test('-1',     [Rule('-1',     Rule.TYPE_NUMBER)])
        self._test('1',      [Rule('1',      Rule.TYPE_NUMBER)])
        self._test('1.0',    [Rule('1.0',    Rule.TYPE_NUMBER)])
        self._test('1.0e10', [Rule('1.0e10', Rule.TYPE_NUMBER)])
        self._test('1e10.0', [Rule('1e10.0', Rule.TYPE_NUMBER)])

        self._test('-100 0 1e10 2.02 3.33e33.3',
                    [ Rule('-100',      Rule.TYPE_NUMBER),
                      Rule('0',         Rule.TYPE_NUMBER),
                      Rule('1e10',      Rule.TYPE_NUMBER),
                      Rule('2.02',      Rule.TYPE_NUMBER),
                      Rule('3.33e33.3', Rule.TYPE_NUMBER)])

    def test_token(self):
        self._test('[1, 2, 3]',                              [Rule([1, 2, 3],                              Rule.TYPE_TOKEN)])
        self._test('{ "key": "value" }',                     [Rule({ "key": "value" },                     Rule.TYPE_TOKEN)])
        self._test('{ "key": [1, 2, 3] }',                   [Rule({ "key": [1, 2, 3] },                   Rule.TYPE_TOKEN)])
        self._test('{ "key": [1, 2, { "key": "value" } ] }', [Rule({ "key": [1, 2, { "key": "value" } ] }, Rule.TYPE_TOKEN)])

        self._test('[1, 2, 3] { "key": "value" } [ 4, 5, 6 ]',
                    [ Rule([1, 2, 3],          Rule.TYPE_TOKEN),
                      Rule({ "key": "value" }, Rule.TYPE_TOKEN),
                      Rule([ 4, 5, 6 ],        Rule.TYPE_TOKEN)])

    def test_operator(self):
        self._test('==', [Rule('==', Rule.TYPE_OPERATOR)])
        self._test('=',  [Rule('=',  Rule.TYPE_OPERATOR)])
        self._test('>',  [Rule('>',  Rule.TYPE_OPERATOR)])
        self._test('<',  [Rule('<',  Rule.TYPE_OPERATOR)])
        self._test('~',  [Rule('~',  Rule.TYPE_OPERATOR)])
        self._test('!',  [Rule('!',  Rule.TYPE_OPERATOR)])
        self._test(':',  [Rule(':',  Rule.TYPE_OPERATOR)])

        self._test('>>>',
                    [ Rule('>', Rule.TYPE_OPERATOR),
                      Rule('>', Rule.TYPE_OPERATOR),
                      Rule('>', Rule.TYPE_OPERATOR)])

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
