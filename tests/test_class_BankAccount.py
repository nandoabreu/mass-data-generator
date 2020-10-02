#! /usr/bin/env python3

import unittest
from datagenerator.BankAccount import BankAccount
from datagenerator.Person import Person


verbose_tests = False

class Test(unittest.TestCase):
    def setUp(self):
        self.object = BankAccount()
        self.person = Person('Alan Turing', '1912-06-23', 'en_GB')

    def test_object(self):
        self.assertIsInstance(self.object, BankAccount)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_auto_setup(self):
        self.assertIsNotNone(self.object.account_number)
        self.assertIsInstance(self.object.account_number, int)
        self.assertGreater(self.object.account_number, 4)

        self.assertIsNotNone(self.object.balance)
        self.assertIsInstance(self.object.balance, (int, float))
        self.assertEqual(self.object.balance, 0)

        self.assertIsNotNone(self.object.active)
        self.assertGreaterEqual(self.object.active, 0)
        self.assertLessEqual(self.object.active, 1)

        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_person(self):
        o = BankAccount(person=self.person)
        self.assertIsNotNone(o.subscriber_name)
        self.assertEqual(o.subscriber_name, self.person.full_name)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_values(self):
        o = BankAccount(account_number=987654, subscriber_name='Alan Turing', subscriber_origin='en_GB', active=1)
        self.assertEqual(o.account_number, 987654)
        self.assertEqual(o.subscriber_name, 'Alan Turing')
        self.assertEqual(o.active, 1)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_csv_string(self):
        self.assertIn(',', self.object.csv())
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

