# -*- coding: UTF-8 -*-
import random
import renpy.store as store
import renpy.exports as renpy

from mer_command import Command


class SexualType(object):

    def __init__(self, id, data):
        self.id = id
        self.data = data

    def name(self):
        return self.data.get('name', 'No name')

    def description(self):
        return self.data.get('description', 'No description')

    def interaction_value(self, activity, type):
        return self.data[activity][type]

    def evolution(self):
        return self.data.get('evolution', list())


class CorePersonSexuality(object):

    def __init__(self, *args, **kwargs):
        self._sexual_type = None
        self.fetishes = set()
        self.taboos = set()
        self.deck = CoreSexDeck()
        self.make_initial_cards()

    @property
    def sexual_type(self):
        return self._sexual_type

    @sexual_type.setter
    def sexual_type(self, value):
        self._sexual_type = value
        self.make_initial_cards()

    def interaction_value(self, activity, type):
        if self.sexual_type is None:
            return 0
        return self.sexual_type.intersection_value(activity, type)

    def make_initial_cards(self):
        cards = CoreSexCard.get_cards()
        for card in cards:
            value = self.interaction_value(card.activity(), card.type())
            value += 2
            for i in range(value):
                self.deck.add_card(card)

    def attractivness(self, person):
        # Temporary return person charm as attractivness
        return person.attribute('charisma')

        features = {i.id for i in person.get_features()}
        if not features.isdisjoint(self.taboos):
            return 0
        value = 0

        return value + len(features.intersection(self.fetishes))

    def add_fetish(self, feature):
        self.fetishes.add(feature.id)

    def add_taboo(self, feature):
        self.taboos.add(feature.id)

    def remove_fetish(self, feature):
        self.fetishes.remove(feature.id)

    def remove_taboo(self, feature):
        self.taboos.remove(feature.id)


class CoreSexCard(object):

    CARDS = dict()

    @classmethod
    def register_card(cls, id, card):
        cls.CARDS[id] = card

    @classmethod
    def get_card(cls, id):
        return cls.CARDS[id]

    @classmethod
    def get_cards(cls):
        return [i for i in cls.CARDS.values()]

    def __init__(self, id, data):
        self.id = id
        self.data = data

    def activity(self):
        return self.data['activity']

    def type(self):
        return self.data['type']


class CoreSexDeck(object):

    def __init__(self):
        self._cards = list()
        self._hand = list()

    def get_cards(self):
        return [i for i in self._cards]

    def get_hand(self):
        return [i for i in self._hand]

    def add_card(self, card):
        self._cards.append(card)

    def add_to_hand(self, card):
        self._cards.remove(card)
        self._hand.append(card)

    def remove_from_hand(self, card):
        self._hand.remove(card)
        self._cards.append(card)

    def max_hand_length(self):
        return 5

    def initial_hand_length(self):
        return 3


class CoreSexMiniGame(object):

    def __init__(self, person1, person2):
        self.person1 = person1
        self.person2 = person2


class CoreAddCards(Command):

    class CardsPicker(object):

        def __init__(self, cards):
            self.cards = cards
            self.revealed = False

        def reveal(self):
            self.revealed = True

        def call(self):
            return renpy.call_screen('sc_pick_sex_card', picker=self)

    def __init__(self, person):
        self.person = person

    def run(self, *args, **kwargs):
        deck = self.person.sexuality.deck
        hand = deck.get_hand()
        if len(hand) > 4:
            return
        else:
            cards = deck.get_cards()
            random.shuffle(cards)
            cards_to_pick = cards[0:2]
            card = self.CardsPicker(cards).call()
            deck.add_to_hand(card)