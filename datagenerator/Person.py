#! /usr/bin/env python3
'''
This module provides access to the Person class

Usage:
    p1 = Person(full_name='Lara Gaspar', name_origin='pt_BR')
    p1.name_origin = 'pt_PT'
    p1.info()

    p2 = Person('Núria Borges', '1994-04-27')
    p2.info()

    p3 = Person()
    p3.create('de_DE') # Auto create a German Person
    p3.info()
'''
from hashlib import md5
import datetime as _dt
import random
import requests
import json
import re
from . import countries


class Person:
    '''
    The Person object can be initialised empty or with arguments
    An ID will be automatically set to the object

    Arguments:
        full_name (str), optional: recommended to have two or more words
        birth_date (str), optional: recommended to follow YYYY-MM-DD format
        name_origin (str), optional: follow ISOs 3166 and 639, as in `pt_BR`

    Attributes:
        id (str): unique generated ID

        full_name (str),
        birth_date (str),
        name_origin (str):
            may be filled manually or via create()
    '''
    def __init__(self, full_name=None, birth_date=None, name_origin=None):
        self.id = f'{md5(str(_dt.datetime.now()).encode("utf-8")).hexdigest()}{id(self)}'
        self.full_name = full_name
        self.birth_date = birth_date
        self.name_origin = name_origin

    def create(self, name_origin=None):
        '''
        Populate object with random data

        Argument:
            name_origin (str), optional:
                if provided, must be one of ISO-3166 and ISO-639, as in `pt_BR`
                if not provided, one of es_ES, en_GB, pt_PT or fr_FR will be used
        '''
        api = 'https://api.namefake.com/'

        try:
            if not name_origin:
                raise RuntimeWarning
            if name_origin not in countries.languages:
                raise KeyError(f'I don\'t have {name_origin!r} as an API language. ')
        except Exception as e:
                name_origin = random.choice(('es_ES', 'en_GB', 'pt_PT', 'fr_FR'))
                print('# INFO: {0}Using language: {1!r}.'.format(str(e).strip('"'), name_origin))

        try:
            res = requests.get(f'https://api.namefake.com/{countries.languages[name_origin]}/')
            data = json.loads(res.text)

            self.full_name = re.sub('(Dr|Sr|Prof)a?\.? ', '', data['name'])
            self.birth_date = data['birth_data']
            self.name_origin = name_origin

        except Exception as e:
            print(f'# ERROR: {e}')

    @staticmethod
    def create_languages() -> list:
        '''
        List available languages to use as argument in create()
        '''
        return sorted(countries.languages.keys())

    def info(self) -> dict:
        '''
        Return a dictionary with Person object data
        '''
        return { 'id': self.id, 'full_name': self.full_name, 'birth_date': self.birth_date, 'name_origin': self.name_origin }

