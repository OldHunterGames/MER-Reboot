from mer_utilities import Command
from mer_basics import suits_value

class Standoff(Command):

    def __init__(self, player_combatant, player_action, enemy, enemy_action):
        self.player_combatant = player_combatant
        self.player_action = player_action
        self.enemy = enemy
        self.enemy_action = enemy_action

    def run(self):
        player_value, enemy_value = suits_value(self.player_action.suit, self.enemy_action.suit)
        if self.player_action.power > self.enemy_action.power:
            player_value += 1
        else:
            enemy_value += 1
        

