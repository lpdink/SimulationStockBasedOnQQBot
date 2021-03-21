import unittest
import tsAPI.csvapi as csvapi
# -*- coding:utf-8 -*-

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_print(self):
        csvapi.getIdByName('')

    def test_init(self):
        csvapi.initDic()

    def test_getName(self):
        csvapi.initDic()
        csvapi.getCodeByName("中平安")

if __name__ == '__main__':
    unittest.main()
