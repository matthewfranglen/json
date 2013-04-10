from visitor import visit
from rule import Rule
import unittest

class TestParser(unittest.TestCase):
    def _test(self, rules, nodes, expected):
        results = visit(rules, nodes)
        self.assertEqual(results, expected)

    def test_index(self):
        # :Tab / \S\S*/l0
        self._test([Rule('0',Rule.TYPE_TOKEN)],           [1,2,3],          [1])
        self._test([Rule('5',Rule.TYPE_TOKEN)],           [1,2,3],          [])
        self._test([Rule('key',Rule.TYPE_TOKEN)],         {'key': 'value'}, ['value'])
        self._test([Rule('another_key',Rule.TYPE_TOKEN)], {'key': 'value'}, [])

        self._test([Rule('0',Rule.TYPE_TOKEN),Rule('0',Rule.TYPE_TOKEN)],     [[1,2],2,3],               [1])
        self._test([Rule('1',Rule.TYPE_TOKEN),Rule('0',Rule.TYPE_TOKEN)],     [[1,2],2,3],               [])
        self._test([Rule('0',Rule.TYPE_TOKEN),Rule('2',Rule.TYPE_TOKEN)],     [[1,2],2,3],               [])

        self._test([Rule('0',Rule.TYPE_TOKEN),Rule('key',Rule.TYPE_TOKEN)],   [{'key': 'value'},2,3],    ['value'])
        self._test([Rule('4',Rule.TYPE_TOKEN),Rule('key',Rule.TYPE_TOKEN)],   [{'key': 'value'},2,3],    [])
        self._test([Rule('0',Rule.TYPE_TOKEN),Rule('ttt',Rule.TYPE_TOKEN)],   [{'key': 'value'},2,3],    [])

        self._test([Rule('key',Rule.TYPE_TOKEN),Rule('0',Rule.TYPE_TOKEN)],   {'key': [1,2]},            [1])
        self._test([Rule('ttt',Rule.TYPE_TOKEN),Rule('0',Rule.TYPE_TOKEN)],   {'key': [1,2]},            [])
        self._test([Rule('key',Rule.TYPE_TOKEN),Rule('2',Rule.TYPE_TOKEN)],   {'key': [1,2]},            [])

        self._test([Rule('key',Rule.TYPE_TOKEN),Rule('key',Rule.TYPE_TOKEN)], {'key': {'key': 'value'}}, ['value'])
        self._test([Rule('ttt',Rule.TYPE_TOKEN),Rule('key',Rule.TYPE_TOKEN)], {'key': {'key': 'value'}}, [])
        self._test([Rule('key',Rule.TYPE_TOKEN),Rule('ttt',Rule.TYPE_TOKEN)], {'key': {'key': 'value'}}, [])

    def test_equals(self):
        self._test([Rule('==',Rule.TYPE_OPERATOR),Rule(5,Rule.TYPE_NUMBER)], [1,2,5], [])
        self._test([Rule('==',Rule.TYPE_OPERATOR),Rule(5,Rule.TYPE_NUMBER)], 5,       [5])

        self._test([Rule('==',Rule.TYPE_OPERATOR),Rule('m',Rule.TYPE_STRING)], 'a',     [])
        self._test([Rule('==',Rule.TYPE_OPERATOR),Rule('m',Rule.TYPE_STRING)], 'm',     ['m'])


    def test_permissive_equals(self):
        pass

    def test_greater_than(self):
        self._test([Rule('>',Rule.TYPE_OPERATOR),Rule(5,Rule.TYPE_NUMBER)],   [1,2,3], [])
        self._test([Rule('>',Rule.TYPE_OPERATOR),Rule(5,Rule.TYPE_NUMBER)],   1,       [])
        self._test([Rule('>',Rule.TYPE_OPERATOR),Rule(5,Rule.TYPE_NUMBER)],   11,      [11])
        self._test([Rule('>',Rule.TYPE_OPERATOR),Rule('m',Rule.TYPE_STRING)], 'a',     [])
        self._test([Rule('>',Rule.TYPE_OPERATOR),Rule('m',Rule.TYPE_STRING)], 'z',     ['z'])

    def test_less_than(self):
        self._test([Rule('<',Rule.TYPE_OPERATOR),Rule(5,Rule.TYPE_NUMBER)],   [1,2,3], [])
        self._test([Rule('<',Rule.TYPE_OPERATOR),Rule(5,Rule.TYPE_NUMBER)],   1,       [1])
        self._test([Rule('<',Rule.TYPE_OPERATOR),Rule(5,Rule.TYPE_NUMBER)],   11,      [])
        self._test([Rule('<',Rule.TYPE_OPERATOR),Rule('m',Rule.TYPE_STRING)], 'a',     ['a'])
        self._test([Rule('<',Rule.TYPE_OPERATOR),Rule('m',Rule.TYPE_STRING)], 'z',     [])

    def test_matches(self):
        self._test([Rule('~',Rule.TYPE_OPERATOR),Rule('.a.*',Rule.TYPE_STRING)], 'aardvark', ['aardvark'])
        self._test([Rule('~',Rule.TYPE_OPERATOR),Rule('.a.*',Rule.TYPE_STRING)], 'anteater', [])

    def test_negate(self):
        pass

    def test_current(self):
        self._test([Rule(':',Rule.TYPE_OPERATOR)], [1,2,3],          [[1,2,3]])
        self._test([Rule(':',Rule.TYPE_OPERATOR)], [[1,2,3]],        [[[1,2,3]]])
        self._test([Rule(':',Rule.TYPE_OPERATOR)], {'key': 'value'}, [{'key': 'value'}])
        self._test([Rule(':',Rule.TYPE_OPERATOR)], {'key': [1,2,3]}, [{'key': [1,2,3]}])

        self._test([Rule(':',Rule.TYPE_OPERATOR),Rule(':',Rule.TYPE_OPERATOR),Rule(':',Rule.TYPE_OPERATOR)], {'key': [1,2,3]}, [{'key': [1,2,3]}])

    def test_child(self):
        self._test([Rule('>',Rule.TYPE_OPERATOR)], [1,2,3],          [1,2,3])
        self._test([Rule('>',Rule.TYPE_OPERATOR)], [[1,2,3]],        [[1,2,3]])
        self._test([Rule('>',Rule.TYPE_OPERATOR)], {'key': 'value'}, ['value'])
        self._test([Rule('>',Rule.TYPE_OPERATOR)], {'key': [1,2,3]}, [[1,2,3]])

        self._test([Rule('>',Rule.TYPE_OPERATOR),Rule('>',Rule.TYPE_OPERATOR),Rule('>',Rule.TYPE_OPERATOR)], {'key': [[1,2,3],2,3]}, [1,2,3])

if __name__ == '__main__':
    unittest.main()
