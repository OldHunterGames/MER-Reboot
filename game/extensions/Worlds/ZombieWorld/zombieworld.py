from collections import defaultdict
import os

import renpy.store as store
import renpy.exports as renpy

from mer_person import PersonWrapper
from mer_command import Command
from mer_utilities import card_back, get_files


class ZombieWorldEvent(object):

    def __init__(self, id, data):
        self.id = id
        self._data = data
        self._replaced_texts = []
        self._options_done = []
        self.fight = None

    @classmethod
    def get_events(cls):
        return [i for i in cls.EVENTS.values()]

    def replace_texts(self, texts):
        self._replaced_texts = texts

    def is_pseudo(self):
        return self._data.get('pseudo', False)

    def name(self):
        return self._data.get('name', 'No name')

    def label(self):
        return self._data.get('label')

    def description(self):
        return self._data.get('description', 'No description')

    def texts(self):
        if len(self._replaced_texts) > 0:
            return self._replaced_texts
        return self._data.get('texts', [])

    def options(self):
        return [i for i in self._data.get('options', []) if i[0] not in self._options_done]

    def do_option(self, option):
        self._options_done.append(option)

    def _get_image(self, key, suffix, alternate=None):
        path = 'extensions/Worlds/ZombieWorld/resources/events'
        images = get_files(path)
        event_image = self._data.get(key)
        if event_image is None:
            for image in images:
                if os.path.basename(image).split('.')[0] == self.id + suffix:
                    event_image = image
        return alternate if event_image is None else event_image

    def list_image(self):
        return self._get_image('list_image', '_list')

    def card_image(self):
        return self._get_image(
            'select_image',
            '_card',
            store.ZombieWorldUtilities.card_empty_image()
        )

    def select_image(self):
        return self._get_image(
            'select_image',
            '_select',
            store.ZombieWorldUtilities.event_empty_image()
        )

    def bg_image(self):
        return self._get_image('bg_image', '_bg')

    def price_description(self):
        return self._data.get('price_description', '')

    def can_call(self):
        return True

    def call(self, person, world):
        renpy.call_in_new_context(self.label(), event=self, person=person, world=world)

    def show(self, person, world):
        renpy.show_screen('sc_zombieworld_event', event=self, person=person, world=world)


class ZombieWorldLocation(object):

    def __init__(self, id, data):
        self.id = id
        self._data = data
        self._events = dict()
        self.selected_event = None
        self.venchile = None
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
            for image in images:
                if os.path.basename(image).split('.')[0] == self.id:
                    location_image = image
        return location_image


class ZombieWorldVenchile(object):

    def __init__(self, id, data):
        self.id = id
        self._data = data

    def name(self):
        return self._data.get('name', '')

    def image(self):
        path = 'extensions/Worlds/ZombieWorld/resources/venchiles'
        images = get_files(path)
        venchile_image = self._data.get('image')

        if venchile_image is None:
            for image in images:
                if os.path.basename(image).split('.')[0] == self.id:
                    venchile_image = image
        return venchile_image


class ZombieWorldPersonMaker(object):
    
    @classmethod
    def make_person(cls, person=None, person_maker=None):
        if person_maker is not None:
            person = person_maker.gen_person(genus='human')
        world_person = ZombieWorldPerson(person)
        return world_person


class ZombieWorldItem(object):

    def __init__(self, id, data=None):
        self.id = id
        self._data = data if data is not None else {}

    def combat_value(self):
        return self._data.get('combat_value', 0)

    def statuses(self):
        return self._data.get('statuses', [])

    def rate_of_fire(self):
        return self._data.get('rate_of_fire', 0)

    def ammo_consumption(self):
        return self._data.get('ammo_consumption', 0)


