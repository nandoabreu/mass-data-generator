#! /usr/bin/env python3

import os
import sys
import random
import datetime as _dt
from . import Person, CreditCard, BankAccount, BankTransaction


def menu():
    options = {
                'p': { 'title': 'people', 'class': 'Person', 'require': {}, },
                'c': { 'title': 'credit cards', 'class': 'CreditCard', 'require': { 'Person': 0.5, }, },
                'a': { 'title': 'bank accounts', 'class': 'BankAccount', 'require': { 'Person': 0.5  }, },
                't': { 'title': 'bank transactions', 'class': 'BankTransaction', 'require': { 'Person': 0.25, 'BankAccount': 0.5 }, },
    }

    print('Menu choices:')
    for option in options:
        print(f'\tUse {option!r} to create a {options[option]["title"]} database')

    option = input('Submit your choice: ').lower()
    if option not in options:
        print('Invalid choice.')
        return None

    return options[option]


if __name__ == '__main__':
    pid = os.getpid()
    db = menu()

    if not db: sys.exit(1)

    regs = int(input(f'Generate how many {db["title"]}? '))
    if regs < 1: sys.exit(0)

    tit = db['title'].replace(' ', '-')
    tmp = f'/tmp/csv_with_{regs}_{tit}.{pid}.csv'
    main_csv = input(f'Save to: (submit path to csv or hit Enter for {tmp}) ')
    if len(main_csv) < 1: main_csv = tmp

    people_csv = None
    people_list = []
    if 'require' in db and 'Person' in db['require']:
        people_num = round(min(max(1, regs * db['require']['Person']), (regs * db['require']['Person'])))
        original_people = min(75, round(people_num * 0.15))
        tit = 'people' if people_num > 1 else 'person'

        tmp = f'/tmp/csv_with_{people_num}_{tit}.{pid}.csv'
        people_csv = input(f'Up to {people_num} {tit} will also be created.\nSave to: (submit path to csv or hit Enter for {tmp}) ')
        if len(people_csv) < 1: people_csv = tmp

        print(f'\n#\tAttention: {original_people} {tit} will be created (slow creation),')
        print(f'#\tthen the remaining will derive from those {original_people} (fast creation)\n')
        #print(f'Up to {people_num} {tit} will be stored in {people_csv}. Please hold...')

        with open(people_csv, 'w') as csv:
            for i in range(people_num):
                if len(people_list) < original_people:
                    print(f'Slowly creating [original] person {(i+1)} of {original_people}...', end='\r')
                    obj = Person.Person()
                    obj.create()
                else:
                    print(f'Rapidly creating [derivated] person {(i+1)} of {people_num}...', end='\r')
                    name = random.choice(people_list).full_name.split(' ')[0]
                    midname = random.choice(people_list).full_name.split(' ')[-1]
                    surname_obj = random.choice(people_list)
                    surname = surname_obj.full_name.split(' ')[-1]
                    name_origin = surname_obj.name_origin
                    birth_Y = random.choice(people_list).birth_date.split('-')[0]
                    birth_M = random.choice(people_list).birth_date.split('-')[1]
                    birth_D = random.choice(people_list).birth_date.split('-')[2]
                    obj = Person.Person(f'{name} {midname} {surname}', f'{birth_Y}-{birth_M}-{birth_D}', name_origin)

                people_list.append(obj)

                if i == 0: csv.write(','.join(obj.info().keys()) + '\n')
                csv.write(obj.csv() + '\n')

        print(f'{len(people_list)} {tit} created. {" "*40}')

    accounts_csv = None
    accounts_list = []
    if 'require' in db and 'BankAccount' in db['require']:
        accounts_num = round(min(max(1, regs * db['require']['BankAccount']), (regs * db['require']['BankAccount'])))
        tit = 'accounts' if accounts_num > 1 else 'account'

        tmp = f'/tmp/csv_with_{accounts_num}_{tit}.{pid}.csv'
        accounts_csv = input(f'Up to {accounts_num} {tit} will also be created.\nSave to: (submit path to csv or hit Enter for {tmp}) ')
        if len(accounts_csv) < 1: accounts_csv = tmp
        #print(f'Up to {accounts_num} {tit} will be stored in {accounts_csv}. Please hold...')

        with open(accounts_csv, 'w') as csv:
            for i in range(accounts_num):
                print(f'Creating account {(i+1)} of {accounts_num}...', end='\r')

                obj = BankAccount.BankAccount(person=random.choice(people_list))
                if obj.number in (o.number for o in accounts_list): continue
                accounts_list.append(obj)

                if i == 0: csv.write(','.join(obj.info().keys()) + '\n')
                csv.write(obj.csv() + '\n')

        print(f'{len(accounts_list)} {tit} created. {" "*40}')

    tit = 'registries' if regs > 0 else 'registry'
    print(f'{regs} {tit} will be stored in {main_csv}. Please hold...')

    with open(main_csv, 'w') as csv:
        moment = None
        if db["class"] == 'BankTransaction':
            moment = _dt.datetime.now() - _dt.timedelta(days=((regs//6)+1))

        for i in range(regs):
    '''
            account = random.choice(accounts_list)
            moment += _dt.timedelta(hours=4)
            transaction = BankTransaction.BankTransaction(account=account, moment=moment.strftime('%Y-%m-%d %H:%M:%S'))

            if i == 0: csv.write(f'{transaction.headers()}\n')
            csv.write(f'{transaction.csv()}\n')
            print(f'Created {i} of {transactions} transaction{t}.', end='\r')

    print(f'{(i+1)} transaction{s} created in {save_to}.')
    '''

    print('Done.')
