#! /usr/bin/env python3

import unittest
from datagenerator.BankTransaction import BankTransaction
from datagenerator.BankAccount import BankAccount


verbose_tests = False

class Test(unittest.TestCase):
    def setUp(self):
        self.object = BankTransaction()
        self.account = BankAccount(subscriber_name='Alan Turing')

    def test_object(self):
        self.assertIsInstance(self.object, BankTransaction)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_auto_setup(self):
        self.assertIsNotNone(self.object.moment)
        self.assertIsInstance(self.object.moment, str)

        self.assertIsNotNone(self.object.account_number)
        self.assertIsInstance(self.object.account_number, int)

        self.assertIsNotNone(self.object.value)
        self.assertIsInstance(self.object.value, (float, int))
        self.assertGreater(abs(self.object.value), 0)

        self.assertIsNotNone(self.object.description)
        self.assertIsInstance(self.object.description, str)

        self.assertIsNotNone(self.object.account_balance)
        self.assertIsInstance(self.object.account_balance, (float, int))
        self.assertGreater(abs(self.object.account_balance), 0)

        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_account(self):
        o = BankTransaction(account=self.account)
        self.assertEqual(o.account_balance, self.account.balance)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_values(self):
        o = BankTransaction(value=5000, description='Salary', moment='2020-10-01 21:29:14', account_number=91234)
        self.assertGreater(o.value, 0)
        self.assertEqual(o.description, 'Salary')
        self.assertEqual(o.moment, '2020-10-01 21:29:14')
        self.assertEqual(o.account_number, 91234)
        self.assertEqual(o.account_balance, o.value)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_csv_string(self):
        self.assertIn(',', self.object.csv())
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

