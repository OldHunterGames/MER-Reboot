# -*- coding: UTF-8 -*-
import random
from mer_utilities import default_avatar
import renpy.store as store


class AngelMaker(object):

    @staticmethod
    def gen_archon_name():
        return random.choice(store.archon_first_names) + ' ' + random.choice(store.archon_second_names)

    @staticmethod
    def gen_archon():
        return CoreAngel(AngelMaker.gen_archon_name(), grade=CoreAngel.DOMINATION_GRADE)

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
        self.ansible = list()
        self.kanonarch = None
        self.apostol = None
        self.world = None

    @property
    def avatar(self):
        if self._avatar is None:
            return default_avatar()
        return self._avatar

    def add_angel(self, angel):
        self.ansible.append(angel)
        angel.kanonarch = self

    def level(self):
        return self.grade.value

    def produce_sparks(self):
        if self.world is None:
            return 0
        else:
            return self.world.witnesses
