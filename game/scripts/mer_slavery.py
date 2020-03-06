class SlaveStats(object):

    def __init__(self):
        self.obedience = 0
        self.approachability = 1
    
    def refresh_approachability(self):
        self.approachability = max(self.obedience, 1)
    
    def decrease_approachability(self):
        self.approachability -= 1
    
class Slave(object):
    _DATA = {}

    def __init__(self, person):
        self.person = person
        if self._DATA.get(person) is None:
            self._DATA[person] = SlaveStats()
    
    def increase_obedience(self):
        print('obedience increased')
        self._DATA[self.person].obedience += 1

    def obedience(self):
        return self._DATA[self.person].obedience
    
    def approachability(self):
        return self._DATA[self.person].approachability
    
    def decrease_approachability(self):
        self._DATA[self.person].decrease_approachability()
        if self.approachability() < 1:
            self.person.exhausted = True
    
    def refresh(self):
        self._DATA[self.person].refresh_approachability()

class SlaveClassTree(object):
    _DATA = {}

    def __init__(self, person):
        self.person = person
        if self._DATA.get(person) is None:
            self._DATA[person] = 'slave'
    
    def get_class(self):
        return self._DATA[self.person]
