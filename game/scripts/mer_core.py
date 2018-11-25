# -*- coding: UTF-8 -*-
from mer_utilities import Observable
from collections import defaultdict
from mer_command import *
import random
import renpy.exports as renpy
import renpy.store as store
import copy


class MERCore(object):

    def __init__(self):

        self._player = None
        self.characters = list()
        self.decade = 1
        self.world = None

    def add_character(self, person):
        self.characters.append(person)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value
    
    def calc_income(self, person):
        income = person.income()
        hierarchy = Hierarchy(person)
        if hierarchy.get_patron() is not None:
            income *= 0.9
            income = int(income)
        for i in hierarchy.get_clientelas():
            income += i.income() // 10
        return income
    
    @Observable
    def skip_turn(self):
        self.player.sparks += self.calc_income(self.player)
        self.player.sparks -= 5
        if self.player.sparks < 0:
            renpy.call_in_new_context('lbl_gameover')
        self.decade += 1

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
    def __init__(self, archon):
        self.archon = archon
        archon.world = self
    
    def visit(self, visitor):
        self.visitor = visitor
        self.on_visit(visitor)
        renpy.call_in_new_context(self.entry_label(), self)
    
    def on_visit(self, person):
        return
    
    def leave(self):
        renpy.jump_out_of_context('lbl_world_return')
    
    def entry_label(self):
        raise NotImplementedError()
    
    def can_sync(self):
        return self.archon not in self.visitor.get_host()
    
    def sync(self):
        SetAngelApostol(self.archon, self.visitor).run()
        self.visitor.sparks -= self.archon.apostol_cost()
    
    def path(self, name):
        return 'extensions/Worlds/' + self.get_path() + name

    def get_path(self):
        raise NotImplementedError()
    
    @classmethod
    def can_create_worlds(cls):
        return True
    
    @classmethod
    def get_worlds(cls):
        return [i for i in cls.__subclasses__() if i.can_create_worlds()]
    
    @classmethod
    def get_random_world(cls):
        return random.choice(cls.get_worlds())

    def get_menu_item_bg(self):
        return None

    def get_menu_item_bg_hover(self):
        return None

    def menu_item_ysize(self):
        return None

class DummyWorld(World):
    
    def entry_label(self):
        return 'lbl_world_dummy'
    
    @classmethod
    def can_create_worlds(cls):
        return False

class MistTravel(object):


    def __init__(self, world, visitor, core):
        self.world = world
        self.visitor = visitor
        self.core = core
    
    def run(self):
        self.core.world = self.world
        self.world.visit(self.visitor)
        self.core.world = None
        self.core.skip_turn()


class Hierarchy(object):

    HIERARCHY = defaultdict(list)
    PATRONS = dict()
    STATUSES = {
        1: 'plebeian',
        2: 'patrician',
        3: 'senator',
        4: 'noble',
        5: 'princeps'
    }

    def __init__(self, person):
        if person is None:
            raise Exception('Hierarchy called with None as person param')
        self.person = person

    def add_clientela(self, person):
        self.HIERARCHY[self.person].append(person)
        self.PATRONS[person] = self.person
        patrons_patron = self.PATRONS.get(self.person)
        while patrons_patron is not None:
            person.add_successor(patrons_patron)
            patrons_patron = self.PATRONS.get(patrons_patron)
        person.add_successor(self.person)
        self.person.add_successor(person)

    def remove_clientela(self, person):
        self.HIERARCHY[self.person].remove(person)
        del self.PATRONS[person]

    def get_patron(self):
        return self.PATRONS.get(self.person)

    def get_clientelas(self):
        return self.HIERARCHY[self.person]

    def can_be_clientela(self, person):
        patron = self.PATRONS.get(self.person)
        while patron is not None:
            if patron == person:
                return False
            patron = self.PATRONS.get(patron)
        return self.status() > Hierarchy(person).status()

    def assembly(self, exclude_self=False):
        clientelas = self.HIERARCHY[self.person]
        if not exclude_self:
            assembly = self.person.get_host()
        else:
            assembly = []
        for clientela in clientelas:
            assembly.extend(clientela.get_host())
        return assembly

    def status(self):
        try:
            status = max([i.level() for i in self.person.get_host()])
        except ValueError:
            status = 1
        return status

    def status_str(self):
        return self.STATUSES[self.status()]

