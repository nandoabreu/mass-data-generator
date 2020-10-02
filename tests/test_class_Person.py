#! /usr/bin/env python3

import unittest
from datagenerator.Person import Person


verbose_tests = False

class Test(unittest.TestCase):
    def setUp(self):
        self.object = Person()

    def test_object(self):
        self.assertIsInstance(self.object, Person)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_random_origin(self):
        self.object.create()
        self.assertIsInstance(self.object.id, str)
        self.assertGreater(len(self.object.id), 0)
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_origin(self):
        o = Person()
        o.create('pt_BR')
        self.assertEqual(o.name_origin, 'pt_BR')
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_object_setup_defined_values(self):
        o = Person(full_name='Alan Turing', birth_date='1912-06-23', name_origin='en_GB')
        self.assertEqual(o.full_name, 'Alan Turing')
        self.assertEqual(o.birth_date, '1912-06-23')
        self.assertEqual(o.name_origin, 'en_GB')
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def test_csv_string(self):
        self.assertIn(',', self.object.csv())
        if verbose_tests: print(f'TEST:ran {self.id()}')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()

