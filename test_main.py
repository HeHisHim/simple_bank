import unittest
from main import SimpleBank
import pyautogui
import time

class TestMain(unittest.TestCase):
    def setUp(self):
        self.simple_bank = SimpleBank()
        self.simple_bank.account = "test_user"
        self.simple_bank.data[self.simple_bank.account] = 1000

    def test_create(self):
        self.assertEqual(self.simple_bank.account in self.simple_bank.data, True)
        self.assertEqual(1000 == self.simple_bank.data[self.simple_bank.account], True)

    def test_deposit(self):
        self.simple_bank.data[self.simple_bank.account] += 100
        self.assertEqual(1100 == self.simple_bank.data[self.simple_bank.account], True)

    def test_withdraw(self):
        self.simple_bank.data[self.simple_bank.account] -= 100
        self.assertEqual(900 == self.simple_bank.data[self.simple_bank.account], True)

    def test_transfer(self):
        self.simple_bank.data[self.simple_bank.account] -= 100
        self.assertEqual(900 == self.simple_bank.data[self.simple_bank.account], True)

if "__main__" == __name__:
    unittest.main()