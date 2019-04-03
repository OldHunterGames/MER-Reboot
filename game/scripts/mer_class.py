import random

import renpy.store as store
import renpy.exports as renpy

from mer_basics import Suits
from mer_utilities import encolor_text
from mer_standoff import Standoff


class PersonClassTypes(object):
    BACKGROUND = 'background'
    SLAVE = 'slave'
    CIVIL = 'civil'


class AttackTypes(object):
    MELEE = 'melee'
    RANGED = 'ranged'
    MAGITECH = 'magitech'


class GarmentsTypes(object):
    NUDE = 'nude'
    CLOTH = 'cloth'
    ATTIRE = 'attire'
    ARMOR = 'armor'
    HEAVY_ARMOR = 'heavy_armor'


class PersonAttack(object):

    def __init__(self, suit, type):
        self.suit = suit
        self.type = type

    def power(self, user):
        return user.attribute({
            'melee': 'might',
            'ranged': 'subtlety',
            'magitech': 'knowledge',
            'unarmed': 'might',
            }[self.type])

    def __str__(self):
        return '{0} {1}'.format(Suits.as_attack_type(self.suit), self.type)

    def colored(self, user):
        return encolor_text(str(self), self.power(user))


class PersonClass(object):

    @staticmethod
    def get_by_id(id):
        return PersonClass(store.mer_class_data['id'])

    @staticmethod
    def random_by_tag(tag):
        return random.choice(PersonClass.get_by_tag(tag))

    @staticmethod
    def get_by_tag(tag):
        return [PersonClass(i) for i in store.mer_class_data.values() if i.get('tag') == tag]

    @staticmethod
    def get_all():
        return [PersonClass(i) for i in store.mer_class_data.values()]

    def __init__(self, data):
        self.tier = data.get('tier', 0)
        self.name = data['name']
        self.key_attributes = data.get('key_attributes', [])
        self.type = data['type']
        self._attack_suits = data.get('attack_suits', [])
        self._attack_types = data.get('attack_types', [])
        self._available_garments = data.get('available_garments', [])
        self.tag = data.get('tag')

    def colored_name(self):
        return encolor_text(self.name, self.tier)

    @property
    def attack_suits(self):
        return self._attack_suits + [Suits.SKULL]

    @property
    def attack_types(self):
        return self._attack_types if len(self._attack_types) > 0 else [AttackTypes.MELEE]

    def get_attacks(self):
        attacks = [PersonAttack(suit, type) for type in self.attack_types for suit in self.attack_suits]
        if len(self.attack_suits) > 1:
            return filter(lambda attack: attack.suit != 'skull', attacks)
        return attacks

    @property
    def available_garments(self):
        return self._available_garments + [GarmentsTypes.NUDE]


class MerArena(object):

    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.state = 'selection'
        self.ally = None
        self.ally_attack = None
        self.enemy = None
        self.fight = None
        self.enemy_attack = None

    def start(self):
        renpy.call_screen('sc_arena', arena=self)

    def make_bet(self, fighter):
        self.ally = fighter
        self.enemy = self.fighter1 if fighter == self.fighter2 else self.fighter2
        self.enemy_attack = random.choice(self.enemy.person_class.get_attacks())
        self.state = 'prefight'

    def select_attack(self, attack):
        self.ally_attack = attack
        self.state = 'results'
        self.fight = Standoff(self.ally, self.ally_attack, self.enemy, self.enemy_attack)
        self.fight.run()