from mer_utilities import value_color

class Emotion(object):

    def __init__(self, id, data):
        self.id = id
        self.data = data
    
    @property
    def name(self):
        return self.data.get('name', self.id)
    
    def opposite(self):
        return self.data.get('opposite')

    def color(self):
        if self.level() > 2:
            return value_color(self.level())
        return self.data['color']
    
    def level(self):
        return self.data.get('level', 2)

basic_emotions = [
    Emotion('fear', {'name': 'Fear', 'opposite': 'anger', 'color': '#808080', 'level': 0}),
    Emotion('anger', {'name': 'Anger', 'opposite': 'fear', 'color': '#000000', 'level': 0}),
    Emotion('suffering', {'name': 'Suffering', 'opposite': 'joy', 'color': '#808080', 'level': 0}),
    Emotion('joy', {'name': 'Joy', 'opposite': 'suffering', 'color': '#000000', 'level': 0}),
    Emotion('disgust', {'name': 'Disgust', 'opposite': 'curiosity', 'color': '#808080', 'level': 0}),
    Emotion('curiosity', {'name': 'Curiosity', 'opposite': 'disgust', 'color': '#000000', 'level': 0}),
    Emotion('apathy', {'name': 'Apathy', 'opposite': 'arousal', 'color': '#808080', 'level': 0}),
    Emotion('arousal', {'name': 'Arousal', 'opposite': 'apathy', 'color': '#000000', 'level': 0})
]

def get_basic_emotion(id):
    emotion = [i for i in basic_emotions if i.id == id][0]
    return emotion

class PersonEmotions(object):
    _DATA = {}

    def __init__(self, person):
        self.person = person
        if not self._DATA.get(person):
            self._DATA[person] = []
    
    def add_emotion(self, emotion):
        if emotion.id not in self.emotions_ids():
            self._DATA[self.person].append(emotion)
    
    def emotions_ids(self):
        return [i.id for i in self._DATA[self.person]]
    
    def combine_emotions(self, emotion1, emotion2, new_emotion):
        emotions = self._DATA[self.person]
        emotions.remove(emotion1)
        emotions.remove(emotion2)
        self.add_emotion(new_emotion)

