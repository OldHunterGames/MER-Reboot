from mer_utilities import roll
import renpy.exports as renpy

class Stress(object):
    
    _DATA = {}

    def __init__(self, person):
        self.person = person
        if person not in self._DATA.keys():
            self._DATA[person] = StressData()
    
    def increase_stress(self):
        self._DATA[self.person].value += 1
    
    def make_unstable(self):
        self._DATA[self.person].unstable = True
    
    def stress_check(self):
        data = self._DATA[self.person]
        if roll(data.value, 6):
            if data.unstable:
                renpy.say(None, '%s stress event' % self.person.name)
            else:
                self.make_unstable()
            return True
        return False

class StressData(object):

    def __init__(self):
        self.value = 0
        self.unstable = False
