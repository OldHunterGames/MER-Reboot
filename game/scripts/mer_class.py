import random

import renpy.store as store
import renpy.exports as renpy

from mer_basics import Suits
from mer_utilities import encolor_text, min_max
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

    _available_classes = {}

    @classmethod
    def card_for_empty_hand(cls, card):
        id = {
            'soul': 'wisdom_of_many_lives',
            'might': 'stubborn',
            'subtlety': 'slippery_words',
            'knowledge': 'common_sense',
            'charisma': 'natural_charm'
        }.get(card)
        return PersonClassCard.get_card(id)

    @classmethod
    def register_class(cls, id, data):
        cls._available_classes[id] = cls(id, data)

    @staticmethod
    def get_by_id(id):
        return PersonClass._available_classes[id]

    @staticmethod
    def get_by_ids(ids):
        return [i for i in PersonClass.get_all() if i.id in ids]

    @staticmethod
    def get_by_tier(tier):
        return [i for i in PersonClass.get_all() if i.tier == tier]

    @staticmethod
    def random_by_tag(tag):
        return random.choice(PersonClass.get_by_tag(tag))

    @staticmethod
    def get_by_tag(tag):
        return [item for item in PersonClass.get_all() if item.tag == tag]

    @staticmethod
    def get_all():
        return PersonClass._available_classes.values()

    @staticmethod
    def available_upgrades(person):
        return [i for i in PersonClass.pipe_filters(
            PersonClass.class_filter,
            PersonClass.gender_filter,
            PersonClass.type_filter,
            PersonClass.tier_filter
        )(person, PersonClass.get_all()) if i.id != person.person_class.id and i.type == person.person_class.type]

    @staticmethod
    def pipe_filters(*filters):
        def inner(person, items):
            if len(filters) < 1:
                return items
            return filter(lambda item: all([f(person, item) for f in filters]), items)
        return inner

    @staticmethod
    def tier_filter(person, new_class):
        if not hasattr(person, 'person_class'):
            return True
        tier_req = person.person_class.tier + 1
        return new_class.tier == tier_req

    @staticmethod
    def class_filter(person, new_class):
        if not hasattr(person, 'person_class'):
            return True
        class_req = new_class.requirements.get('class')
        if class_req is None:
            return True
        return person.person_class.id in class_req

    @staticmethod
    def type_filter(person, new_class):
        if not hasattr(person, 'person_class'):
            return True
        type_req = new_class.requirements.get('type')
        if type_req is None:
            return True
        return type_req == person.person_class.type

    @staticmethod
    def gender_filter(person, new_class):
        if not hasattr(person, 'gender'):
            return True
        needed_gender = person.gender
        gender = new_class.requirements.get('gender')
        
        if gender is None:
            return True
        elif needed_gender == gender:
            return True
        elif 'not' in gender and needed_gender != gender.split(' ')[1]:
            return True

        return False

    def __init__(self, id, data):
        self.id = id
        self.tier = data.get('tier', 0)
        self.name = data['name']
        self.key_attributes = data.get('key_attributes', [])
        self.type = data['type']
        self._attack_suits = data.get('attack_suits', [])
        self._attack_types = data.get('attack_types', [])
        self._available_garments = data.get('available_garments', [])
        self.tag = data.get('tag')
        self.requirements = data.get('prerequisites', {})
        self.cost = data.get('cost', 0)
        self.cards = [PersonClassCard.get_card(i) for i in data.get('cards', [])]
        self._prototype = data.get('prototype')

    @property
    def prototype(self):
        if self._prototype is not None:
            return PersonClass.get_by_id(self._prototype)
        return self._prototype
    
    def get_cards(self, case):
        if case == 'all':
            cards = [i for i in self.cards]
        else:
            cards = [i for i in self.cards if i.type == case or i.type is None]
        if self.prototype is not None:
            cards.extend(self.prototype.get_cards(case))
        return cards

    def colored_name(self):
        return encolor_text(self.name, self.tier)

    @property
    def attack_suits(self):
        return self._attack_suits + [Suits.SKULL]

    @property
    def attack_types(self):
        return self._attack_types if len(self._attack_types) > 0 else [AttackTypes.MELEE]

    @property
    def available_garments(self):
        return self._available_garments + [GarmentsTypes.NUDE]


class PersonClassCard(object):
    @classmethod
    def get_card(cls, id):
        return cls(id, store.person_cards_data[id])

    def __init__(self, id, data):
        self.data = data
        self.id = id

    @property
    def type(self):
        return self.data.get('type')

    def suit(self, user, context):
        suit = self.data.get('suit', Suits.SKULL)
        try:
            suit = suit(user, context)
        except TypeError:
            pass
        return suit

    @property
    def name(self):
        return self.data.get('name', 'No name')
    
    @property
    def attribute(self):
        return self.data.get('attribute')

    @property
    def value(self):
        return self.data.get('value', 0)
    
    @property
    def custom(self):
        return self.data.get('custom')

    @min_max(0, 5)
    def get_power(self, user, context):
        if self.custom is not None:
            return self.custom(user, context)

        if self.attribute is not None:
            return user.attribute(self.attribute)

        return self.value

    def description(self, user, context):
        return '{name}({suit})'.format(name=self.name, suit=self.suit(user, context))


class MerArena(object):

    def __init__(self, fighter1, fighter2, sparks=0):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.state = 'selection'
        self.ally = None
        self.enemy = None
        self.fight = None
        self.sparks = sparks

    def start(self):
        return renpy.call_screen('sc_arena', arena=self)

    def make_bet(self, fighter):
        self.ally = fighter
        self.enemy = self.fighter1 if fighter == self.fighter2 else self.fighter2
        self.state = 'prefight'
        self.fight = Standoff(self.ally, self.enemy)

    def end(self):
        self.state = 'results'
        


class MerArenaMaker(object):

    def __init__(self, maker_func, min_player_level=0, allowed_classes=None, fixed_enemy=None, sparks=0, die_after_fight=True):
        self.min_player_level = min_player_level
        self.allowed_classes = None if allowed_classes is None else [i for i in allowed_classes]
        self.fixed_enemy = fixed_enemy
        self.maker_func = maker_func
        self.sparks = sparks
        self.current_enemy = self.make_gladiator()
        self.is_winned = False
        self.die_after_fight = die_after_fight

    def is_active(self, player):
        return player.person_class.tier >= self.min_player_level
            
    def can_put_fighter(self, player):
        return len(self.filter_fighters(player)) > 0

    def filter_fighters(self, player):
        glads = [i for i in player.slaves]
        glads.append(player)
        glads = [i for i in glads if not i.exhausted]
        if self.allowed_classes is None:
            return glads
        return [i for i in glads if i.person_class in self.allowed_classes]

    def make_gladiator(self):
        if self.fixed_enemy is not None:
            allowed_classes = self.fixed_enemy
        else:
            allowed_classes = self.allowed_classes
        return self.maker_func(allowed_classes)

    def set_gladiator(self, *args, **kwargs):
        self.current_enemy = self.make_gladiator()

