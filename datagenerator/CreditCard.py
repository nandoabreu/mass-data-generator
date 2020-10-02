#! /usr/bin/env python3
'''
This module provides access to the CreditCard class

Usage:
    c1 = CreditCard(network='Visa', card_number='4111111111111111')
    c1.info()

    p1 = Person()
    p1.create('pt_BR')
    c2 = CreditCard(person=p1)
    c2.info()
'''
import random
import datetime as _dt
from .Person import Person
from . import issuers


networks = {
             'Visa': { 'country': None, 'digits': 16, 'prefix': [4] },
             'Mastercard': { 'country': None, 'digits': 16, 'prefix': [51,52,53,54,55] },
             'American Express': { 'country': None, 'digits': 15, 'prefix': [34,37] },
             'Diners Club': { 'country': None, 'digits': 14, 'prefix': [36,38] },
             'Discover': { 'country': 'US', 'digits': 16, 'prefix': [60,65] },
             'JCB': { 'country': 'US', 'digits': 16, 'prefix': [35] },
             'Hipercard': { 'country': 'BR', 'digits': 16, 'prefix': [38,60] },
             'Elo': { 'country': 'BR', 'digits': 16, 'prefix': [36297,5067,4576,4011] },
}

class CreditCard:
    '''
    The CreditCard object can be initialised empty or with arguments
    If not provided, credit card data will be automatically set

    Arguments:
        network (str), optional: as in `Visa`, `Mastercard`, `Hipercard`
        issuer (str), optional: as in `Bank of China`, `Lloyds`, `Baroda`
        card_number (int), optional: recommended 14 to 16 numbers
        expiration (str), optional: recommended to follow `MM/YY` format

        person (obj), optional:
            send a constructed Person object to replace subscriber_name
            person has precedence over subscriber_name argument

        subscriber_name (str), optional:
            recommended to have two or more names
            or use person argument to use a Person object

        subscriber_origin (str), optional:
            If sent, must follow ISOs 3166 and 639, as in `pt_BR`
            If a subscriber_name is provided, this should qualify subscriber's origin
            If neither a subscriber nor a person is provided, subscriber_origin may help
            to automatically create a new person with name from this origin
            If network and/or issuer are not provided, this value may help
            choosing not only between global networks or issuers, but also
            between local ones, if avaliable in networks (line 24) and issuers

    Attributes:
        network (str),
        issuer (str),
        card_number (int),
        subscriber_name (str),
        subscriber_id (str),
        expiration (str)
    '''
    def __init__(self, network=None, issuer=None, card_number=None, subscriber_name=None, person=None, subscriber_origin=None, expiration=None):
        country = None
        subscriber_id = None

        if person or not subscriber_name:
            if not person or not isinstance(person, Person):
                person = Person()
                person.create(name_origin=subscriber_origin)

            subscriber_name = person.full_name
            country = person.name_origin[-2:]
            subscriber_id = person.id

        elif subscriber_origin:
            country = subscriber_origin[-2:]

        if not network:
            network = random.choice([n for n in networks.keys() if networks[n]['country'] in (country, None)])

        if not issuer:
            issuer = random.choice([i for i in issuers.companies.keys() if issuers.companies[i] in (country, None)])

        if not card_number:
            card_number = str(random.choice(networks[network]['prefix']))

            while True:
                card_number += str(random.random())[2:3]
                if len(card_number) == (networks[network]['digits']-1): break

            s = 0
            for i, d in enumerate(card_number[::-1]):
                d = int(d)
                if i % 2 == 0: d *= 2
                s += sum([int(d) for d in str(d)])

            card_number = int(card_number + str(10 - (s % 10)))

        if not expiration:
            expiration = _dt.datetime.now() + _dt.timedelta(days=random.randrange(-6, 48)*30)
            expiration = expiration.strftime('%m/%y')

        self.network = network
        self.issuer = issuer
        self.card_number = card_number
        self.subscriber_name = subscriber_name
        self.subscriber_id = subscriber_id
        self.expiration = expiration

    def info(self) -> dict:
        '''
        Return a dictionary with Credit Card object data
        '''
        return { 'network': self.network, 'issuer': self.issuer, 'card_number': self.card_number, 
                 'subscriber_name': self.subscriber_name, 'subscriber_id': self.subscriber_id, 'expiration': self.expiration }

    def csv(self) -> str:
        '''
        Return a csv string with Credit Card object data
        '''
        return f'"{self.network}","{self.issuer}",{self.card_number},"{self.subscriber_name}",{self.subscriber_id},{self.expiration}'.replace('None', '').replace('""', '')

