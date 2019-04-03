from mer_command import Command
from mer_basics import suits_value, Suits

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
        self._calc_suits()
        self._calc_power()
        self._calc_class()
        self._calc_armor()
        
        result = sum(self.results) if len(self.results) > 0 else 0

        if result > self.enemy.person_class.tier:
            self.winner = self.player_combatant
        else:
            self.winner = self.enemy

    def update_counter(self):
        self.counter += self.results[self.index]
        self.index += 1

    def _calc_suits(self):
        player_value, enemy_value = suits_value(self.player_action.suit, self.enemy_action.suit)
        if player_value > enemy_value:
            self.results.append(1)
            self.messages.append('Advantage. {0} is effective against {1}'.format(
                Suits.as_attack_type(self.player_action.suit),
                Suits.as_attack_type(self.enemy_action.suit)
            ))
        elif enemy_value > player_value:
            self.results.append(-1)
            self.messages.append('Vulnerability. {0} is not effective against {1}'.format(
                Suits.as_attack_type(self.player_action.suit),
                Suits.as_attack_type(self.enemy_action.suit)
            ))

    def _calc_power(self):
        player_power = self.player_action.power(self.player_combatant)
        enemy_power = self.enemy_action.power(self.enemy)
        if player_power > enemy_power:
            self.results.append(1)
            self.messages.append('Advantage. Your attack is more powerful')
        elif enemy_power > player_power:
            self.results.append(-1)
            self.messages.append('Vulnerability. Your attack is weaker')

    def _calc_class(self):
        enemy_class = self.enemy.person_class.tier if self.enemy_action.suit != 'skull' else 0
        ally_class = self.player_combatant.person_class.tier if self.player_action.suit != 'skull' else 0
        if enemy_class > ally_class:
            self.results.append(-1)
            self.messages.append('Advantage. Your class is worse')
        elif ally_class > enemy_class:
            self.results.append(1)
            self.messages.append('Advantage. Your class is better')

    def _calc_armor(self):
        ally_armor = self.player_combatant.armor.calc_bonus({'standoff_type': 'combat', 'suit': self.enemy_action.suit})
        enemy_armor = self.enemy.armor.calc_bonus({'standoff_type': 'combat', 'suit': self.player_action.suit})

        if ally_armor > 0:
            self.results.append(1)
            self.messages.append('Advantage. Good armor')
        elif ally_armor < 0:
            self.results.append(-1)
            self.messages.append('Vulnerability. Bad armor')

        if enemy_armor > 0:
            self.results.append(-1)
            self.messages.append('Vulnerability. Enemy has good armor')
        elif enemy_armor < 0:
            self.results.append(1)
            self.messages.append('Advantage. Enemy has bad armor')
