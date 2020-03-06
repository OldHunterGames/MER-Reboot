import random


_natures_list = ['sanguine', 'choleric', 'phlegmatic', 'melancholic']
class NatureData(object):
    
    _DATA = {}
    def __init__(self, person):
        self.person = person
        if self._DATA.get(person) is None:
            self._DATA[person] = random.choice(_natures_list)
    
    def get_nature(self):
        return self._DATA[self.person]
    
    @staticmethod
    def shuffled_natures():
        list_copy = [i for i in _natures_list]
        random.shuffle(list_copy)
        return list_copy
    
    @staticmethod
    def natures():
        list_copy = [i for i in _natures_list]
        return list_copy

class QuirkData(object):
    _DATA = {}
    def __init__(self, person):
        self.person = person
        if self._DATA.get(person) is None:
            self._DATA[person] = Quirk.generate_quirks_pair()
    
    def get_quirks(self):
        return [i for i in self._DATA[self.person]]

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
    def get_quirks(cls):
        return cls._DATA.values()
    
    @classmethod
    def generate_quirks_pair(cls):
        if (len(cls._DATA) < 1):
            raise 'Quirk data not initialized'
        quirks = dict(cls._DATA.items())
        first = random.choice(quirks.values())
        del quirks[first.id]
        available = [quirk for quirk in quirks.values() if quirk.bad_strategy != first.good_strategy]
        return first, random.choice(available)
    
    @classmethod
    def quirk_good_stategy(cls, quirk):
        return cls._DATA[quirk.id].good_strategy
    
    @classmethod
    def quirk_bad_stategy(cls, quirk):
        return cls._DATA[quirk.id].bad_strategy
    
    @classmethod
    def quirk_by_good_strategy(cls, strategy):
        for value in cls._DATA.values():
            if cls.quirk_good_stategy(value) == strategy:
                return value
    
    @classmethod
    def quirk_by_bad_strategy(cls, strategy):
        for value in cls._DATA.values():
            if cls.quirk_bad_stategy(value) == strategy:
                return value

    def __init__(self, id, data):
        self.id = id
        self.data = data
    
    @property
    def good_strategy(self):
        return self.data['good_strategy']
    
    @property
    def good_reactions(self):
        return self.data['good_reactions']
    
    @property
    def bad_strategy(self):
        return self.data['bad_strategy']
    
    @property
    def bad_reactions(self):
        return self.data['bad_reactions']

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

    @classmethod
    def get_strategies(cls):
        return [
            cls.chantage,
            cls.bribe,
            cls.deprivation,
            cls.seduction,
            cls.reason,
            cls.torture,
            cls.humiliation,
            cls.discipline,
        ]

class StrategyQuality(object):
    good = 'good'
    bad = 'bad'
    neutral = 'neutral'

class QuirksSuggestions(object):
    _DATA = {}

    def __init__(self, person):
        self.person = person
        if self._DATA.get(person) is None:
            self._DATA[person] = {
                'nature': None,
                'quirk1': None,
                'quirk2': None
            }
    
    def get_control_strategy_suggestions(self):
        quirk1 = self._DATA[self.person]['quirk1']
        quirk2 = self._DATA[self.person]['quirk2']
        return [
            quirk1 and Quirk.quirk_good_stategy(quirk1),
            quirk2 and Quirk.quirk_good_stategy(quirk2),
        ]
    
    def suggest(self, field, value):
        self._DATA[self.person][field] = value
    
    def get_suggestion(self, field):
        return self._DATA[self.person][field]

    def get_suggestions(self):
        return self._DATA[self.person].values()