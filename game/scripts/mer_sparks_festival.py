# -*- coding: UTF-8 -*-
import renpy.store as store
import renpy.exports as renpy


class SparksFestival(object):

    DEFAULT_BONUSES = {
        1: 25,
        2: 50,
        3: 100,
        4: 200,
    }

    def __init__(self, persons, hierarchy):
        self.persons = persons
        self.hierarchy = hierarchy

    def run(self):
        return

    @classmethod
    def default_bonus(cls, person, hierarchy):
        status = hierarchy(person).status()
        if status == 4:
            # TODO: check for minor house ownership
            return cls.DEFAULT_BONUSES[status]
        if status == 5:
            return 1000

        return cls.DEFAULT_BONUSES[status]