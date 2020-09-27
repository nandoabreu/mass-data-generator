#! /usr/bin/env python3
'''
This module provides access to the BankAccount class

Usage:
    a1 = BankAccount(number=90101, active=1)
    a1.info()

    obj = Person()
    obj.create('fr_FR')
    a2 = BankAccount(person=obj)
    a2.info()
'''
import random
from .Person import Person


class BankAccount:
    '''
    The CreditCard object can be initialised empty or with arguments
    If not provided, credit card data will be automatically set

        self.number = number
        self.balance = 0
        self.owner_name = owner_name
        self.owner_id = owner_id
        self.active = active

    Arguments:
        network (str), optional: as in `Visa`, `Mastercard`, `Hipercard`
        issuer (str), optional: as in `Bank of China`, `Lloyds`, `Baroda`
        number (int), optional: recommended 14 to 16 numbers
        expiration (str), optional: recommended to follow `MM/YY` format

        person (obj), optional:
            send a constructed Person object to replace holder_name
            person has precedence over holder_name argument

        holder_name (str), optional:
            recommended to have two or more names
            or use person argument to use a Person object

        name_origin (str), optional:
            If sent, must follow ISOs 3166 and 639, as in `pt_BR`
            If a holder_name is provided, this should qualify holder's origin
            If neither a holder nor a person is provided, name_origin may help
            to automatically create a new person with name from this origin
            If network and/or issuer are not provided, this value may help
            choosing not only between global networks or issuers, but also
            between local ones, if avaliable in networks (line 24) and issuers

    Attributes:
        network (str),
        issuer (str),
        number (int),
        holder_name (str),
        holder_id (str),
        expiration (str)
    '''
    def __init__(self, number=None, owner_name=None, person=None, name_origin=False, active=None):
        owner_id = None

        if person or not owner_name:
            if not person or not isinstance(person, Person):
                person = Person()
                person.create(name_origin=name_origin)

            owner_name = person.full_name
            owner_id = person.id

        if not number:
            number = random.randrange(10001, 99999)

        if not active or active not in (0, 1):
            status = 0 if (random.randrange(99) % 10) == 0 else 1

        self.number = number
        self.balance = 0
        self.owner_name = owner_name
        self.owner_id = owner_id
        self.active = active

    def info(self) -> dict:
        '''
        Return a dictionary with Bank Account object data
        '''
        return { 'number': self.number, 'balance', self.balance, 'owner_name': self.owner_name, 'owner_id': self.owner_id, 'active': self.active }

