#! /usr/bin/env python3

import sys
import random
import datetime as _dt
from . import BankAccount, BankTransaction


if __name__ == '__main__':
    tmp = f'/tmp/data.{int(random.randrange(1001,9999))}.csv'
    save_to = input(f'Inform the path to the file to store data: [Hit Enter for {tmp}] ')
    if len(save_to) < 1: save_to = tmp

    transactions = int(input('Generate how many bank transactions? '))
    accounts_to_create = min(max(1, transactions//100), 100)
    s = 's' if accounts_to_create > 1 else ''

    print(f'Generating {accounts_to_create} account{s}. Please hold...')

    accounts = []
    for i in range(accounts_to_create):
        if len(accounts) < 10:
            account = BankAccount()
        else:
            name = random.choice(accounts).owner.split(' ')[0]
            surname = random.choice(accounts).owner.split(' ')[-1]
            account = BankAccount(owner=f'{name} {surname}')

        if account.number in [a.number for a in accounts]:
            del account
            continue

        accounts.append(account)
        print(f'Created {i} of {accounts_to_create} account{s}.', end='\r')

    t = 's' if transactions > 1 else ''
    print(f'{len(accounts)} account{s} created. Generating {transactions} transaction{t}. Please hold...')

    with open(save_to, 'w') as csv:
        moment = _dt.datetime.now() - _dt.timedelta(days=((transactions//6)+1))
        for i in range(transactions):
            account = random.choice(accounts)
            moment += _dt.timedelta(hours=4)
            transaction = BankTransaction(account=account, moment=moment.strftime('%Y-%m-%d %H:%M:%S'))

            if i == 0: csv.write(f'{transaction.headers()}\n')
            csv.write(f'{transaction.csv()}\n')
            print(f'Created {i} of {transactions} transaction{t}.', end='\r')

    print(f'{(i+1)} transaction{s} created in {save_to}.')

