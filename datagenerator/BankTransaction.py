#! /usr/bin/env python3
'''
This module provides access to the BankTransaction class

Usage:
    t1 = BankTransaction()
    t1.info()

    t2 = BankTransaction(account=BankAccount(number=90101))
    t2.info()

    account_list = [BankAccount(owner_origin='nn_NO')]
    t3 = BankTransaction(account=account_list[0])
    t4 = BankTransaction(account=account_list[0])
    t3.info()
    t4.info()

    person_ca = Person()
    person_ca.create('fr_CA')
    ba = BankAccount(person=person_ca)
    transaction = BankTransaction(account=ba)
    transaction.info()
'''
import random
from datetime import datetime
from .BankAccount import BankAccount


actions = {
            'Deposit': +1,
            'Credit Transfer': +1,
            'Withdrawl': -1,
            'Debit Payment': -1
}

class BankTransaction:
    '''
    The BankTransaction object can be initialised empty or with arguments
    For each omitted argument, data will be randomly set

    Arguments:
        value (float), optional:
            float number as in `9999.10` or `-1000`
            Note: if description is provided, value should be also

        description (str), optional:
            If not in actions (line 21) and value has `-`, will be a debit
            If description is in actions, signs in value will be ignored
            Its recommended to provide a value if description is customised

        moment (str), optional:
            If provided, recommended `YYYY-mm-dd HH:MM:SS` format
            If omitted, current date and time will be provided

        account (obj), optional:
            send a constructed Account object to replace account_number
            Account has precedence over account_number argument

        account_number (int), optional:
            recommended to have 4-8 digits
            or use account argument to use an Account object

    Attributes:
        account_number (int): account number for the transaction
        account_balance (float): if a BankAccount object is provided
        description (str),
        moment (str),
        value (float)
    '''
    def __init__(self, value=None, description=None, moment=None, account=None, account_number=None):
        if account or not account_number:
            if not account or not isinstance(account, BankAccount):
                account = BankAccount(owner_name='Jane Doe')

            account_number = account.number

        operation = None
        if description:
            if description in actions:
                operation = actions[description]
            else:
                operation = '-1' if value < 0 else '+1'

        else:
            description = random.choice(list(actions))
            operation = actions[description]

        if not isinstance(value, (float, int)):
            value = random.random() * (10 ** random.randrange(1,6))
        value = round( abs(float(value)), 2 ) * operation

        if not moment:
            moment = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.moment = moment
        self.account_number = account_number
        self.value = value
        self.description = description

        if account:
            account_balance = round( account.balance + value, 2 )
            self.account_balance = account.balance = account_balance

        else:
            self.account_balance = round( value, 2 )

    def info(self) -> dict:
        '''
        Return a dictionary with Bank Transaction object data
        '''
        return { 'moment': self.moment, 'account_number': self.account_number, 'value': self.value, 'description': self.description, 'account_balance': self.account_balance }

    def csv(self) -> str:
        '''
        Return a csv string with Bank Transaction object data
        '''
        return f'"{self.moment}",{self.account_number},{self.value},"{self.description}",{self.account_balance}'.replace('None', '').replace('""', '')

