#! /usr/bin/env python3
'''
This module provides access to the BankAccount class

Usage:
    a1 = BankAccount(account_number=90101, subscriber_name='Lara Lugo', active=1)
    a1.info()

    person = Person()
    person.create('de_AT')
    a2 = BankAccount(person=person)
    a2.info()

    a3 = BankAccount(subscriber_origin='nl_BE')
    a3.info()
'''
import random
from .Person import Person


class BankAccount:
    '''
    The BankAccount object can be initialised empty or with arguments
    For each not provided argument, data will be randomly set

    Arguments:
        account_number (int), optional: recommended 4 to 8 numbers
        active (int), optional: use 1 for active or 0 for inactive

        person (obj), optional:
            send a constructed Person object to replace subscriber_name
            person has precedence over subscriber_name argument

        subscriber_name (str), optional:
            recommended to have two or more names
            or use person argument to use a Person object

        subscriber_origin (str), optional:
            If sent, must follow ISOs 3166 and 639, as in `pt_BR`
            If a subscriber_name is provided, this should qualify holder's origin
            If neither a holder nor a person is provided, subscriber_origin may help
            to automatically create a new person with name from this origin
            If network and/or issuer are not provided, this value may help
            choosing not only between global networks or issuers, but also
            between local ones, if avaliable in networks (line 24) and issuers

    Attributes:
        balance (float): initiates with 0.00
        subscriber_id (str): if BankAccount receives/creates a Person, this will be set
        active (int): 0 for inactive account, 1 for active account
        subscriber_name (str),
        account_number (int)
    '''
    def __init__(self, account_number=None, subscriber_name=None, person=None, subscriber_origin=None, active=None):
        subscriber_id = None

        if person or not subscriber_name:
            if not person or not isinstance(person, Person):
                person = Person()
                person.create(name_origin=subscriber_origin)

            subscriber_name = person.full_name
            subscriber_id = person.id

        if not account_number:
            account_number = random.randrange(10001, 99999)

        if not active or active not in (0, 1):
            active = 0 if (random.randrange(99) % 10) == 0 else 1

        self.account_number = account_number
        self.balance = 0
        self.subscriber_name = subscriber_name
        self.subscriber_id = subscriber_id
        self.active = active

    def info(self) -> dict:
        '''
        Return a dictionary with Bank Account object data
        '''
        return { 'account_number': self.account_number, 'balance': self.balance, 'subscriber_name': self.subscriber_name, 'subscriber_id': self.subscriber_id, 'active': self.active }

    def csv(self) -> str:
        '''
        Return a csv string with Bank Account object data
        '''
        return f'{self.account_number},{self.balance},"{self.subscriber_name}",{self.subscriber_id},{self.active}'.replace('None', '').replace('""', '')

