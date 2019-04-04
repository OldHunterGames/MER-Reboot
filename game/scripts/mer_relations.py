import collections


class TensionPoint(object):

    def __init__(self, name, reason):
        self.name = name
        self.reason = reason


class InfluenceCard(object):

    _INFLUENCE_CARDS = dict()

    @classmethod
    def register(cls, id, item):
        cls._INFLUENCE_CARDS [id] = item

    @classmethod
    def get_one(cls, id):
        return cls._INFLUENCE_CARDS [id]

    def __init__(self, id, data):
        self.id = id
        self.data = data

    def name(self):
        return self.data.get('name')

    def image(self):
        return self.data.get('image')

    def positive_connection(self):
        return self.data.get('positive_connection')

    def negative_connection(self):
        return self.data.get('negative_connection')


class Relations(object):
    MAX_INFLUENCE = 3
    CONFLICT_TYPES = {
        'pride': 'abusive',
        'fear': 'vengeful',
        'greed': 'demanding',
        'dependence': 'spoiled',
        'jealousy': 'scornful',
        'impudent': 'lust'
    }

    HARMONY_TYPES = {
        'pride': 'benevolent',
        'fear': 'submissive',
        'greed': 'amused',
        'dependence': 'obedient',
        'jealousy': 'zealous',
        'impudent': 'slutty'
    }
    
    def __init__(self):
        self._tension_points = list()
        self._influence = collections.deque(maxlen=self.MAX_INFLUENCE)

    def tension(self):
        return len(self._tension_points)

    def add_tension(self, tension):
        self._tension_points.append(tension)

    def add_influence(self, influence):
        self._influence.append(influence)

    def get_influence(self):
        return [i for i in self._influence]
