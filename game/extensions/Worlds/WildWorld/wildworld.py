# -*- coding: UTF-8 -*-
import renpy.store as store
from mer_utilities import encolor_text
import random


class Feature(object):
    
    FEATURES = dict()

    def __init__(self, data):
        self._data = data
    
    @property
    def slot(self):
        return self._data.get('slot')
    
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
    def random_by_slot(cls, slot):
        return random.choice(cls.get_by_slot(slot))

class WildWorldPersonMaker(object):
    
    @classmethod
    def make_person(cls, person=None, person_maker=None):
        if person_maker is not None:
            person = person_maker.gen_person(gender='female')
        gender = Feature.get_feature(person.gender)
        world_person = WildWorldPerson(person)
        world_person.add_feature(gender)
        return world_person

class WildWorldPerson(object):
    

    def __init__(self, coreperson):
        self._wrapped_person = coreperson
        self.features = dict()
        self.slotless_features = list()
    
    def add_feature(self, feature):
        if feature.slot is None:
            self.slotless_features.append(feature)
            return
        self.features[feature.slot] = feature
    
    def attribute(self, attr):
        return self.count_modifiers(attr)
    
    def count_modifiers(self, attr):
        value = 0
        for i in self.features.values():
            value += i.count_modifiers(attr)
        for i in self.slotless_features:
            value += i.count_modifiers(attr)
        return max(-2, min(value, 5))
    
    def show_attributes(self):
        attrs = dict()
        for key, value in store.wildworld_attributes.items():
            attr = self.attribute(key)
            if attr < -1:
                attrs[value['name']] = encolor_text(value['low'], 'red')
            elif attr > 0:
                attrs[value['name']] = encolor_text(value['high'], attr)
        return attrs
    
    @property
    def avatar(self):
        return self._wrapped_person.avatar
    
    def __call__(self, *args, **kwargs):
        return self._wrapped_person.__call__(*args, **kwargs)
    
    def predict(self, *args, **kwargs):
        return self._wrapped_person.predict(*args, **kwargs)
