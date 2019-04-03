import random

import renpy.store as store
import renpy.exports as renpy


class Suits(object):
    DIAMONDS = 'diamonds'
    SPADES = 'spades'
    CLUBS = 'clubs'
    HEARTS = 'hearts'
    JOKER = 'joker'
    SKULL = 'skull'

    @classmethod
    def as_attribute(cls, suit):
        return {
            cls.DIAMONDS: 'might',
            cls.SPADES: 'subtlety',
            cls.CLUBS: 'knowledge',
            cls.HEARTS: 'charisma',
        }.get(suit)

    @classmethod
    def as_attack_type(cls, suit):
        return {
            cls.DIAMONDS: 'heavy',
            cls.SPADES: 'swift',
            cls.CLUBS: 'accurate',
            cls.HEARTS: 'impactful',
            cls.SKULL: 'unarmed',
        }.get(suit)

results = {
    Suits.DIAMONDS: lambda _: 0,
    Suits.JOKER: lambda _: 1,
    Suits.SKULL: lambda _: -1,
    Suits.SPADES: lambda suit: 1 if suit == Suits.HEARTS else 0,
    Suits.CLUBS: lambda suit: 1 if suit == Suits.SPADES else 0,
    Suits.HEARTS: lambda suit: 1 if suit == Suits.CLUBS else 0
}

def suits_value(suit1, suit2):
    return [results[suit1](suit2), results[suit2](suit1)]


class Armor(object):

    @classmethod
    def get_by_type(cls, type):
        return [cls(id, data) for id, data in store.mer_armor.items() if data['type'] == type or data['type'] is None]

    @classmethod
    def random_by_type(cls, type):
        return random.choice(cls.get_by_type(type))

    def __init__(self, id, data):
        self.id = id
        self.data = data

    @property
    def name(self):
        return self.data.get("name")

    def calc_bonus(self, context):
        return self.data.get('calc_bonus', lambda x: 0)(context)
