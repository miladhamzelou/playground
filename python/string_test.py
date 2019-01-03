# python3 -m unittest string_test.py -v
# python3 -m unittest string_test.StringTestCase.test_upper
# python3 -m unittest discover -s . -p "*_test.py" -v
# python3 -m unittest discover . "*_test.py" -v

import unittest

class StringTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(StringTestCase())
    return suite

if __name__ == '__main__':
    # unittest.main()
    runner = unittest.TextTestRunner()
    runner.run(suite())
