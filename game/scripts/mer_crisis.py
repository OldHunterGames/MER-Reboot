import renpy.store as store
import renpy.exports as renpy


class MerCrisis(object):

    _DATA = []

    @classmethod
    def register_crisis(cls, crisis):
        cls._DATA.append(crisis)

    @classmethod
    def find_by_trigger(cls, trigger, actor, target):
        for crisis in cls._DATA:
            if crisis.trigger == trigger and crisis.condition_check(actor, target):
                return crisis

    def __init__(self, trigger, source, condition_check):
        self.trigger = trigger
        self.source = source
        self.condition_check = condition_check


class MerCrisisSystem(object):
    _PASSED_CRISIS_DATA = {}

    def __init__(self, person):
        self.person = person
        if self._PASSED_CRISIS_DATA.get(person) is None:
            self._PASSED_CRISIS_DATA[person] = []
            self._TRIGGERED_CRISIS_DATA[person] = []

    def trigger_crisis(self, crisis):
        renpy.call_in_new_context('lbl_crisis_menu_glue', crisis, self)

    def is_passed_crisis(self, crisis):
        return crisis in self._PASSED_CRISIS_DATA[self.person]

    def check_crisis(self, actor, trigger):
        print(trigger)
        crisis = MerCrisis.find_by_trigger(trigger, actor, self.person)
        if not self.is_passed_crisis(crisis):
            return crisis
        return None

    def fulfill_crisis(self, crisis):
        self._PASSED_CRISIS_DATA[self.person].append(crisis)


class MerCrisisRoute(object):

    _DATA = []

    @classmethod
    def register_route(cls, route):
        cls._DATA.append(route)

    @classmethod
    def get_by_crisis(cls, crisis):
        return [i for i in cls._DATA if i.crisis == crisis]

    @classmethod
    def add_route(cls, route):
        cls._DATA.append(route)

    def __init__(self, crisis, name, label):
        self.crisis = crisis
        self.label = label
        self.name = name

    def go_to_route(self, player, person):
        return renpy.call_in_new_context(self.label, player=player, person=person, crisis=self.crisis)
