#! /usr/bin/env python3
'''
Generate Person object
'''
import datetime as _dt
import random
import requests
import json
import re
from . import countries


class Person:
    def __init__(self, full_name=None, birth_date=None):
        '''
        Object initialization

        Arguments:
            full_name (str), optional: if provided, must have at least one name and one family name
            birth_date (str), optional: if provided, must follow YYYY-MM-DD format

        To print object's informations, use Person.info()
        '''
        if birth_date:
            try:
                birth_obj = _dt.datetime.strptime(f'{birth_date} 00:00:00', '%Y-%m-%d %H:%M:%S')
                if _dt.datetime.now() < birth_obj:
                    raise ValueError('Birth date in the future')
                birth_date = birth_obj.strftime('%Y-%m-%d')
            except Exception as e:
                print(f'# WARNING: {e}')
                birth_date = None

        if full_name:
            try:
                if (len(full_name) < 5 or ' ' not in full_name):
                    raise ValueError('Full name has less than 5 letters or doesn\'t have \'names + family names\'')
            except Exception as e:
                full_name = None
                print(f'# WARNING: {e}')

        self.full_name = full_name
        self.birth_date = birth_date
        self.name_origin = '(undefined)'

    def create(self, name_origin=None) -> bool:
        '''
        Populate object with random data

        Argument:
            name_origin (str), optional:
                if provided, must be one of ISO-3166 and ISO-639, as in pt_BR
                if not provided, one of most common languages will be used
                to list available codes, use Person.create_languages()
        '''
        api = 'https://api.namefake.com/'

        try:
            if not name_origin:
                raise RuntimeWarning
            if name_origin not in countries.languages:
                raise KeyError('I don\'t have {name_origin!r} as an API language. ')
        except Exception as e:
                name_origin = random.choice(('es_ES', 'en_GB', 'pt_PT', 'fr_FR'))
                print(f'# INFO: {e}Using language: {name_origin!r}.')

        try:
            res = requests.get(f'https://api.namefake.com/{countries.languages[name_origin]}/')
            data = json.loads(res.text)

            self.full_name = re.sub('(Dra?|Profa?)\.? ', '', data['name'])
            self.birth_date = data['birth_data']
            self.name_origin = name_origin

            return True

        except Exception as e:
            print(f'# ERROR: {e}')
            return False

    @staticmethod
    def create_languages() -> list:
        '''
        List available languages when automatically populating Person object
        '''
        return sorted(countries.languages.keys())

    def info(self) -> dict:
        '''
        Return a dictionary with Person information
        '''
        return { 'full_name': self.full_name, 'birth_date': self.birth_date, 'name_origin': self.name_origin }

