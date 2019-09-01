chakra_levels = {
    0: [-1, -1, -1, -1, 0, 1, 2],
    1: [-1, -1, -1, 0, 1, 2, 3],
    2: [-1, -1, 0, 1, 2, 3, 4],
    3: [0, 1, 2, 3, 4, 5, 5],
    4: [1, 2, 3, 4, 5, 5, 5],
    5: [2, 3, 4, 5, 5, 5, 5]
}

class Soul:

    def __init__(self):

        self.level = 0
        self.abilities = []

    def add_ability(self, ability):
        self.abilities.append(ability)

    def ability_level(self, ability):
        index = self.abilities.index(ability)
        return chakra_levels[self.level]