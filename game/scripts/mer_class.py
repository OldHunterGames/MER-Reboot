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
    def get_by_tier(tier, items=None):
        if items is not None:
            return [i for i in items in i.tier == tier]
        return [i for i in PersonClass.get_all() if i.tier == tier]

    @staticmethod
    def random_by_tag(tag):
        return random.choice(PersonClass.get_by_tag(tag))

    @staticmethod
    def get_by_tag(tag, items=None):
        if items is not None:
            return [i for i in items if i.tag == tag]
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
        if getattr(person, 'person_class', None) is None:
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
        self._data = data
        self.id = id
        self.tier = data.get('tier', 0)
        self.name = data['name']
        self.key_attributes = data.get('key_attributes', [])
        self.type = data['type']
        self._available_garments = data.get('available_garments', [])
        self.tag = data.get('tag')
        self.requirements = data.get('prerequisites', {})
        self.cost = data.get('cost', 0)
        self._prototype = data.get('prototype')
    
    @property
    def cards(self):
        return [PersonClassCard.get_card(i) for i in self._data.get('cards', [])]

    @property
    def prototype(self):
        if self._prototype is not None:
            return PersonClass.get_by_id(self._prototype)
        return self._prototype
    
    def get_cards(self, case, get_suport=False):
        if case == 'all':
            cards = [i for i in self.cards]
        else:
            if get_suport:
                cards = [i for i in self.cards if (i.case == case or i.case is None) and i.type == 'support']
            else:
                cards = [i for i in self.cards if (i.case == case or i.case is None) and i.type != 'support']
        if self.prototype is not None:
            cards.extend(self.prototype.get_cards(case, get_suport))
        return cards

    def colored_name(self):
        return encolor_text(self.name, self.tier)

    @property
    def available_garments(self):
        return self._available_garments + [GarmentsTypes.NUDE]
    
    def __str__(self):
        return '{} {}'.format(self.name, self.tier)


class PersonClassCard(object):
    @classmethod
    def get_card(cls, id, giver=None):
        return cls(id, store.person_cards_data[id], giver)

    def __init__(self, id, data, giver=None):
        self.data = data
        self.id = id
        self.giver = giver
    
    def __str__(self):
        return self.id
    
    @property
    def permanent_context(self):
        return {'giver': self.giver}

    @property
    def type(self):
        return self.data.get('type')
    
    @property
    def case(self):
        return self.data.get('case')

    def suit(self, user, context=None):
        if context is None:
            context = {}
        context = self.permanent_context.update(context)
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
    def get_power(self, user, context=None):
        if context is None:
            context = {}
        context = self.permanent_context.update(context)
        if self.custom is not None:
            return self.custom(user, context)

        if self.attribute is not None:
            if self.giver:
                return self.giver.attribute(self.attribute)
            return user.attribute(self.attribute)

        return self.value

    def description(self, user, context):
        return '{name}({suit})'.format(name=self.name, suit=self.suit(user, context))


class MerArena(object):

    def __init__(self, fighter1, fighter2, sparks=0, cards_filter=None):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.state = 'selection'
        self.ally = None
        self.enemy = None
        self.fight = None
        self.sparks = sparks
        self.cards_filter = cards_filter

    def start(self):
        return renpy.call_screen('sc_arena', arena=self)

    def make_bet(self, fighter):
        self.ally = fighter
        self.enemy = self.fighter1 if fighter == self.fighter2 else self.fighter2
        self.state = 'prefight'
        self.fight = Standoff(self.ally, self.enemy, self.cards_filter)

    def end(self):
        self.state = 'results'
    
    def raise_fame(self, calculator, player):
        fight = self.fight
        player_price = calculator(fight.player_combatant)
        enemy_price = calculator(fight.enemy)
        
        if fight.is_player_win():
            if player_price.training_price() < enemy_price.entertainment_raiting_formula():
                new_classes = player.person_class.available_upgrades(player)
                if len(new_classes) > 0:
                    player.person_class = random.choice(new_classes)
                return True
        # self.drop_fame(calculator, player)
        return False
    
    def drop_fame(self, calculator, player):
        fight = self.fight
        if calculator(fight.winner).training_price() > calculator(fight.loser).entertainment_raiting_formula():
            if player.person_class.prototype is not None:
                player.person_class = player.person_class.prototype
            return True
        return False


class MerArenaMaker(object):

    def __init__(self, maker_func, allowed_checker, sparks_calculator, min_player_level=0, die_after_fight=True, cards_filter=None, can_skip_enemy=False, gain_prestige=True):
        self.min_player_level = min_player_level
        self.maker_func = maker_func
        self.allowed_checker = allowed_checker
        self.sparks_calculator = sparks_calculator
        self.current_enemy = self.make_gladiator()
        self.is_winned = False
        self.die_after_fight = die_after_fight
        self.cards_filter = cards_filter
        self.can_skip_enemy = can_skip_enemy
        self.gain_prestige = gain_prestige
        self.team = []

    def is_active(self, player):
        return player.person_class.tier >= self.min_player_level and self.can_put_fighter(player)
            
    def can_put_fighter(self, player):
        return len(self.filter_fighters(player)) > 0

    def filter_fighters(self, player):
        glads = [i for i in player.slaves]
        glads = [i for i in glads if not i.exhausted]

        return [i for i in glads if self.allowed_checker(i)]

    def make_gladiator(self):
        return self.maker_func()

    def set_gladiator(self, *args, **kwargs):
        self.current_enemy = self.make_gladiator()
    
    def get_prize(self, arena):
        return self.sparks_calculator(arena)

