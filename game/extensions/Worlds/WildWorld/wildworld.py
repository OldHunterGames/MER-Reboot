# -*- coding: UTF-8 -*-
import random
from collections import Counter
import renpy.store as store
import renpy.exports as renpy
from mer_utilities import encolor_text


class Location(object):
    
    def __init__(self, data):
        self._data = data
    
    def name(self):
        return self._data.get('name')
    
    def label(self):
        return self._data.get('label')
    
    def visit(self, world):
        renpy.call(self.label(), world=world)


class Locations(object):
    
    def __init__(self, width=5, height=5, **kwargs):
        self._width = 5
        self._height = 5
        self.locations = [None for i in range(width*height)]
        self.current = 0
        self.city_naems = kwargs.get('city_names')
        self._generate_locations()
    
    def size(self):
        return len(self.locations)
    
    def current_location(self):
        return self.get_loc(self.current)
    
    def _generate_locations(self):
        city = 2
        empty_row = False
        for i in range(0, self._height):
            index = i * self._width
            if empty_row:
                self.locations[index] = self.gen_road()
                self.locations[index+1] = self.gen_wildness()
                self.locations[index+2] = self.gen_road()
                self.locations[index+3] = self.gen_wildness()
                self.locations[index+4] = self.gen_road()
                empty_row = False
            else:
                if city == 2:
                    self.locations[index] = self.gen_city()
                    self.locations[index+1] = self.gen_road()
                    self.locations[index+2] = self.gen_wildness()
                    self.locations[index+3] = self.gen_road()
                    self.locations[index+4] = self.gen_city()
                    city = 1
                    empty_row = True
                elif city == 1:
                    self.locations[index] = self.gen_road()
                    self.locations[index+1] = self.gen_wildness()
                    self.locations[index+2] = self.gen_city()
                    self.locations[index+3] = self.gen_road()
                    self.locations[index+4] = self.gen_wildness()
                    city = 2
                    empty_row = True
            
                
    
    def get_loc(self, index):
        return self.locations[index]

    def _can_go(self, index, side):
        sides = {
            'left': range(0, self.size(), self._width),
            'right': range(self._width - 1, self.size(), self._width),
            'top': range(0, self._width),
            'bot': range(self.size()-1, self.size()-self._width-1, -1)
        }
        return index not in sides[side]
    
    def can_go(self, location_pos, turns=1):
        available = {1: list()}
        locs = {
            'top': location_pos - 5,
            'bot': location_pos + 5,
            'left': location_pos - 1,
            'right': location_pos + 1,
        }
        for key, value in locs.items():
            if value >= 0 and value < 25 and self._can_go(location_pos, key):
                available[1].append(value)
        calculated = 2
        calculated_points = [i for i in available[1]]
        while turns > 1:
            available[calculated] = list()
            for i in available[calculated-1]:
                locs = {
                    'top': i - 5,
                    'bot': i + 5,
                    'left': i - 1,
                    'right': i + 1,
                }
                for key, value in locs.items():
                    if value >= 0 and value < 25 and value not in calculated_points and self._can_go(i, key):
                        available[calculated].append(value)
            available[calculated] = list(set(available[calculated]))
            calculated_points.extend(available[calculated])
            calculated += 1
            turns -= 1
        return available        
    
    def gen_city(self):
        name = random.choice(store.wildworld_city_names)
        data = {'name': name, 'type': 'city'}
        data.update(random.choice(store.wildworld_cities.values()))
        return Location(data)
    
    def gen_road(self):
        data = {'type': 'road'}
        data.update(store.wildworld_locations['road'])
        return Location(data)
    
    def gen_wildness(self):
        data = {'type': 'wildness'}
        data.update(store.wildworld_locations['wildness'])
        return Location(data)


class Item(object):
    ITEMS = dict()

    def __init__(self, id, data):
        self.id = id
        self._data = data
    
    @property
    def type(self):
        return self._data.get('type')
    
    def escape_chance(self, value):
        return self._data.get('escape_chance', lambda x: x)(value)
    
    def food_consumption(self, value):
        return self._data.get('food_consumption', lambda x: x)(value)
    
    def __getattr__(self, key):
        try:
            return self.__dict__['_data'][key]
        except KeyError:
            raise AttributeError(key)
    
    @classmethod
    def register_item(cls, id, item):
        cls.ITEMS[id] = item
    
    @classmethod
    def get_item(cls, id):
        return cls.ITEMS[id]
    
    def has_tag(self, tag):
        return tag in self._data.get('tags', list())


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
            person = person_maker.gen_person()
        gender = Feature.get_feature(person.gender)
        world_person = WildWorldPerson(person)
        world_person.add_feature(gender)
        return world_person

class WildWorldPerson(object):
    

    def __init__(self, coreperson):
        self._wrapped_person = coreperson
        self.features = dict()
        self.slotless_features = list()
        self.applied_item = None
        self._items = Counter()
    
    def add_item(self, item):
        self._items[item] += 1
    
    def remove_item(self, item):
        if self._items[item] > 0:
            self._items[item] -= 1
    
    def items(self, tag=None):
        if tag is not None:
            return [i for i in self._items.keys() if i.has_tag(tag)]
        return self._items.keys()
    
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
    
    def attribute(self, attr):
        return self.count_modifiers(attr)
    
    def count_modifiers(self, attr):
        value = 0
        for i in self.features.values():
            value += i.count_modifiers(attr)
        for i in self.slotless_features:
            value += i.count_modifiers(attr)
        return max(-2, min(value, 5))
    
    def attributes(self):
        attrs = dict()
        for key in store.wildworld_attributes.keys():
            attrs[key] = self.attribute(key)
        return attrs
    
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
    
    @property
    def name(self):
        return self._wrapped_person.firstname
    
    @property
    def gender(self):
        return self._wrapped_person.gender