from visitor import visit
from rule import Rule
import unittest

class TestParser(unittest.TestCase):
    def _test(self, rules, nodes, expected):
        results = visit(rules, nodes)
        self.assertEqual(results, expected)

    def test_index(self):
        # :Tab / \([\|{\)/l0
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
        pass

    def test_permissive_equals(self):
        pass

    def test_greater_than(self):
        pass

    def test_less_than(self):
        pass

    def test_matches(self):
        pass

    def test_negate(self):
        pass

    def test_current(self):
        pass

    def test_child(self):
        pass

if __name__ == '__main__':
    unittest.main()
