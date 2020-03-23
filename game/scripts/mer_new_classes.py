from mer_basics import Suits
import random

class PersonClassType(object):
    useless = 'useless'
    matrial = 'matrial'
    social = 'social'
    service = 'service'
    managing = 'managing'

def person_class_suit(person_class):
    return {
        'useless': Suits.SKULL,
        'matrial': Suits.SPADES,
        'social': Suits.HEARTS,
        'service': Suits.DIAMONDS,
        'managing': Suits.CLUBS
    }[person_class]


class ClassData(object):
    _BACKGROUND_DATA = {}
    _CLASS_DATA = {}

    def __init__(self, person):
        self.person = person
    

class MERBackgroundClass(object):

    _DATA = {}

    @classmethod
    def get_classes(cls):
        return cls._DATA.values()
    
    @classmethod
    def get_random_class(cls):
        return random.choice(cls.get_classes())

    def __init__(self, id, data):
        self.data = data
        self.id = id
    
    def level(self):
        return self.data.get('level', 0)
    
    def name(self):
        return self.data.get('name', 'No name')
    
    def description(self):
        return self.data.get('description', 'No description')

class MERClass(object):
    
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def name(self):
        return self.data.get('name', 'No name')
    
    def description(self):
        return self.data.get('description', 'No description')