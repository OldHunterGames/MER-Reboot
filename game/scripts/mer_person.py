# -*- coding: UTF-8 -*-
import random
import renpy.store as store
import renpy.exports as renpy
import copy

from mer_utilities import default_avatar, weighted_random, encolor_text
from mer_relations import Relations
from mer_class import PersonClassCard


class CoreFeature(object):
    
    FEATURES = dict()

    def __init__(self, id, data):
        self.id = id
        self._data = data
    
    @property
    def slot(self):
        return self._data.get('slot')
    
    @property
    def attribute(self):
        return self._data.get('attribute')
    
    @property
    def prerequisites(self):
        return self._data.get('prerequisites', [])
    
    def get(self, key, default=None):
        return self._data.get(key, default)

    @property
    def cards(self):
        return [PersonClassCard.get_card(i) for i in self._data.get('cards', [])]
    
    def get_cards(self, case, get_suport=False):
        if case == 'all':
            cards = [i for i in self.cards]
        else:
            if get_suport:
                cards = [i for i in self.cards if (i.case == case or i.case == 'universal') and i.type == 'support']
            else:
                cards = [i for i in self.cards if (i.case == case or i.case == 'universal') and i.type != 'support']
        return cards
    
    @property
    def market_description(self):
        return self._data.get('market_description', 'No description %s' % self.id)
    
    def description(self, person):
        return self._data.get(person.gender, {}).get('description', 'No description')

    def name(self, person):
        return self._data.get(person.gender, {}).get('name', 'No description')
    
    def count_modifiers(self, attr):
        return self._data.get(attr, 0)

    @classmethod
    def register_feature(cls, id, feature):
        cls.FEATURES[id] = feature
    
    @classmethod
    def get_feature(cls, id):
        return cls.FEATURES[id]
    
    @classmethod
    def get_by_slot(cls, slot):
        features = list()
        for value in cls.FEATURES.values():
            if value.slot == slot:
                features.append(value)
        return features
    
    @classmethod
    def random_by_slot(cls, slot, weighted=False):
        try:
            feature = random.choice(cls.get_by_slot(slot))
        except IndexError:
            print(slot)
            raise
        else:
            return feature