class ZombieWorldPerson(PersonWrapper):
    

    def __init__(self, *args, **kwargs):
        super(ZombieWorldPerson, self).__init__(*args, **kwargs)
        self._vitality = self.max_vitality
        self._filth = 0
        self.zombification = 0
        self.food = 0
        self.drugs = 0
        self.ammo = 0
        self.fuel = 0
        self._items = list()
        self._equipment = {
            'melee_weapon': None,
            'armor': None,
            'ranged_weapon': None
        }
        self._events = defaultdict(list)

    def statuses(self):
        statuses = []
        if self._equipment['armor']:
            statuses.extend(self._equipment['armor'].statuses())
        if self._equipment['melee_weapon']:
            statuses.extend(self._equipment['melee_weapon'].statuses())
        return statuses

    def armor_value(self):
        return self._equipment['armor'].combat_value() if self._equipment['armor'] is not None else 0

    def weapon_value(self):
        return self._equipment['melee_weapon'].combat_value() if self._equipment['melee_weapon'] is not None else 0

    def ranged_weapon(self):
        return self._equipment['ranged_weapon']

    def combat_value(self):
        value = self.weapon_value()
        if 'ignore_armor' not in self.statuses():
            value += self.armor_value()
        return value

    @property
    def filth(self):
        return self._filth

    @filth.setter
    def filth(self, value):
        self._filth = max(0, value)
    
    @property
    def vitality(self):
        return self._vitality

    @vitality.setter
    def vitality(self, value):
        self._vitality = min(self.max_vitality, value)
        for i in self._events['vitality_changed']:
            i(self.vitality)

    @property
    def max_vitality(self):
        return 3 + self.attribute('might')

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


class ZombieWorldCombat(object):

    def __init__(self, world, player, ghoul_count, label, event, followers_count=0,):
        self.world = world
        self.player = player
        self.event = event
        self.followers = followers_count
        self.ghoul_power = ghoul_count
        self.active = True
        self.shots = player.ranged_weapon().rate_of_fire if player.ranged_weapon() is not None else 0
        self.label = label

    def player_power(self):
        return self.player.vitality + self.player.combat_value() + self.followers

    def start(self):
        renpy.call_in_new_context('lbl_zombieworld_combat', combat=self, world=self.world)

    def fight(self):
        self.ghoul_power -= self.player_power()
        ZombieWorldChangeVitality(self.player, -1).run()
        if self.ghoul_power <= 0:
            self.event.fight = None
            renpy.call_in_new_context(self.label, self.event, self.player, self.world)

    def can_shoot(self):
        if self.shots < 1 and not self.shots == 'auto':
            return False

        if self.player.ranged_weapon().ammo_consumption() >= self.player.ammo:
            return True

        return False

    def shoot(self):
        self.player.ammo -= self.player.ranged_weapon().ammo_consumption()
        if self.shots != 'auto':
            self.shots -= 1
        self.ghoul_power -= 1
        if self.ghoul_power <= 0:
            self.event.fight = None
            renpy.call_in_new_context(self.label, self.event, self.player, self.world)

    def ammo_consumption(self):
        if self.player.ranged_weapon() is not None:
            return self.player.ranged_weapon().ammo_consumption()
        return 0

class ZombieWorldActivateEvent(Command):

    def __init__(self, person, event, world):
        self.person = person
        self.event = event
        self.world = world 

    def run(self):
        world = self.world
        person = self.person
        event = self.event
        self.event.call(self.person, self.world)


class ZombieWorldEventAction(Command):

    def __init__(self, person, event, world, action):
        self.person = person
        self.event = event
        self.world = world
        self.action = action

    def run(self):
        self.event.do_option(self.action)
        if self.action['type'] == 'fight':
            renpy.call_in_new_context(
                'lbl_zombieworld_event_start_fight',
                self.event,
                self.person,
                self.world,
                self.action['ghouls'],
                self.action['win_label']
            )
        else:
            renpy.call_in_new_context(self.action['label'], self.event, self.person, self.world)


class ZombieWorldShowEvent(Command):

    def __init__(self, person, event, world):
        self.person = person
        self.event = event
        self.world = world 

    def run(self):
        world = self.world
        person = self.person
        event = self.event
        self.event.show(self.person, self.world)

class ZombieWorldChangeVitality(Command):

    def __init__(self, person, amount):
        self.person = person
        self.amount = amount

    def run(self):
        self.person.vitality += self.amount
        if self.amount < 0:
            zombification = self.person.filth - self.person.vitality
            if self.person.filth > 0 and zombification > 0:
                self.person.zombification += zombification

class ZombieWorldChangeFilth(Command):

    def __init__(self, person, amount):
        self.person = person
        self.amount = amount

    def run(self):
        if self.person.gender == 'female' and self.amount > 0:
            self.person.zombification += self.amount
        self.person.filth += self.amount
