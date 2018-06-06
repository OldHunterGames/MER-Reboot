# -*- coding: UTF-8 -*-
import random
import copy
from collections import Counter, defaultdict
import renpy.store as store
import renpy.exports as renpy
from mer_utilities import encolor_text


class SlaverCaravanQuest(object):

    QUESTS = dict()

    def __init__(self, id):
        self.id = id

    @classmethod
    def register_quest(cls, id, quest):
        cls.QUESTS[id] = quest

    @classmethod
    def get_quests(cls):
        return [i for i in cls.QUESTS.values()]

    def label(self):
        return 'lbl_slavercaravan_quest_' + self.id


class Location(object):
    
    def __init__(self, data):
        self._data = data
        self.visited = False
    
    def name(self):
        return self._data.get('name')
    
    def label(self):
        return self._data.get('label')
    
    def type(self):
        return self._data.get('type')
    
    def events(self):
        return self._data.get('events')
    
    def visit(self, world):
        renpy.call(self.label(), world=world)
    
    def get_text(self, id):
        data = self._data.get('texts', dict())
        return data.get(id, 'No text')
    
    def random_text(self, id):
        data = self._data.get('texts', dict())
        texts = data.get(id, [])
        if len(texts) > 0:
            return random.choice(texts)
        else:
            return 'No text'

class Locations(object):
    
    def __init__(self, width=5, height=5, **kwargs):
        self._width = 5
        self._height = 5
        self.locations = [None for i in range(width*height)]
        self._wild_indexes = list()
        self.current = 0
        self.city_names = copy.copy(store.slavercaravan_town_names)
        self._world = kwargs.get('world')
        self.quests_pool = kwargs.get('quests')
        self._generate_locations()
        
    
    def size(self):
        return len(self.locations)
    
    def current_location(self):
        return self.get_loc(self.current)
    
    def get_closest_wildness(self):
        locations = []
        current_location = self.current_location()
        if current_location.type() == 'wildness':
            return current_location
        if current_location.type() == 'city':
            turns = 2
        else:
            turns = 1
        available = self.can_go(self.current, turns)
        for list_ in available.values():
            for i in list_:
                if self.get_loc(i).type() == 'wildness':
                    locations.append(self.get_loc(i))
        return random.choice(locations)
        
    
    def _generate_locations(self):
        city = 2
        empty_row = False
        for i in range(0, self._height):
            index = i * self._width
            if empty_row:
                self.locations[index] = self.gen_road()
                self.locations[index+1] = self.gen_wildness(index+1)
                self.locations[index+2] = self.gen_road()
                self.locations[index+3] = self.gen_wildness(index+3)
                self.locations[index+4] = self.gen_road()
                empty_row = False
            else:
                if city == 2:
                    self.locations[index] = self.gen_city()
                    self.locations[index+1] = self.gen_road()
                    self.locations[index+2] = self.gen_wildness(index+2)
                    self.locations[index+3] = self.gen_road()
                    self.locations[index+4] = self.gen_city()
                    city = 1
                    empty_row = True
                elif city == 1:
                    self.locations[index] = self.gen_wildness(index)
                    self.locations[index+1] = self.gen_road()
                    self.locations[index+2] = self.gen_city()
                    self.locations[index+3] = self.gen_road()
                    self.locations[index+4] = self.gen_wildness(index+4)
                    city = 2
                    empty_row = True
        self.current = random.choice(self._wild_indexes)
            
                
    
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
    
    def locs_to_go(self):
        locs = {
            'top': self.current - 5,
            'bot': self.current + 5,
            'left': self.current - 1,
            'right': self.current + 1,
        }
        available = dict()
        for key, value in locs.items():
            if value >= 0 and value < 25 and self._can_go(self.current, key):
                available[key] = value
            else:
                available[key] = None
        return available
        
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
        data = {'type': 'city'}
        city = random.choice(store.slavercaravan_cities.items())
        data.update(city[1])
        name = random.choice(self.city_names[city[0]])
        data['name'] = name
        img = random.choice(store.slavercaravan_cities[city[0]]['images'])
        img = self._world.path(img)
        loc = Location(data)
        loc.image = img
        loc.quest = random.choice(self.quests_pool)
        self.quests_pool.remove(loc.quest)
        return loc
    
    def gen_road(self):
        data = {'type': 'road'}
        data.update(store.slavercaravan_locations['road'])
        img = random.choice(store.slavercaravan_locations['road']['images'])
        img = self._world.path(img)
        loc = Location(data)
        loc.image = img
        return loc
    
    def gen_wildness(self, index):
        data = {'type': 'wildness'}
        data.update(store.slavercaravan_locations['wildness'])
        self._wild_indexes.append(index)
        img = random.choice(store.slavercaravan_locations['wildness']['images'])
        img = self._world.path(img)
        loc = Location(data)
        loc.image = img
        return loc


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
    
    @classmethod
    def get_items(cls, tag):
        return [i for i in cls.ITEMS.values() if i.has_tag(tag)]
    
    def has_tag(self, tag):
        return tag in self._data.get('tags', list())


class SlaverCaravanPersonMaker(object):
    
    @classmethod
    def make_person(cls, person=None, person_maker=None):
        if person_maker is not None:
            person = person_maker.gen_person(genus='human')
        world_person = SlaverCaravanPerson(person)
        return world_person

class SlaverCaravanPerson(object):
    

    def __init__(self, coreperson):
        self._wrapped_person = coreperson
        self.applied_item = None
        self._items = Counter()
        self._state = 5
        self._statuses = set()
        self._events = defaultdict(list)
    
    def add_event(self, id, func):
        self._events[id].append(func)
    
    def remove_event(self, id, func):
        try:
            self._events[id].remove(func)
        except ValueError:
            pass
    
    def has_status(self, value):
        return value in self._statuses
    
    def add_status(self, value):
        self._statuses.add(value)
    
    def remove_status(self, value):
        if self.has_status(value):
            self._statuses.remove(value)
    
    def statuses(self):
        return [i for i in self._statuses]
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = max(-1, min(5, value))
        if self._state < 2:
            for func in self._events['critical_state']:
                func(self)
        if self._state <= 0:
            renpy.call_in_new_context('lbl_slavercaravan_gameover')
    
    def add_item(self, item):
        self._items[item] += 1
    
    def remove_item(self, item):
        if self._items[item] > 0:
            self._items[item] -= 1
        if self._items[item] == 0:
            del self._items[item]
    
    def items(self, tag=None, as_dict=False):
        if as_dict:
            return copy.copy(self._items)
        if tag is not None:
            return [i for i in self._items.keys() if i.has_tag(tag)]
        return self._items.keys()
    
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


class SlaverCaravanFilter(object):

    @staticmethod
    def filter_by_gender(items, gender):
        return [person for person in items if person.gender == gender]

    @staticmethod
    def filter_by_attribute(items, attr_value, attr='all'):
        if attr == 'all':
            return [person for person in items if any([value >= attr_value for value in person.attributes().values()])]
        else:
            return [person for person in items if person.attribute(attr) >= attr_value]