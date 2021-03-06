#! /usr/bin/env python3
'''
This module provides access to the Person class

Usage:
    p1 = Person(full_name='Lara Gaspar', subscriber_origin='pt_BR')
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
from requests.exceptions import HTTPError
from . import countries

# Assure logs dir for this module
import os
log_dir = 'logs'
os.makedirs(log_dir, mode=0o777, exist_ok=True)

# Activate logs for this module
import logging as _log
log_level = 'DEBUG'
log_file = 'Person.log'

# logging hack in case of windows
_datefmt = '%Y%m%dT%H%M%S' if os.name == 'nt' else '%s'

# Set log level and path in config
log_file = os.path.join(log_dir, log_file)
_log.basicConfig(level=log_level, filename=log_file, datefmt=_datefmt,
                 format='%(asctime)s:%(process)d:%(levelname)s:%(message)s')


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
    def __init__(self, **kwargs):
        self.id = f'{md5(str(_dt.datetime.now()).encode("utf-8")).hexdigest()}{id(self)}'
        self.full_name = kwargs.get('full_name') if kwargs.get('full_name') else None
        self.birth_date = kwargs.get('birth_date') if kwargs.get('birth_date') else None
        self.name_origin = kwargs.get('name_origin') if kwargs.get('name_origin') else None

        _log.info(f'Person initiated with ID: {self.id}')
        _log.debug(f'Person initiated with name: {self.full_name}')

    def create(self, name_origin=None):
        '''
        Populate object with random data

        Argument:
            name_origin (str), optional:
                if provided, must be one of ISO-3166 and ISO-639, as in `pt_BR`
                if not provided, one of es_ES, en_GB, pt_PT or fr_FR will be used
        '''
        _log.info(f'Person.create() called to populate object')
        api = 'https://api.namefake.com/'

        try:
            if not name_origin:
                raise RuntimeWarning
            if name_origin not in countries.languages:
                raise KeyError(f'I don\'t have {name_origin!r} as an API language. ')
        except Exception as e:
                name_origin = random.choice(('es_ES', 'en_GB', 'pt_PT', 'fr_FR'))
                _log.info('{0}Using language: {1!r}.'.format(str(e).strip('"'), name_origin))

        res = None
        try:
            url = f'https://api.namefake.com/{countries.languages[name_origin]}/'
            _log.debug(f'API request to {url}')
            res = requests.get(url, timeout=10)

        except Exception as e:
            if 'timeout' in str(e).lower():
                _log.warning('API request TIMEOUT error.')
            else:
                _log.error('API request error:', e)

        if res:
            try:
                status_code = res.status_code
                _log.info(f'API status code: {res.status_code}')

                if status_code != 200:
                    raise ValueError(f'API status code: {status_code}')

                data = json.loads(res.text)

                if len(data["name"]) < 5:
                    raise ValueError(f'API did not return a person name')

                _log.debug(f'namefake.com person\'s name: {data["name"]}')
                _log.debug(f'namefake.com person\'s uuid: {data["uuid"]}')
                _log.info(f'namefake.com person\'s URL: {data["url"]}')

                self.full_name = re.sub('^(\w+)a?\. ', '', data['name'])
                self.birth_date = data['birth_data']
                self.name_origin = name_origin

            except Exception as e:
                _log.error(e)

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

    def csv(self) -> str:
        '''
        Return a csv string with Person object data
        '''
        return f'{self.id},"{self.full_name}",{self.birth_date},{self.name_origin}'.replace('None', '').replace('""', '')