class PersonCreator(object):

    AGE_SLOTS = {
        # 'junior': 1,
        'elder': 2,
        'adolescent': 3,
        'mature': 4,
    }

    ALIGNMENT_SLOTS = [
        'nutrition',
        'authority',
        'comfort',
        'communication',
        'eros',
        'ambition',
        'prosperity',
        'safety',
    ]

    PHYSICAL_SLOTS = [
        'height',
        'constitution',
        'voice',
        'eyes',
        'smile',
        'skin',
    ]
    
    BACKGROUND_SLOTS = [
        'homeworld',
    ]

    GENDER_SLOTS = {
        'male': [
            'dick',
        ],
        'female': [
            'boobs',
        ],
        'shemale': [
            'boobs',
            'dick',
        ]
    }

    MASCULINE_SLOTS = [
        'dick', 
    ]

    FEMINIE_SLOTS = [
        'boobs',
    ]


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

    @classmethod
    def gen_person(cls, **kwargs):
        gender = kwargs.get('gender')
        genus = kwargs.get('genus')
        genus_preset = kwargs.get('genus_preset')
        if genus_preset is None and genus is None:
            # raise Exception('No genus or genus preset provided for get_person')
            genus_preset = store.serpsis_genus_preset
        if gender is None:
            gender = CoreFeature.random_by_slot('gender')
        else:
            gender = CoreFeature.get_feature(gender)
        if genus is None:
            genus_id = weighted_random(genus_preset)
            genus = CoreFeature.get_feature(genus_id)
        else:
            genus = CoreFeature.get_feature(genus)

        name = kwargs.get('name', PersonCreator.get_name(gender.id))
        person = CorePerson(name, gender, genus)
        for i in cls.make_features():
            person.add_feature(i)
        keys = store.new_features.keys()
        random.shuffle(keys)
        level = person.soul_level - 1
        for key in keys:
            if level < 1:
                break
            feature = store.new_features[key]
            if feature.get('limitations') is None:
                person.add_feature(CoreFeature(key, feature))
            else:
                limitations = feature.get('limitations')
                if limitations['gender'] == person.gender:
                    person.add_feature(CoreFeature(key, feature))
        # for i in cls.make_features():
        #     person.add_feature(i)
        # for i in cls.gender_features(gender.id):
        #     person.add_feature(i)

        cls.gen_background(person)
        person.set_avatar(PersonCreator.gen_avatar(gender.id, genus.id))
        return person

    @classmethod
    def gen_background(cls, person):
        soul = person.soul_level
        features = CoreFeature.get_by_slot('background')
        person_features_id = [i.id for i in person.get_features()]
        available_features = []
        world = person.feature_by_slot('homeworld')
        available_classes_by_world = world.get('backgrounds', [])
        for feat in features:
            if len(feat.prerequisites) < 1 and feat.get('tier', 0) == person.soul_level:
                available_features.append(feat)
            else:
                if all([i in person_features_id for i in feat.prerequisites]) and feat.get('tier', 0) == person.soul_level:
                    available_features.append(feat)
        if len(available_features) < 1:
            feats = [i.id for i in person.get_features()]
            raise Exception(
                """
                Failed to generate background for person.
                Soul level: %s.
                Features: %s.
                World: %s.
                Failed to find features by prerequisites and soul level.
                """ % (soul, feats, world.id)
            )
        available_by_world = [i for i in available_features if i.id in available_classes_by_world]
        try:
            person.add_feature(random.choice(available_by_world))
        except IndexError:
            feats = [i.id for i in person.get_features()]
            raise Exception(
                """
                Failed to generate background for person.
                Soul level: %s.
                Person Features: %s.
                World: %s.
                Features available for person prerequisites and soul level
                are not available for this world
                Features found: %s.
                Features available for world: %s.
                """ % (soul, feats, world.id, [i.id for i in available_features], available_classes_by_world)
            )

    @classmethod
    def gender_features(cls, gender):
        return [CoreFeature.random_by_slot(slot) for slot in cls.GENDER_SLOTS[gender]]

    @staticmethod
    def appearance_type(gender):
        return {'male': 'masculine', 'female': 'feminine'}[gender]

    @staticmethod
    def gen_avatar(gender, genus):
        start_path = 'images/avatar/' + genus
        # TODO: Generate cultures instead of hardcode
        cultures = ['african', 'arabic', 'native', 'nordic', 'oriental', 'slavic', 'western']
        start_path = PersonCreator._check_avatar(start_path, PersonCreator.appearance_type(gender))
        start_path = PersonCreator._check_avatar(start_path, random.choice(cultures))
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

    @classmethod
    def make_alignments(cls):
        slots = [i for i in cls.ALIGNMENT_SLOTS]
        chances = [1 for i in range(5)]
        chances.append(0)
        random.shuffle(chances)
        features = list()
        for i in chances:
            if i == 0:
                break
            slot = random.choice(slots)
            slots.remove(slot)
            feature = CoreFeature.random_by_slot(slot)
            features.append(feature)
        return features
    
    @classmethod
    def make_physical(cls):
        slots = [i for i in cls.PHYSICAL_SLOTS]
        chances = [1 for i in range(5)]
        chances.append(0)
        random.shuffle(chances)
        features = list()
        for i in chances:
            if i == 0:
                break
            slot = random.choice(slots)
            slots.remove(slot)
            feature = CoreFeature.random_by_slot(slot)
            features.append(feature)
        return features

    @classmethod
    def make_background(cls):
        slots = [i for i in cls.BACKGROUND_SLOTS]
        features = list()
        for slot in slots:
            features.append(CoreFeature.random_by_slot(slot))
        return features

    @classmethod
    def make_features(cls):
        features = []
        features.append(CoreFeature.random_by_slot('temper'))
        # features = cls.make_alignments()
        # features.extend(cls.make_physical())
        features.extend(cls.make_background())
        return features


