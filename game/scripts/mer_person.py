# -*- coding: UTF-8 -*-
import random
import renpy.store as store
import renpy.exports as renpy
from mer_utilities import default_avatar


class PersonCreator(object):

    @staticmethod
    def names_data():
        return store.person_names

    @staticmethod
    def get_name(gender):
        data = PersonCreator.names_data()
        names = data.get(gender, data.get('default'))
        if names is None:
            raise Exception('Invalid data')
        return random.choice(names)

    @staticmethod
    def gen_person(**kwargs):
        gender = kwargs.get('gender')
        genus = kwargs.get('genus')
        age = kwargs.get('age')
        # temporary genus is always human
        genus = 'human'
        if gender is None:
            gender = random.choice(store.person_genders)
        if genus is None:
            genus = random.choice(store.person_genuses)
        if age is None:
            age = random.choice(store.person_ages)
        name = kwargs.get('name', PersonCreator.get_name(gender))
        person = CorePerson(name, gender, age, genus)
        person.set_avatar(PersonCreator.gen_avatar(gender, age, genus))
        return person

    @staticmethod
    def appearance_type(gender):
        return {'male': 'masculine', 'female': 'feminine'}[gender]

    @staticmethod
    def gen_avatar(gender, age, genus):
        start_path = 'images/avatar/'
        # TODO: Generate cultures instead of hardcode
        if genus == 'human':
            start_path += genus + '/'
            cultures = ['african', 'arabic', 'native', 'nordic', 'oriental', 'slavic', 'western']
            start_path += random.choice(cultures)
        else:
            start_path += genus
        start_path = PersonCreator._check_avatar(start_path, PersonCreator.appearance_type(gender))
        start_path = PersonCreator._check_avatar(start_path, age)
        try:
            avatar = random.choice(PersonCreator._get_avatars(start_path))
        except IndexError:
            avatar = default_avatar()
        return avatar

    @staticmethod
    def _check_avatar(start_path, attr):
        if attr is not None:
            if renpy.exists(start_path + '/%s' % attr):
                start_path += '/%s' % attr
        return start_path

    @staticmethod
    def _get_avatars(path):
        all_ = renpy.list_files()
        avas = [str_ for str_ in all_ if str_.startswith(path)]
        return avas


class CorePerson(object):


    def __init__(self, firstname, gender, age, genus):

        self._firstname = firstname
        self.gender = gender
        self.age = age
        self.genus = genus
        self._avatar = None
        self._renpy_character = store.Character(firstname)
        self._host = list()
        self._sparks = 100
        self._successors = list()
    
    def income(self):
        return sum([i.produce_sparks() for i in self.get_host()])

    def set_avatar(self, value):
        self._avatar = value

    @property
    def sparks(self):
        return self._sparks

    @sparks.setter
    def sparks(self, value):
        self._sparks = value

    def heir(self):
        try:
            heir = self._successors[0]
        except IndexError:
            heir = None
        return heir

    def add_successor(self, person):
        self._successors.append(person)

    def remove_successor(self, person):
        self._successors.remove(person)

    def successors(self):
        return [i for i in self._successors]

    def is_successor(self, person):
        return person in self._successors

    def add_angel(self, angel):
        self._host.append(angel)

    def remove_angel(self, angel):
        self._host.remove(angel)

    def get_host(self):
        return [i for i in self._host]

    @property
    def avatar(self):
        if self._avatar is None:
            return default_avatar()
        return self._avatar

    @property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, value):
        self._firstname = value
        self._set_renpy_char_name()


    def _set_renpy_char_name(self):
        self._renpy_character.name = self.firstname

    def __call__(self, what, interact=True):
        store.sayer = self
        self._renpy_character(what, interact=interact)
        store.sayer = None

    def say_phrase(self, phrase_id, default_value='No phrase'):
        phrase = self.get_phrase(phrase_id, default_value)
        self(phrase)

    def predict(self, what):
        self._renpy_character.predict(what)
