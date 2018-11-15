import renpy.store as store
import renpy.exports as renpy

from mer_person import PersonWrapper
from mer_command import Command
from mer_utilities import card_back


class ZombieWorldEvent(object):

    EVENTS = dict()

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

    def image(self):
        return self._data.get('image', card_back())

    def price_description(self):
        return self._data.get('price_description', '')

    def price_lbl(self):
        return self._data.get('price_lbl')

    def can_call(self):
        return True

    def call_price(self, person):
        if self.price_lbl() is not None:
            renpy.call_in_new_context(self.price_lbl(), event=self, person=person)

    def call(self, person):
        renpy.call_in_new_context(self.label(), event=self, person=person)


class ZombieWorldLocation(object):

    def __init__(self, id, data):
        self.id = id
        self._data = data
        self._events = list()
        self.selected_event = None
        self._description = None

    def set_description(self, text):
        self._description = text

    def select_event(self, event):
        self.selected_event = event

    def add_event(self, event):
        self._events.append(event)

    def remove_event(self, event):
        self._events.remove(event)

    def events(self):
        return [i for i in self._events]

    def description(self):
        if self._description is not None:
            return self._description
        return self._data.get('description', 'No description')

    def name(self):
        return self._data.get('name', 'No name')


class ZombieWorldPersonMaker(object):
    
    @classmethod
    def make_person(cls, person=None, person_maker=None):
        if person_maker is not None:
            person = person_maker.gen_person(genus='human')
        world_person = ZombieWorldPerson(person)
        return world_person

class ZombieWorldPerson(PersonWrapper):
    

    def __init__(self, *args, **kwargs):
        super(ZombieWorldPerson, self).__init__(*args, **kwargs)
        self.male_filth = 0
        self.female_filth = 0
        self._vitality = 100

    @property
    def vitality(self):
        return self._vitality

    @vitality.setter
    def vitality(self, value):
        self._vitality = max(0, min(100, value))


class ZombieWorldActivateEvent(Command):

    def __init__(self, person, event):
        self.person = person
        self.event = event

    def run(self):
        self.event.call_price(self.person)
        self.event.call(self.person)
    
