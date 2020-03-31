from mer_basics import Suits
import random

class PersonClassType(object):
    useless = 'useless'
    matrial = 'matrial'
    social = 'social'
    service = 'service'
    managing = 'managing'

    @classmethod
    def get_types(cls):
        return ['useless', 'matrial', 'social', 'service', 'managing']

def person_class_suit(person_class):
    return {
        'useless': Suits.SKULL,
        'matrial': Suits.SPADES,
        'social': Suits.HEARTS,
        'service': Suits.DIAMONDS,
        'managing': Suits.CLUBS
    }[person_class]


class ClassData(object):
    _CLASS_DATA = {}

    def __init__(self, person):
        self.person = person

    def set_class(self, new_class):
        self._CLASS_DATA[self.person] = new_class
    
    def get_class(self):
        if self.person in self._CLASS_DATA.keys():
            return self._CLASS_DATA[self.person]
        return self._get_background()
    
    def _get_background(self):
        return self.person.feature_by_slot('background')

    def class_level(self):
        return self.person.count_modifiers('class_' + self.get_class().type())

class MERClass(object):

    _DATA = {}

    @classmethod
    def register_classes(cls, data):
        for key, value in data.items():
            cls._DATA[key] = MERClass(key, value)
    
    @classmethod
    def get_random_class_by_type(cls, type):
        return random.choice(cls.get_classes_by_type(type))
    
    @classmethod
    def get_classes_by_type(cls, type):
        return [i for i in cls._DATA.values() if i.type == type]
    
    @classmethod
    def get_classes(cls):
        return cls._DATA.values()
    
    @classmethod
    def get_class(cls, id):
        return cls._DATA[id]
    
    @classmethod
    def get_random_class(cls):
        return random.choice(cls.get_classes())
    
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def name(self):
        return self.data.get('name', 'No name')
    
    def description(self):
        return self.data.get('description', 'No description')
    
    def type(self):
        return self.data['type']