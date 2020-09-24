#! /usr/bin/env python3

import random
import requests
import json
import datetime as _dt


class BankAccount:
    def __init__(self, number=None, owner=None):
        if not number: number = random.randrange(10001, 99999)
        if not owner:
            language = random.choice(('spanish-spain', 'english-united-kingdom', 'portuguese-portugal', 'french-france'))
            res = requests.get(f'https://api.namefake.com/{language}/random/')
            owner = json.loads(res.text)['name']

        self.number = number
        self.owner = owner
        self.balance = 0

class BankTransaction:
    def __init__(self, value=None, account=None, moment=None, description=None):
        actions = { 'Deposit': +1, 'Credit Transfer': +1, 'Withdrawl': -1, 'Debit Payment': -1 }

        if not description or description not in actions:
            description = random.choice(list(actions))

        try:
            value = abs(float(value))
        except:
            value = random.random() * (10 ** random.randrange(1,6))
        finally:
            value = round(value, 2) * actions[description]

        if not account or not isinstance(account, BankAccount):
            account = BankAccount()

        try:
            moment = _dt.datetime.strptime(f'{moment}', f'%Y-%m-%d %H:%M:%S')
        except:
            moment = _dt.datetime.now()

        self.value = value
        self.account = account
        self.moment = moment
        self.description = description

        self.account.balance = account.balance + value

    def csv(self) -> str:
        moment = self.moment.strftime('%Y-%m-%d %H:%M:%S')
        return f'{moment},{self.account.number},{self.description},{self.value},{self.account.balance:.2f}'

    def headers(self):
        return 'moment,account,description,value,balance'

