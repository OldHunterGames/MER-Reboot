# -*- coding: UTF-8 -*-
from mer_utilities import Observable
from collections import defaultdict
import random
import renpy.exports as renpy
import renpy.store as store
import copy


class MERCore(object):

    def __init__(self):

        self._player = None
        self.characters = list()

    def add_character(self, person):
        self.characters.append(person)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value

class EventsBook(object):

    def __init__(self, turns_to_store=0):
        self._events = list()
        self._turns_to_store = turns_to_store
        self._turns_passed = 0

    def skip_turn(self):
        self._turns_passed += 1
        if self._turns_passed > self._turns_to_store:
            self._clear_events()
            self._turns_passed = 0

    def _clear_events(self):
        self._events = list()

    def add_entry(self, value):
        self._events.append(value)

    def get_records(self):
        return copy.copy(self._events)


class PersonalBook(EventsBook):

    def __init__(self, turns_to_store=0):
        super(PersonalBook, self).__init__(turns_to_store)
        self._events = defaultdict(list)

    def add_entry(self, person, value):
        self._events[person].append(value)

    def get_records(self, person):
        return copy.copy(self._events[person])

    def _clear_events(self):
        self._events = defaultdict(list)


class World(object):
    # Basic class for every world connected to MER
    # in modules, save any specific data to world instance
    # to save state between visits to same world
    
    items_whitelist = []
    description = None
    type = None

    def __init__(self, core, *args, **kwargs):
        self._synced = False
        self._gem_added = False
        self._core = core
        self._travelers = list()

    @property
    def player(self):
        for i in self._travelers:
            if self._core.player == i:
                return i

    def get_travelers(self):
        return copy.copy(self._travelers)
    
    def _transfer_persons(self, *args):
        # basic implementation for persons transfering between worlds
        # for i in args:
        #    self._transfer_items(i)
        self._travelers += args
    
    def _transfer_items(self, person):
        # basic implementation for items transfering
        for item in person.all_items():
            if item.id not in self.items_whitelist:
                person.remove_item(item)
    
    def entry_point(self):
        # should return entry label of world
        raise NotImplementedError
    
    def return_point(self):
        return None

    def navgem_mark(self):
        self._gem_added = True
        self._synced = True

    def travel(self, core, travelers):
        core.set_world(self)
        self._transfer_persons(*travelers)
        if getattr(self, '__visited', False):
            self.__visited = True
            if self.return_point() is not None:
                renpy.call_in_new_context(self.return_point(), world=self)
        self.__visited = True
        renpy.call_in_new_context(self.entry_point(), world=self)
    
    @classmethod
    def can_create_worlds(cls):
        return True
    
    @classmethod
    def get_worlds(cls):
        return [i for i in cls.__subclasses__() if i.can_create_worlds]

    def sync_world(self):
        if self._synced:
            return False
        self._synced = True
        return True

    def leave(self, person=None):
        if person is None:
            person = self.player
        if self._synced and not self._gem_added:
            person.add_item(NavigationGem(self))
            self._gem_added = True
        self._core.set_world('core')
        self._transfer_persons(*self._travelers)

    def path(self, name):
        return 'extensions/Worlds/' + self.get_path() + name

    def get_path(self):
        raise NotImplementedError()

class MistTravel(object):


    def __init__(self, core, world, *args, **kwargs):
        self.core = core
        try:
            self.world = world(core)
        except TypeError:
            self.world = world
        self.travelers = args
        self.navgem = kwargs.get('navgem', False)
    
    def travel(self):
        #TODO: mist events
        self.world.navgem_mark()
        self.world.travel(self.core, self.travelers)
        self.world.leave()
        # mist event again
        self.core.set_world('core')
        #TODO: clear outer world items


class Hierarchy(object):

    HIERARCHY = defaultdict(list)
    STATUSES = {
        1: 'plebeian',
        2: 'patrician',
        3: 'senator',
        4: 'noble',
        5: 'princeps'
    }

    def __init__(self, person):

        self.person = person

    def add_clientela(self, person):
        self.HIERARCHY[self.person].append(person)

    def can_be_clientela(self, person):
        return self.status() > Hierarchy(person).status()

    def assembly(self):
        clientelas = self.HIERARCHY[self.person]
        assembly = self.person.get_chorus()
        for clientela in clientelas:
            assembly.extend(clientela.get_host())
        return assembly

    def status(self):
        return max([i.level() for i in self.person.get_host()])

    def status_str(self):
        return self.STATUSES[self.status()]

