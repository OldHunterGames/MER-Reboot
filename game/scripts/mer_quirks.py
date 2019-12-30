import random

class QuirkData(object):
    _DATA = {}
    def __init__(self, person):
        self.person = person
        if self._DATA.get(person) is None:
            self._DATA[person] = Quirk.generate_quirks_pair()
    
    def good_strategy(self):
        return [quirk.good_strategy for quirk in self._DATA[self.person]]
    
    def bad_strategy(self):
        return [quirk.bad_strategy for quirk in self._DATA[self.person]]
    
    def get_strategy_quality(self, strategy):
        if strategy in self.good_strategy():
            return StrategyQuality.good
        if strategy in self.bad_strategy():
            return StrategyQuality.bad
        return StrategyQuality.neutral

class Quirk(object):
    _DATA = {}

    @classmethod
    def register_quirks(cls, data_dict):
        for key, value in data_dict.items():
            cls._DATA[key] = Quirk(key, value)
    
    @classmethod
    def generate_quirks_pair(cls):
        if (len(cls._DATA) < 1):
            raise 'Quirk data not initialized'
        quirks = dict(cls._DATA.items())
        first = random.choice(quirks.values())
        del quirks[first.id]
        available = [quirk for quirk in quirks.values() if quirk.bad_strategy != first.good_strategy]
        return first, random.choice(available)

    def __init__(self, id, data):
        self.id = id
        self.data = data
    
    @property
    def good_strategy(self):
        return self.data['good_strategy']
    
    @property
    def bad_strategy(self):
        return self.data['bad_strategy']

    @property
    def name(self):
        return self.data.get('name', 'No name')

class ControlStrategy(object):
    chantage = 'chantage'
    bribe = 'bribe'
    seduction = 'seduction'
    reason = 'reason'
    torture = 'torture'
    deprivation = 'deprivation'
    humiliation = 'humiliation'
    discipline = 'discipline'

class StrategyQuality(object):
    good = 'good'
    bad = 'bad'
    neutral = 'neutral'