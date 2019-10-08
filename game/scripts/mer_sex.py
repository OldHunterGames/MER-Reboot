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
        if person.gender == 'male':
            self._conditions.append('has_dick')
        self.actions = {}
        self.last_description = ''

    @property
    def conditions(self):
        temp_added = set()
        temp_removed = set()
        for value in self.actions.values():
            temp_added = temp_added.union(set(value.temporary_conditions().get('add')))
            temp_removed = temp_removed.union(set(value.temporary_conditions().get('remove')))
        return list(set(self._conditions).union(temp_added).difference(temp_removed))

    def apply_action(self, action):
        self.actions[action.type()] = action
        data = action.permanent_conditions()
        for removed in data.get('remove', []):
            self._conditions.remove(removed)
        for added in data.get('add', []):
            self._conditions.append(added)
            
        if action.type() == 'action':
            self.use_action(action)
            self.actions = {}

    def set_last_action_description(self):
        actions = self.actions
        key = frozenset([i.id for i in actions.values()])

        self.last_description = store.actions_descriptions.get(key, '')
    
    def use_action(self, action):
        self.set_last_action_description()
        self.interest -= 1
        if action in self.used_actions:
            return
        self.used_actions.add(action)
        self.thrill += 1

class SexType(object):
    Solo = 'Solo'
    Duo = 'Duo'
    Group = 'Group'

class SexState(object):
    select_pose = 'select_pose'
    select_modus = 'select_modus'
    select_action = 'select_action'

class MerSex(object):

    def __init__(self, participants, state=None):
        if len(participants) < 1:
            raise Exception('There is should be at least one participant in sex')
        self.state = state or []
        self.participants = participants
        self.target = participants[1]

    def add_action(self, action):
        self.action_flow.append(action)

    def next_action(self):
        if self.participants[0].actions.get('behavior'):
            return 'action'
        elif self.participants[0].actions.get('pose'):
            return 'behavior'
        else:
            return 'pose'

    def filter_actions(self, actions, filter=None):
        filtered = []
        for i in actions:
            current_key = [j.id for j in self.participants[0].actions.values()]
            current_key.append(i.id)
            current_key = frozenset(current_key)
            keys = list(store.actions_descriptions.keys())
            good_keys = []
            allowed = False
            for k in keys:
                if current_key.issubset(k):
                    good_keys.append(k)
            if len(current_key) < 3:
                for key in good_keys:
                    act = self.find_action(key)
                    behavior = self.find_behavior(key)
                    if self.is_available(act) and self.is_available(behavior):
                        allowed = True
            if len(current_key) == 3:
                for key in good_keys:
                    act = self.find_action(key)
                    if self.is_available(act):
                        allowed = True
            if not allowed:
                continue
            if self.is_available(i):
                filtered.append(i)
        if filter is not None:
            return [i for i in filtered if filter(i)]
        return filtered

    def is_available(self, action):
        personal_conditions = self.participants[0].conditions
        target_conditions = self.target.conditions
        return (all([cond in personal_conditions for cond in action.required_conditions()])
            and all([cond in target_conditions for cond in action.required_target_conditions()]))

    def find_action(self, key):
        for i in SexAction.get_by_type('action'):
            if i.id in key:
                return i

    def find_behavior(self, key):
        for i in SexAction.get_by_type('behavior'):
            if i.id in key:
                return i
    def is_available_pose(self, pose):
        return any([pose.id in key for key in SexAction.description_keys()])

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
        return self.participants[0].last_description

    def type(self):
        if len(self.participants) == 1:
            return SexType.Solo
        elif len(self.participants) == 2:
            return SexType.Duo

        return SexType.Group

    def start(self):
        return renpy.call_screen('sc_sex', self)

    def filter(self, cards):
        return [i for i in cards]

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

    def required_conditions(self):
        return self.data.get('conditions', [])

    def required_target_conditions(self):
        return self.data.get('target_conditions', [])

    def permanent_conditions(self):
        return self.data.get('permanent_conditions', {'remove': [], 'add': []})
    
    def temporary_conditions(self):
        return self.data.get('temporary_conditions', {'remove': [], 'add': []})

    @classmethod
    def description_keys(cls):
        return store.actions_descriptions.keys()

    @classmethod
    def pose_keys(cls):
        return [i.id for i in cls.get_by_type('pose')]