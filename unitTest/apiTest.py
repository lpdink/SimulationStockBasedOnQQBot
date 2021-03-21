import unittest
import tsAPI.api as api

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(False, False)
    def test_getCurrent(self):
        print(api.getCurrent('000581'))
    def test_getCurrentPrice(self):
        self.assertTrue(api.getCurrentPrice('000581') - 23.100 < 0.001)

if __name__ == '__main__':
    unittest.main()
