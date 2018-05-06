# -*- coding: UTF-8 -*-
import random
from mer_utilities import default_avatar, Observable
from mer_core import Hierarchy
import renpy.store as store


class AngelMaker(object):

    OBSERVERS = {
        'archon_generated': list()
    }

    @staticmethod
    def add_observer(event, callback):
        AngelMaker.OBSERVERS[event].append(callback)

    @staticmethod
    def remove_observer(event, callback):
        AngelMaker.OBSERVERS[event].remove(callback)

    @staticmethod
    def gen_archon_name():
        return random.choice(store.archon_first_names) + ' ' + random.choice(store.archon_second_names)

    @staticmethod
    def gen_archon():
        archon = CoreAngel(AngelMaker.gen_archon_name(), grade=CoreAngel.DOMINATION_GRADE)
        for i in AngelMaker.OBSERVERS['archon_generated']:
            i(archon)
        return archon

    @staticmethod
    def gen_ellochim_name():
        return random.choice(store.ellochim_names)

    @staticmethod
    def gen_ellochim(archons=None):
        return CoreAngel(AngelMaker.gen_ellochim_name(), grade=CoreAngel.ELLOCHIM_GRADE)

    @staticmethod
    def gen_cherub_name():
        return random.choice(store.cherub_names)

    @staticmethod
    def gen_cherub():
        return CoreAngel(AngelMaker.gen_cherub_name(), grade=CoreAngel.CHERUB_GRADE)

    @staticmethod
    def gen_seraph_name(house):
        return store.seraph_names[house]

    @staticmethod
    def gen_seraph(house):
        return CoreAngel(AngelMaker.gen_seraph_name(house), grade=CoreAngel.SERAPH_GRADE)


class AngelGrade(object):

    def __init__(self, name, value):

        self.name = name
        self.value = value

    
#Guardian-angels grades
GUARDIAN_GRADE = AngelGrade('guarding_grade', 0)
SHADOW_GRADE = AngelGrade('shadow_grade', 0)
SERVANT_GRADE = AngelGrade('servan_grade', 0)
PHOENIX_GRADE = AngelGrade('phoenix_grade', 0)


class CoreAngel(object):


    #Archont grades
    PRINCIPATOR_GRADE = AngelGrade('pricipator_grade', 0)
    VIRTUE_GRADE = AngelGrade('virtue_grade', 0)
    DOMINATION_GRADE = AngelGrade('domination_grade', 2)
    ELLOCHIM_GRADE = AngelGrade('ellochim_grade', 3)
    CHERUB_GRADE = AngelGrade('cherub_grade', 4)
    SERAPH_GRADE = AngelGrade('separh_grade', 5)

    def __init__(self, name, avatar=None, *args, **kwargs):
        self.name = name
        self._avatar = avatar
        self.grade = kwargs.get('grade')
        self.ensemble = list()
        self.kanonarch = None
        self._witnesses = []
        self._apostol = None
        self.world = None
    
    def can_be_apostol(self, person):
        if person == self.apostol:
            return False
        if self.grade == self.DOMINATION_GRADE:
            return True
        elif self.grade.value > 2:
            person_ensemble = [i for i in person.get_host() if i in self.ensemble]
            return len(person_ensemble) > (len(self.ensemble) / 2)
        return False

    def available_kanonarch_grade(self):
        if self.grade == self.DOMINATION_GRADE:
            return self.ELLOCHIM_GRADE
        elif self.grade == self.ELLOCHIM_GRADE:
            return self.CHERUB_GRADE
        return None

    @property
    def apostol(self):
        return self._apostol

    @apostol.setter
    def apostol(self, value):
        self._witnesses.append(value)
        self._apostol = value

    def apostol_cost(self):
        if self.level() == 2:
            return len(self.get_witnesses())
        return store.ensemble_costs[len(self.ensemble)] * store.ensemble_multiplier[self.level()]

    def get_witnesses(self, hierarchy=Hierarchy):
        witnesses = [i for i in self._witnesses]
        if self.apostol is not None:
            witnesses.append(hierarchy(self.apostol).get_patron())
            witnesses.extend(hierarchy(self.apostol).get_clientelas())
            witnesses.extend(self.apostol.successors())
        kanonarch = self.kanonarch
        while kanonarch is not None:
            witnesses.append(kanonarch.apostol)
            kanonarch = kanonarch.kanonarch
        return list(set([i for i in witnesses if i is not None]))

    def add_witness(self, person):
        self._witnesses.append(person)

    def remove_witness(self, person):
        self._witnesses.remove(person)

    @property
    def avatar(self):
        if self._avatar is None:
            return default_avatar()
        return self._avatar

    def add_angel(self, angel):
        self.ensemble.append(angel)
        angel.kanonarch = self

    def level(self):
        return self.grade.value

    def produce_sparks(self):
        if self.world is None:
            return 0
        return len(self.get_witnesses())
