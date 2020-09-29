#! /usr/bin/env python3
'''
This module provides access to the CreditCard class

Usage:
    c1 = CreditCard(network='Visa', number='4111111111111111')
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
    def __init__(self, network=None, issuer=None, number=None, holder_name=None, person=None, name_origin=None, expiration=None):
        country = None
        holder_id = None

        if person or not holder_name:
            if not person or not isinstance(person, Person):
                person = Person()
                person.create(name_origin=name_origin)

            holder_name = person.full_name
            country = person.name_origin[-2:]
            holder_id = person.id

        elif name_origin:
            country = name_origin[-2:]

        if not network:
            network = random.choice([n for n in networks.keys() if networks[n]['country'] in (country, None)])

        if not issuer:
            issuer = random.choice([i for i in issuers.companies.keys() if issuers.companies[i] in (country, None)])

        if not number:
            number = str(random.choice(networks[network]['prefix']))

            while True:
                number += str(random.random())[2:3]
                if len(number) == (networks[network]['digits']-1): break

            s = 0
            for i, d in enumerate(number[::-1]):
                d = int(d)
                if i % 2 == 0: d *= 2
                s += sum([int(d) for d in str(d)])

            number = int(number + str(10 - (s % 10)))

        if not expiration:
            expiration = _dt.datetime.now() + _dt.timedelta(days=random.randrange(-6, 48)*30)
            expiration = expiration.strftime('%m/%y')

        self.network = network
        self.issuer = issuer
        self.number = number
        self.holder_name = holder_name
        self.holder_id = holder_id
        self.expiration = expiration

    def info(self) -> dict:
        '''
        Return a dictionary with Credit Card object data
        '''
        return { 'network': self.network, 'issuer': self.issuer, 'number': self.number, 'holder_name': self.holder_name, 'holder_id': self.holder_id, 'expiration': self.expiration }

    def csv(self) -> str:
        '''
        Return a csv string with Credit Card object data
        '''
        return f'"{self.network}","{self.issuer}",{self.number},"{self.holder_name}",{self.holder_id},{self.expiration}'.replace('None', '').replace('""', '')

