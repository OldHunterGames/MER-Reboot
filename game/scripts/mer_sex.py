import renpy.exports as renpy
import renpy.store as store


class SexParticipant(object):

    def __init__(self, person, controlled=False):
        self.person = person
        self.tags = []
        self.stamina = 5
        self.drive = 0
        self.eros = []
        self.controlled = controlled
    
    @property
    def avatar(self):
        return self.person.avatar

class MerSex(object):
    def __init__(self, participants):
        self.participants = participants
        self.current_action = []
        self.completed_actions = []
    
    def start(self):
        return renpy.call_screen('sc_sex', self)
    
    def apply_action(self, action):
        self.current_action.append(action)
    
    def remove_action(self, action):
        try:
            self.current_action.remove(action)
        except ValueError:
            pass
    
    def available_actions(self):
        if len(self.current_action) > 0:
            actions = SexCard.get_card_childs(self.current_action[-1])
        else:
            actions = SexCard.get_suitless_cards()
        if len(actions) < 1 and len(self.current_action) > 0:
            self.complete_action()
            return self.available_actions()
        return actions
    
    def complete_action(self):
        self.completed_actions.append(tuple(self.current_action))
        self.current_action.pop()
    
    def current_description(self):
        return get_action_description(self.current_action)
    
    def can_go_back(self):
        return len(self.current_action) > 0
    
    def go_back(self):
        self.current_action.pop()

def get_action_description(action_list):
    return store.sex_descriptions.get(frozenset([i.id for i in action_list]), 'No desc')

class SexCard(object):
    _CARDS = {}
    def __init__(self, id, data):
        self.data = data
        self.id = id
    
    @property
    def name(self):
        return self.data.get('name', 'No name')

    @property
    def suit(self):
        return self.data.get('suit')

    @property
    def childs(self):
        return self.data.get('childs', [])

    @classmethod
    def get_suitless_cards(cls):
        return [i for i in cls._CARDS.values() if i.suit is None]
    
    @classmethod
    def get_card_childs(cls, card):
        return [value for k, value in cls._CARDS.items() if k in card.childs]

    @classmethod
    def register_action(cls, key, value):
        cls._CARDS[key] = SexCard(key, value)