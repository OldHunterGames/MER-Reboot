from collections import defaultdict
import ntpath

import renpy.store as store
import renpy.exports as renpy

from mer_person import PersonWrapper
from mer_command import Command
from mer_utilities import card_back, get_files


class ZombieWorldEvent(object):

    EVENTS = dict()
    _IMAGES = dict()

    def __init__(self, id, data):
        self.id = id
        self._data = data

    @classmethod
    def register_event(cls, id, event):
        cls.EVENTS[id] = event

    @classmethod
    def get_events(cls):
        return [i for i in cls.EVENTS.values()]

    def is_pseudo(self):
        return self._data.get('pseudo', False)

    def name(self):
        return self._data.get('name', 'No name')

    def label(self):
        return self._data.get('label')

    def description(self):
        return self._data.get('description', 'No description')

    def _get_image(self, key, suffix):
        path = 'extensions/Worlds/ZombieWorld/resources/events'
        images = get_files(path)
        event_image = self._data.get(key)
        if event_image is None:
            event_image = self._IMAGES.get(self.id + suffix)
        if event_image is None:
            for image in images:
                if ntpath.basename(image).split('.')[0] == self.id + suffix:
                    ZombieWorldEvent._IMAGES[self.id + suffix] = image
                    event_image = image
        return card_back() if event_image is None else event_image

    def list_image(self):
        return self._get_image('list_image', '_list')

    def select_image(self):
        return self._get_image('select_image', '_select')

    def bg_image(self):
        return self._get_image('bg_image', '_bg')

    def price_description(self):
        return self._data.get('price_description', '')

    def can_call(self):
        return True

    def call(self, person, world):
        renpy.call_in_new_context(self.label(), event=self, person=person, world=world)


class ZombieWorldLocation(object):

    _IMAGES = dict()

    def __init__(self, id, data):
        self.id = id
        self._data = data
        self._events = dict()
        self.selected_event = None
        self._description = None

    def set_description(self, text):
        self._description = text

    def select_event(self, event):
        self.selected_event = event

    def add_event(self, event):
        self._events[event.id] = event

    def remove_event(self, event):
        if event == self.selected_event:
            self.selected_event = None
        del self._events[event.id]

    def remove_event_by_id(self, id):
        if self._events[id] == self.selected_event:
            self.selected_event = None
        del self._events[id]

    def events(self):
        return [i for i in self._events.values()]

    def description(self):
        if self._description is not None:
            return self._description
        return self._data.get('description', 'No description')

    def name(self):
        return self._data.get('name', 'No name')

    def image(self):
        path = 'extensions/Worlds/ZombieWorld/resources/locations'
        images = get_files(path)
        location_image = self._data.get('image')
        if location_image is None:
            location_image = self._IMAGES.get(self.id)
        if location_image is None:
            for image in images:
                if ntpath.basename(image).split('.')[0] == self.id:
                    ZombieWorldLocation._IMAGES[self.id] = image
                    location_image = image
        return location_image


class ZombieWorldPersonMaker(object):
    
    @classmethod
    def make_person(cls, person=None, person_maker=None):
        if person_maker is not None:
            person = person_maker.gen_person(genus='human')
        world_person = ZombieWorldPerson(person)
        return world_person


class ZombieWorldItem(object):

    def __init__(self, id):
        self.id = id


class ZombieWorldPerson(PersonWrapper):
    

    def __init__(self, *args, **kwargs):
        super(ZombieWorldPerson, self).__init__(*args, **kwargs)
        self.male_filth = 0
        self.female_filth = 0
        self._vitality = 100
        self._items = list()
        self._events = defaultdict(list)

    @property
    def vitality(self):
        return self._vitality

    @vitality.setter
    def vitality(self, value):
        self._vitality = max(0, min(100, value))
        for ev in self._events['vitality_changed']:
            ev(self.vitality)

    def add_eventlistener(self, event, callback):
        self._events[event].append(callback)

    def remove_eventlistener(self, event, callback):
        self._events[event].remove(callback)

    def add_item(self, item):
        self._items.append(item)

    def items(self):
        return [i for i in self._items]

    def remove_item(self, item):
        self._items.remove(item)

    def has_item(self, id):
        return True if self.find_item(id) is not None else False

    def find_item(self, id):
        for i in self._items:
            if i.id == id:
                return i


class ZombieWorldActivateEvent(Command):

    def __init__(self, person, event, world):
        self.person = person
        self.event = event
        self.world = world

    def run(self):
        self.event.call(self.person, self.world)
    
