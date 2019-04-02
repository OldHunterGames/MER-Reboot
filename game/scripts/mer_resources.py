from collections import defaultdict


class BasicResource(object):

    def __init__(self, name):
        self.name = name
        self.values = defaultdict(int)

    def change_value(self, person, value):


class Material(object):

    def __init__(self, id, name,)


class ResourceManager(object):

    def __init__(self, basic_resource_name):

        self._basic_resource = basic_resource_name
        self._basic_resource_values = defaultdict(int)

        self._materials = defaultdict(list)
        self._products = defaultdict(list)

    def basic_resource_name(self):
        return self._basic_resource

    def basic_resource_value(self, person):
        self._basic_resource_values[person]

    def change_basic_resource(self, person, value):
        self._basic_resource_values[person] += value

