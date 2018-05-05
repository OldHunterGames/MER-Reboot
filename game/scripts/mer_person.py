# -*- coding: UTF-8 -*-
import random
import renpy.store as store
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
    def gen_person(gender=None):
        if gender is None:
            gender = random.choice(store.person_genders)
        name = PersonCreator.get_name(gender)
        return CorePerson(name, gender)


class CorePerson(object):


    def __init__(self, firstname, gender):

        self._firstname = firstname
        self.gender = gender
        self._avatar = None
        self._renpy_character = store.Character(firstname)
        self._host = list()
        self._sparks = 0
        self._successors = list()

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
