from visitor import visit
import unittest

class TestParser(unittest.TestCase):
    def _test(self, rules, nodes, expected):
        results = visit(rules, nodes)
        self.assertEqual(results, expected)

    def test_index(self):
        self._test([('0','token')], [1,2,3], [1])

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
