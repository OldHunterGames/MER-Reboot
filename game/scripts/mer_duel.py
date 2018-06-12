# -*- coding: UTF-8 -*-
import random
import renpy.store as store
import renpy.exports as renpy

from mer_command import Command


class CoreDuelSuit(object):

    ACTION_GET = 'get_card'
    ACTION_DROP = 'drop_card'
    _SUITS = dict()

    @classmethod
    def register_suit(cls, id, suit):
        cls._SUITS[id] = suit

    @classmethod
    def get_suit(cls, id):
        return cls._SUITS[id]

    @classmethod
    def get_suits(cls):
        return cls._SUITS.values()

    def __init__(self, id, data):

        self.id = id
        self.data = data

    def action(self):
        return self.data.get('action')

    def name(self):
        return self.data.get('name', 'No name')

    def beats(self):
        return self.data.get('beats')



class CoreDuelCard(object):

    _CARDS = dict()

    @classmethod
    def random_card(cls):
        return random.choice(cls._CARDS.values())

    @classmethod
    def register_card(cls, id, card):
        cls._CARDS[id] = card

    def __init__(self, id, data):
        self.data = data
        self.id = id

    def name(self):
        return self.data.get('suit').name()

    def action(self):
        return self.data.get('suit').action()

    def is_stronger_than(self, card):
        return card.id in self.data.get('suit').beats()


class CoreDuel(object):

    INITIAL_CARDS = 5
    PLAYER_WIN, PLAYER_LOOSE = range(2)

    def __init__(self, player, person):
        self.player = player
        self.person = person
        self.cards = dict()
        self.played_cards = dict()
        self.max_cards = dict()

    def start(self, return_result=False):
        self.init_cards()
        self.person_play_card()
        self.get_card(self.person)
        renpy.call_in_new_context('lbl_core_duel', duel=self)
        if return_result:
            return self.result

    def init_cards(self):
        self.cards[self.player] = [CoreDuelCard.random_card() for i in range(self.INITIAL_CARDS)]
        self.cards[self.person] = [CoreDuelCard.random_card() for i in range(self.INITIAL_CARDS)]
        player_might = self.player.attribute('might')
        person_might = self.person.attribute('might')
        if player_might > person_might:
            difference = player_might - person_might
            while difference > 0 and len(self.cards[self.person]) > 1:
                self.cards[self.person] = self.cards[self.person][0:len(self.cards[self.person])-1]
                difference -= 1
        elif player_might < person_might:
            difference = person_might - player_might
            while difference > 0 and len(self.cards[self.player]) > 1:
                self.cards[self.player] = self.cards[self.player][0:len(self.cards[self.player])-1]
                difference -= 1
        self.max_cards[self.player] = len(self.cards[self.player])
        self.max_cards[self.person] = len(self.cards[self.person])
        self.played_cards[self.player] = None

    def get_card(self, who):
        if len(self.cards[who]) < self.max_cards[who]:
            self.cards[who].append(CoreDuelCard.random_card())

    def drop_card(self, who):
        if len(self.cards[who]) > 0:
            if who == self.player:
                cards = [i for i in self.cards[who]]
                random.shuffle(cards)
                card = renpy.call_in_new_context('lbl_duel_drop_card', cards[0:2])
            else:
                card = random.choice(self.cards[who])
            self.cards[who].remove(card)

    def player_play_card(self, card):
        if self.played_cards[self.player] is not None:
            self.cards[self.player].append(self.played_cards[self.player])
        self.played_cards[self.player] = card
        self.cards[self.player].remove(card)

    def person_play_card(self):
        self.played_cards[self.person] = random.choice(self.cards[self.person])
        self.cards[self.person].remove(self.played_cards[self.person])

    def card_effect(self, card, user):
        if card.action() == CoreDuelSuit.ACTION_GET:
            self.get_card(user)
        if card.action() == CoreDuelSuit.ACTION_DROP:
            if user == self.player:
                dropper = self.person
            else:
                dropper = self.player
            self.drop_card(dropper)

    def get_round_winner(self):
        if self.played_cards[self.player].is_stronger_than(self.played_cards[self.person]):
            for card in self.played_cards.values():
                self.card_effect(card, self.player)
        else:
            for card in self.played_cards.values():
                self.card_effect(card, self.person)
        self.played_cards[self.player] = None
        self.new_turn()

    def new_turn(self):
        if len(self.cards[self.player]) < 1:
            self.end(looser=self.player)
        elif len(self.cards[self.person]) < 1:
            self.end(looser=self.person)

        self.person_play_card()
        self.get_card(self.person)
        self.get_card(self.player)

    def end(self, looser):
        if looser == self.player:
            renpy.call_in_new_context('lbl_core_duel_end', text='You loose')
            self.result = self.PLAYER_LOOSE
        else:
            renpy.call_in_new_context('lbl_core_duel_end', text='%s loose' % self.person.name)
            self.result = self.PLAYER_WIN
        renpy.return_statement()
        