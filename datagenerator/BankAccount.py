#! /usr/bin/env python3
'''
This module provides access to the BankAccount class

Usage:
    a1 = BankAccount(number=90101, owner_name='Lara Lugo', active=1)
    a1.info()

    person = Person()
    person.create('de_AT')
    a2 = BankAccount(person=person)
    a2.info()

    a3 = BankAccount(owner_origin='nl_BE')
    a3.info()
'''
import random
from .Person import Person


class BankAccount:
    '''
    The BankAccount object can be initialised empty or with arguments
    For each not provided argument, data will be randomly set

    Arguments:
        number (int), optional: recommended 4 to 8 numbers
        active (int), optional: use 1 for active or 0 for inactive

        person (obj), optional:
            send a constructed Person object to replace owner_name
            person has precedence over owner_name argument

        owner_name (str), optional:
            recommended to have two or more names
            or use person argument to use a Person object

        owner_origin (str), optional:
            If sent, must follow ISOs 3166 and 639, as in `pt_BR`
            If a owner_name is provided, this should qualify holder's origin
            If neither a holder nor a person is provided, owner_origin may help
            to automatically create a new person with name from this origin
            If network and/or issuer are not provided, this value may help
            choosing not only between global networks or issuers, but also
            between local ones, if avaliable in networks (line 24) and issuers

    Attributes:
        balance (float): initiates with 0.00
        owner_id (str): if BankAccount receives/creates a Person, this will be set
        active (int): 0 for inactive account, 1 for active account
        owner_name (str),
        number (int)
    '''
    def __init__(self, number=None, owner_name=None, person=None, owner_origin=None, active=None):
        owner_id = None

        if person or not owner_name:
            if not person or not isinstance(person, Person):
                person = Person()
                person.create(name_origin=owner_origin)

            owner_name = person.full_name
            owner_id = person.id

        if not number:
            number = random.randrange(10001, 99999)

        if not active or active not in (0, 1):
            active = 0 if (random.randrange(99) % 10) == 0 else 1

        self.number = number
        self.balance = 0
        self.owner_name = owner_name
        self.owner_id = owner_id
        self.active = active

    def info(self) -> dict:
        '''
        Return a dictionary with Bank Account object data
        '''
        return { 'number': self.number, 'balance': self.balance, 'owner_name': self.owner_name, 'owner_id': self.owner_id, 'active': self.active }