class CorePerson(object):

    def __str__(self):
        return 'person: %s' % self.name

    def __init__(self, firstname, gender, genus):

        self._firstname = firstname
        self.genus = genus
        self._avatar = None
        self._renpy_character = store.Character(firstname)
        self._host = list()
        self._sparks = 100
        self._successors = list()
        self.features = dict()
        self.slotless_features = list()
        self.add_feature(gender)
        self.player_relations = Relations()
        self.soul_level = weighted_random(store.core_soul_weights)
        self.person_class = None
        self.grove = False
        self.exhausted = False
        self.temporary_cards = {
            'support': None,
            'love': None,
            'fellowship': None,
            'sabotage': None,
        }
        self.relations = {} # temp, will be removed
    
    def add_relation(self, relation, person):
        self.relations[relation] = person

    def get_relation(self, relation):
        return self.relations.get(relation)

    def get_cards(self, case, get_support=False, get_temporary=True, special_filter=None):
        cards = self.person_class.get_cards(case, get_support)
        # background = self.feature_by_slot('background')
        # cards.extend(background.get_cards(case, get_support))
        if special_filter is not None:
            cards = [i for i in cards if special_filter(i)]
        if get_support:
            for i in cards:
                i.giver = self
            return cards
        if len(cards) < 1:
            if case == 'combat' or case == 'all':
                cards.append(PersonClassCard.get_card('struggle'))
            if case == 'social' or case == 'all':
                attr = self.max_attribute()
                if self.soul_level > self.attribute(attr):
                    attr = 'soul'
                cards.append(self.person_class.card_for_empty_hand(attr))
        if self.grove and get_temporary:
            cards.append(PersonClassCard.get_card('lucky'))
        if get_temporary:
            for key, card in self.temporary_cards.items():
                if card is not None and key != 'sabotage':
                    cards.append(card)
        return cards

    def get_sabotage(self):
        return self.temporary_cards['sabotage']

    def set_temporary_card(self, card, type):
        self.temporary_cards[type] = card

    def after_fight(self):
        self.grove = False
        for key in self.temporary_cards:
            self.temporary_cards[key] = None
    
    def calc_influence(self, influence):
        value = 2
        if self.has_feature(influence.positive_connection()):
            value += 1
        if self.has_feature(influence.negative_connection()):
            value -= 1
        return value

    def player_influence(self):
        influence = self.player_relations.get_influence()
        value = 0
        for i in influence:
            value += self.calc_influence(i)
        return value

    def player_relations_sum(self):
        return self.player_influence() - self.player_relations.tension()

    def get_last_influence(self):
        value = 0
        influence = None
        for i in self.player_relations.get_influence():
            if self.calc_influence(i) >= value:
                value = self.calc_influence(i)
                influence = i
        return influence

    def player_relations_nature(self):
        if self.player_relations.tension() == 0 and self.player_influence() == 0:
            return 2
        if self.player_relations_sum() <= 0:
            if self.player_influence() == 0:
                return 1
            else:
                return 0
    
    def show_player_relations_nature(self):
        if self.player_relations_nature() == 0:
            return self.get_last_influence().conflict
        elif self.player_relations_nature() == 5:
            return self.get_last_influence().harmony
        return 


    @property
    def gender(self):
        return self.features['gender'].id

    def attribute(self, attr):
        return max(-2, min(5, self.get_attribute_value(attr)))

    def max_attribute(self):
        return max(self.attributes().keys(), key=lambda x: self.attributes()[x])
    
    def count_modifiers(self, attr, skip_slots=None):
        if skip_slots is None:
            skip_slots = []
        value = 0
        for i in self.features.values():
            if i.slot not in skip_slots:
                value += i.count_modifiers(attr)
        for i in self.slotless_features:
            value += i.count_modifiers(attr)
        return value
    
    def get_attribute_value(self, attr):
        background = self.feature_by_slot('background')
        if attr in background.get('high_attributes', []):
            attribute = self.genus.get(attr, (0, 0))[1]
            attribute += self.count_modifiers(attr, ['background', 'genus'])
            return attribute
        elif attr in background.get('low_attributes', []):
            return -1
        else:
            return self.genus.get(attr, (0, 0))[0]

    def attributes(self):
        attrs = dict()
        for key in store.core_attributes.keys():
            attrs[key] = self.attribute(key)
        return attrs
    
    def show_attributes(self):
        attrs = dict()
        for key, value in store.core_attributes.items():
            attr = self.attribute(key)
            if attr < -1:
                attrs[value['name']] = encolor_text(value['low'], 'red')
            elif attr > 0:
                attrs[value['name']] = encolor_text(value['high'], attr)
        return attrs

    def add_feature(self, feature):
        if feature.slot is None:
            self.slotless_features.append(feature)
            return
        self.features[feature.slot] = feature
    
    def remove_feature(self, feature):
        if feature.slot is None:
            self.slotless_features.remove(feature)
        else:
            del self.features[feature.slot]

    def get_features(self):
        features = self.features.values()
        features.extend(self.slotless_features)
        return features
    
    def feature_by_slot(self, slot):
        return self.features.get(slot)
    
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

    @property
    def name(self):
        return self.firstname

    def _set_renpy_char_name(self):
        self._renpy_character.name = self.firstname

    def __call__(self, what, interact=True):
        store.sayer = self
        self._renpy_character(what, interact=interact)
        store.sayer = None

    def say_phrase(self, phrase_id, default_value='No phrase'):
        phrase = self.get_phrase(phrase_id, default_value)
        self(phrase)

    def say(self, what):
        renpy.call_screen('sc_dialog', who=self, what=what)

    def predict(self, what):
        self._renpy_character.predict(what)


class PersonWrapper(object):

    def __init__(self, coreperson, *args, **kwargs):
        self._wrapped_person = coreperson

    def attribute(self, attr):
        return self.count_modifiers(attr)
    
    def count_modifiers(self, attr):
        return self._wrapped_person.count_modifiers(attr)
    
    def attributes(self):
        return self._wrapped_person.attributes()
    
    def show_attributes(self):
        return self._wrapped_person.show_attributes()
    
    @property
    def avatar(self):
        return self._wrapped_person.avatar
    
    def __call__(self, *args, **kwargs):
        return self._wrapped_person.__call__(*args, **kwargs)
    
    def predict(self, *args, **kwargs):
        return self._wrapped_person.predict(*args, **kwargs)
    
    @property
    def name(self):
        return self._wrapped_person.firstname
    
    @property
    def gender(self):
        return self._wrapped_person.gender