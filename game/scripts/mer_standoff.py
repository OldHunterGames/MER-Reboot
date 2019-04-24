import random

from mer_basics import suits_value, Suits

class Standoff(object):

    def __init__(self, player_combatant, enemy,):
        self.player_combatant = player_combatant
        self.enemy = enemy
        self.enemy_cards = enemy.get_cards('combat')
        if self.player_combatant.get_sabotage() is not None:
            self.enemy_cards.append(self.player_combatant.get_sabotage())
        self.player_cards = player_combatant.get_cards('combat')
        if self.enemy.get_sabotage() is not None:
            self.player_cards.append(self.enemy.get_sabotage())
        self.player_current_card = None
        self.enemy_current_card = self.next_enemy_card()
        self.winner = None
        self.calc_winner()
        self.message = None

    def is_player_win(self):
        return self.winner == self.player_combatant

    def next_enemy_card(self):
        try:
            card = random.choice(self.enemy_cards)
        except IndexError:
            card = None
        return card

    def calc_winner(self):
        if len(self.enemy_cards) < 1:
            self.winner = self.player_combatant
            self.loser = self.enemy
            return
        if len(self.player_cards) < 1:
            self.winner = self.enemy
            self.loser = self.player_combatant

    def select_card(self, card):
        self.player_current_card = card
        self.calc()

    def enemy_lost_card(self):
        self.enemy_cards.remove(self.enemy_current_card)
        self.enemy_current_card = self.next_enemy_card()

    def clear_message(self):
        self.message = None

    def calc(self):
        self.calc_winner()
        if self.winner is not None:
            return

        player_suit, enemy_suit = suits_value(
            self.player_current_card.suit(self.player_combatant, {}),
            self.enemy_current_card.suit(self.enemy, {})
        )
        self.message = 'fail'
        
        if player_suit > enemy_suit:
            self.enemy_lost_card()
            self.message = 'success'
        elif player_suit == enemy_suit:
            player_power = self.player_current_card.get_power(self.player_combatant, {})
            enemy_power = self.enemy_current_card.get_power(self.enemy, {})
            if player_power > enemy_power:
                self.enemy_lost_card()
                self.message = 'success'

        self.player_cards.remove(self.player_current_card)
        self.player_current_card = None
        self.calc_winner()

