#! /usr/bin/env python3

import random
from . import Person
from . import issuers


class CreditCard:
    def __init__(self, network=None, issuer=None, number=None, person=None):
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

        if number and len(str(abs(int(number)))) < 10: number = None

        self.network = network
        self.issuer = issuer
        self.number = number
        self.person = person
        

#if not issuer: issuer = random.choice([ company for company in issuers.companies if not issuers.companies[company] ])
#if not network: network = random.choice([ network for network in networks if not networks[network]['country'] ])
