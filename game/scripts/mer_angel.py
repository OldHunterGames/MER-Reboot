# -*- coding: UTF-8 -*-
from mer_utilities import default_avatar


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
    DOMINATION_GRADE = AngelGrade('domination_grade', 1)

    def __init__(self, name, avatar=None, *args, **kwargs):
        self.name = name
        self._avatar = avatar
        self.grade = kwargs.get('grade')
        self.ansible = list()
        self.kanonarch = None

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
