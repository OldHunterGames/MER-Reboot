import renpy.exports as renpy
import renpy.store as store


class SexParticipant(object):

    def __init__(self, person, controlled_by_player=False):
        self.person = person
        self.controlled_by_player = controlled_by_player


class SexType(object):
    Solo = 'Solo'
    Duo = 'Duo'
    Group = 'Group'

class MerSex(object):

    def __init__(self, participants, state=None):
        if len(participants) < 1:
            raise Exception('There is should be at least one participant in sex')
        self.state = state or []
        self.participants = participants
        self.actions = {}
    
    def apply_action(self, action):
        self.actions[action.type()] = action

    def remove_action(self, action):
        del self.actions[action.type()]

    def description(self):
        text = ''
        for i in self.actions.values():
            text += i.description() + '\n'
        return text
    
    def action_multikey_description(self):
        try:
            next(i for i in self.actions.values() if i.type() == 'action')
        except StopIteration:
            return ""
        key = frozenset([i.id for i in self.actions.values()])
        return store.actions_descriptions.get(key, 'No description for %s' % '-'.join(list(key)))

    def type(self):
        if len(self.participants) == 1:
            return SexType.Solo
        elif len(self.participants) == 2:
            return SexType.Duo

        return SexType.Group

    def start(self):
        return renpy.call_screen('sc_sex', self)

    def filter(self, cards):
        return [i for i in cards if all([state in self.state for state in i.conditions()])]

class SexAction(object):
    _ACTIONS = {}

    @classmethod
    def register_action(cls, id, data):
        cls._ACTIONS[id] = SexAction(id, data)

    @classmethod
    def get_by_type(cls, type):
        return [i for i in cls._ACTIONS.values() if i.type() == type]

    @classmethod
    def get_action(cls, id):
        return cls._ACTIONS[id]

    def __init__(self, id, data):
        self.id = id
        self.data = data

    def type(self):
        return self.data.get('type')

    def description(self):
        return self.data.get('description')

    def name(self):
        return self.data.get('name', 'No name action')

    def conditions(self):
        return self.data.get('conditions', [])
        