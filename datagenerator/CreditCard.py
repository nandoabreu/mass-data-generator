#! /usr/bin/env python3

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
    def __init__(self, holder_name=None, network=None, issuer=None, number=None, expiration=None):
        if number and int(number) < (10 ** 13): number = None

        self.network = network
        self.issuer = issuer
        self.number = number
        self.holder_name = holder_name
        self.expiration = expiration

    def create(self, person=None, name_origin=None, network=None, issuer=None):
        country = None

        if not person or not isinstance(person, Person):
            person = Person()
            person.create(name_origin=name_origin)
            if person.name_origin: country = person.name_origin[-2:]
        elif name_origin:
            country = name_origin[-2:]

        try:
            if not network:
                raise RuntimeWarning
            if network not in networks:
                raise KeyError(f'I don\'t have {network!r} as a known credit card network. ')
        except Exception as e:
                network = random.choice([n for n in networks.keys() if networks[n]['country'] in (country, None)])
                print('# INFO: {0}Using network: {1!r}.'.format(str(e).strip('"'), network))

        try:
            if not issuer:
                raise RuntimeWarning
            if issuer not in issuers.companies:
                raise KeyError(f'I don\'t have {issuer!r} as known credit card issuer. ')
        except Exception as e:
                issuer = random.choice([i for i in issuers.companies.keys() if issuers.companies[i] in (country, None)])
                print('# INFO: {0}Using issuer: {1!r}.'.format(str(e).strip('"'), issuer))

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
        expiration = _dt.datetime.now() + _dt.timedelta(days=random.randrange(-6, 48)*30)

        self.network = network
        self.issuer = issuer
        self.number = number
        self.holder_name = person.full_name
        self.expiration = expiration.strftime('%m/%y')

    def info(self) -> dict:
        '''
        Return a dictionary with Credit Card information
        '''
        return { 'network': self.network, 'issuer': self.issuer, 'number': self.number, 'holder_name': self.holder_name, 'expiration': self.expiration }

