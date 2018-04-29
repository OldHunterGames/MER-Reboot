# -*- coding: UTF-8 -*-
import renpy.store as store
from mer_utilities import default_avatar


class CorePerson(object):


    def __init__(self, firstname):

        self._firstname = firstname
        self._avatar = None
        self._renpy_character = store.Character(firstname)

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