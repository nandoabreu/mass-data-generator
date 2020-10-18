#! /usr/bin/env python3

import os
import sys
import random
import datetime as _dt
from . import Person, CreditCard, BankAccount, BankTransaction


def menu() -> dict:
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
        sys.exit(1)

    return options[option]

def generate_people(regs_num: int) -> list:
    #original_regs = int(regs_num * 0.1)
    original_regs = min(100, round(regs_num * 0.15))

    print(f'\n#\tAttention: {original_regs:,} people will be created (slow creation),')
    print(f'#\tand other {(regs_num-original_regs):,} will derive from the those (fast creation).\n')

    original_objs = []
    response_list = []

    i = 0
    empty = 0
    while True:
        print(f'Creating person {(i+1):,} of {regs_num:,}... {" "*30}', end='\r')

        if len(original_objs) < original_regs:
            obj = Person.Person()
            obj.create()

            if obj and obj.full_name:
                original_objs.append(obj)
                if empty > 0: empty = 0
            elif empty > 4:
                print(f'{empty} errors on trying to parse person: ABORT')
                return original_objs
            else:
                empty +=1
                print(f'{empty} errors on parsing person {i}: RETRY', end='\r')
                continue
        else:
            if not response_list: response_list = original_objs[:]

            name = random.choice(original_objs).full_name.split(' ')[0]
            midname = random.choice(random.choice(original_objs).full_name.split(' '))
            surname_obj = random.choice(original_objs)
            surname = surname_obj.full_name.split(' ')[-1]
            name_origin = surname_obj.name_origin

            birth_Y = random.randint(1940,2000)
            birth_M = str(random.randint(1,12)).zfill(2)
            birth_D = str(random.randint(1,28)).zfill(2)

            obj = Person.Person(full_name=f'{name} {midname} {surname}', birth_date=f'{birth_Y}-{birth_M}-{birth_D}', name_origin=name_origin)

            response_list.append(obj)
            if len(response_list) == regs_num:
                print(f'{len(response_list):,} people created. {" "*40}')
                print(f'List of objects using {sys.getsizeof(response_list)/(10**6):.1f}MB')
                return response_list

        i += 1

def generate_accounts(regs_num: int, people_list: list) -> list:
    response_list = []
    while len(response_list) < regs_num:
        print(f'Creating account {len(i)+1} of {regs_num}... {" "*30}', end='\r')

        obj = BankAccount.BankAccount(person=random.choice(people_list))
        if not obj.number in (o.number for o in response_list):
            response_list.append(obj)

    print(f'{len(response_list):,} accounts created. {" "*40}')
    print(f'List of objects using {sys.getsizeof(response_list)/(10**6):.1f} MB')
    return response_list


if __name__ == '__main__':
    pid = os.getpid()
    db = menu()

    main_regs = int(input(f'Generate how many {db["title"]}? '))
    if main_regs < 1: sys.exit(2)

    tmp = f'/tmp/{main_regs:,}_{db["title"]}.{pid}.csv'.replace(',', '_').replace(' ', '-')
    main_csv = input(f'Save to: (submit path to csv or Enter for {tmp}) ')
    if len(main_csv) < 1: main_csv = tmp

    people_list = []
    if 'require' in db and 'Person' in db['require']:
        regs = round(min(max(1, main_regs * db['require']['Person']), (main_regs * db['require']['Person'])))

        tmp = f'/tmp/{regs:,}_people.{pid}.csv'.replace(',', '_').replace(' ', '-')
        csv = input(f'{regs:,} people will also be created.\nSave to: (submit path to csv or Enter for {tmp}) ')
        if len(csv) < 1: csv = tmp

        people_list = generate_people(regs)

        with open(csv, 'w') as csv:
            for i, obj in enumerate(people_list):
                if i == 0: csv.write(','.join(obj.info().keys()) + '\n')
                csv.write(obj.csv() + '\n')

    accounts_list = []
    if 'require' in db and 'BankAccount' in db['require']:
        regs = round(min(max(1, main_regs * db['require']['BankAccount']), (main_regs * db['require']['BankAccount'])))

        tmp = f'/tmp/{regs:,}_accounts.{pid}.csv'.replace(',', '_').replace(' ', '-')
        csv = input(f'{regs:,} accounts will also be created.\nSave to: (submit path to csv or Enter for {tmp}) ')
        if len(csv) < 1: csv = tmp

        accounts_list = generate_accounts(regs, people_list)

        with open(csv, 'w') as csv:
            for i, obj in enumerate(accounts_list):
                if i == 0: csv.write(','.join(obj.info().keys()) + '\n')
                csv.write(obj.csv() + '\n')

    print(f'\n{main_regs:,} {db["title"]} will now be created. Please hold.')
    import time

    with open(main_csv, 'w') as csv:
        obj_list = []

        moment = None
        if db["class"] == 'BankTransaction':
            moment = _dt.datetime.now() - _dt.timedelta(days=((regs//6)+1))

        if db["class"] == 'Person':
            obj_list = generate_people(main_regs)

        elif db["class"] == 'BankAccount':
            obj_list = generate_accounts(main_regs, people_list)

        print(f'\n{len(obj_list):,} {db["title"]} will now be stored. Please hold.')

        for i, obj in enumerate(obj_list):
            print(f'Storing {(i+1):,} of {len(obj_list):,} {db["title"]}... {" "*30}', end='\r')

            person, account = None, None
            if people_list: person = random.choice(people_list)
            if accounts_list: account = random.choice(accounts_list)
            if moment: moment += _dt.timedelta(hours=4)

            if i == 0: csv.write(','.join(obj.info().keys()) + '\n')
            csv.write(obj.csv() + '\n')

        print(f'{(i+1):,} {db["title"]} stored. {" "*40}')
    print('Done.')

