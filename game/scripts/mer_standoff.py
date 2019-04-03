from mer_command import Command
from mer_basics import suits_value

class Standoff(Command):

    def __init__(self, player_combatant, player_action, enemy, enemy_action):
        self.player_combatant = player_combatant
        self.player_action = player_action
        self.enemy = enemy
        self.enemy_action = enemy_action
        self.winner = None
        self.messages = []
        self.results = []
        self.index = 0
        self.counter = 0

    def is_player_win(self):
        return self.winner == self.player_combatant

    def run(self):
        player_value, enemy_value = suits_value(self.player_action.suit, self.enemy_action.suit)
        if player_value > enemy_value:
            self.results.append(1)
            self.messages.append('Advantage. {0} is effective against {1}'.format(self.player_action.suit, self.enemy_action.suit))
        elif enemy_value > player_value:
            self.results.append(-1)
            self.messages.append('Vulnerability. {0} is not effective against {1}'.format(self.player_action.suit, self.enemy_action.suit))
        player_power = self.player_action.power(self.player_combatant)
        enemy_power = self.enemy_action.power(self.enemy)
        if player_power > enemy_power:
            player_value += 1
            self.results.append(1)
            self.messages.append('Advantage. Your attack is more powerful')
        elif enemy_power > player_power:
            player_value -= 1
            self.results.append(-1)
            self.messages.append('Vulnerability. Your attack is weaker')
        enemy_class = self.enemy.person_class.tier if self.enemy_action.suit != 'skull' else 0
        ally_class = self.player_combatant.person_class.tier if self.player_action.suit != 'skull' else 0
        if enemy_class > ally_class:
            player_value -= 1
            self.results.append(-1)
            self.messages.append('Advantage. Your class is worse')
        elif ally_class > enemy_class:
            player_value += 1
            self.results.append(1)
            self.messages.append('Advantage. Your class is better')
        print(self.messages)
        print(self.results)
        if player_value > self.enemy.person_class.tier:
            self.winner = self.player_combatant
        else:
            self.winner = self.enemy

    def update_counter(self):
        self.counter += self.results[self.index]
        self.index += 1

