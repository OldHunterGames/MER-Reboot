import renpy.exports as renpy
import renpy.store as store


class SexParticipant(object):

    def __init__(self, person, controlled_by_player=False):
        self.person = person
        self.controlled_by_player = controlled_by_player
        self.thrill = 0
        self.interest = 5
        self.used_actions = set()
        self._conditions = ['cloth', 'free_mouth']
        self.actions = {
            'pose': SexAction.get_action('sit'),
            'behavior': SexAction.get_action('sadly')
        }

    @property
    def conditions(self):
        temp_added = set()
        temp_removed = set()
        for value in self.actions.values():
            temp_added = temp_added.union(set(value.temp_personal_conditions().get('add')))
            temp_removed = temp_removed.union(set(value.temp_personal_conditions().get('remove')))
        return list(set(self._conditions).union(temp_added).difference(temp_removed))

    def apply_action(self, action):
        self.actions[action.type()] = action
        data = action.edit_personal_conditions()
        for removed in data.get('remove', []):
            self._conditions.remove(removed)
        for added in data.get('add', []):
            self._conditions.aappend(added)
        if action.type() == 'pose' or action.type() == 'behavior':
            try:
                del self.actions['action']
            except KeyError:
                pass
        else:
            self.use_action(action)
    
    def use_action(self, action):
        self.interest -= 1
        if action in self.used_actions:
            return
        self.used_actions.add(action)
        self.thrill += 1

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

    def filter_actions(self, actions):
        personal_conditions = self.participants[0].conditions
        filtered = []
        for i in actions:
            if (all([cond in personal_conditions for cond in i.personal_conditions()])
                and all([cond in self.state for cond in i.conditions()])):
                    filtered.append(i)
        return filtered

    def apply_action(self, action):
        self.participants[0].apply_action(action)

    def is_active_behavior(self, action):
        actions = self.participants[0].actions
        return action == actions.get('behavior')

    def remove_action(self, action):
        del self.actions[action.type()]

    def description(self):
        text = ''
        for i in self.actions.values():
            text += i.description() + '\n'
        return text
    
    def action_multikey_description(self):
        actions = self.participants[0].actions
        if actions.get('action') is None:
            key = frozenset([actions.get('pose').id])
        else:
            key = frozenset([i.id for i in actions.values()])
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

    def edit_conditions(self):
        return self.data.get('edit_conditions', {'remove': [], 'add': []})

    def personal_conditions(self):
        return self.data.get('personal_conditions', [])

    def edit_personal_conditions(self):
        return self.data.get('edit_personal_conditions', {'remove': [], 'add': []})
    
    def temp_personal_conditions(self):
        return self.data.get('temp_personal_conditions', {'remove': [], 'add': []})