#! /usr/bin/env python3

import unittest
from datagenerator.CreditCard import CreditCard
from datagenerator.Person import Person


verbose_tests = False

class Test(unittest.TestCase):
    def setUp(self):
        self.object = CreditCard()
        self.person = Person('Alan Turing', '1912-06-23', 'en_GB')

    def test_object(self):
        self.assertIsInstance(self.object, CreditCard)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_auto_setup(self):
        self.assertIsNotNone(self.object.network)
        self.assertIsInstance(self.object.network, str)

        self.assertIsNotNone(self.object.issuer)
        self.assertIsInstance(self.object.issuer, str)

        self.assertIsNotNone(self.object.card_number)
        self.assertIsInstance(self.object.card_number, int)
        self.assertGreater(self.object.card_number, 10)

        self.assertIsNotNone(self.object.subscriber_name)
        self.assertIsInstance(self.object.subscriber_name, str)

        self.assertIsNotNone(self.object.subscriber_id)
        self.assertIsInstance(self.object.subscriber_id, str)

        self.assertIsNotNone(self.object.expiration)
        self.assertIsInstance(self.object.expiration, str)

        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_person(self):
        o = CreditCard(person=self.person)
        self.assertIsNotNone(o.subscriber_name)
        self.assertEqual(o.subscriber_name, self.person.full_name)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_origin(self):
        o = CreditCard(subscriber_origin='en_GB')
        self.assertIsNotNone(o.subscriber_name)
        self.assertIsInstance(o.subscriber_name, str)
        self.assertGreater(len(o.subscriber_name), 4)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_values(self):
        o = CreditCard(network='Mastercard', issuer='Nubank', card_number=4111111111111111, subscriber_name='Alan Turing', subscriber_origin='en_GB', expiration='10/22')
        self.assertEqual(o.network, 'Mastercard')
        self.assertEqual(o.issuer, 'Nubank')
        self.assertEqual(o.card_number, 4111111111111111)
        self.assertEqual(o.subscriber_name, 'Alan Turing')
        self.assertEqual(o.expiration, '10/22')
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_csv_string(self):
        self.assertIn(',', self.object.csv())
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

