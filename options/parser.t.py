from parser import parse_arguments
import unittest

class TestParser(unittest.TestCase):
    def test_string(self):
       tokens = parse_arguments("'hello'")
       self.assertEqual(tokens, [("'hello'", 'string')])

    def test_number(self):
        pass

    def test_token(self):
        pass

    def test_operator(self):
        pass

    def test_invalid(self):
        pass

if __name__ == '__main__':
    unittest.main()
