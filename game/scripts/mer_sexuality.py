# -*- coding: UTF-8 -*-
import random
import renpy.store as store
import renpy.exports as renpy

from mer_command import Command


class SexualType(object):

    _SEX_TYPES = dict()

    @classmethod
    def register_type(cls, id, sex_type):
        cls._SEX_TYPES[id] = sex_type

    @classmethod
    def get_type(cls, id):
        return cls._SEX_TYPES[id]

    @classmethod
    def random_type(cls):
        return random.choice(cls._SEX_TYPES.values())

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


class SexualOrientation(object):

    _SEX_ORIENTATIONS = dict()

    @classmethod
    def register_orientation(cls, id, sex_orientation):
        cls._SEX_ORIENTATIONS[id] = sex_orientation

    @classmethod
    def get_type(cls, id):
        return cls._SEX_ORIENTATIONS[id]

    @classmethod
    def random_orientation(cls):
        return random.choice(cls._SEX_ORIENTATIONS.values())

    def __init__(self, id, data):
        self.id = id
        self.data = data

    def like(self, person):
        return self.data.get(person.gender) > 0

    def name(self):
        return self.data.get('name', 'No name')

    def description(self):
        return self.data.get('description', 'No description')


class CorePersonSexuality(object):

    def __init__(self, *args, **kwargs):
        self._sexual_type = SexualType.random_type()
        self._sexual_orientation = SexualOrientation.random_orientation()
        self.fetishes = set()
        self.taboos = set()
        self.deck = CoreSexDeck()
        self.make_initial_cards()

    @property
    def sexual_type(self):
        return self._sexual_type

    @property
    def sexual_orientation(self):
        return self._sexual_orientation

    @sexual_orientation.setter
    def sexual_orientation(self, value):
        self._sexual_orientation = value

    @sexual_type.setter
    def sexual_type(self, value):
        self._sexual_type = value
        self.make_initial_cards()

    def interaction_value(self, activity, type):
        if self.sexual_type is None:
            return 0
        return self.sexual_type.interaction_value(activity, type)

    def make_initial_cards(self):
        cards = CoreSexCard.get_cards()
        for card in cards:
            value = self.interaction_value(card.activity(), card.type())
            value += 2
            for i in range(value):
                self.deck.add_card(card)

    def attractivness(self, person):
        # Temporary return person charm as attractivness
        return 3
        return person.attribute('charisma')

        features = {i.id for i in person.get_features()}
        if not features.isdisjoint(self.taboos):
            return 0
        if not self._sexual_orientation.like(person):
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
        self.value = 0

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


class CoreSexMinigame(object):

    NPC_WIN, PLAYER_WIN = range(2)

    def __init__(self, player, person):
        self.player = player
        self.person = person
        self.player_played_cards = list()

    def can_start(self):
        return self.player.sexuality.attractivness(self.person) > 0 and \
            self.person.sexuality.attractivness(self.player) > 0

    @property
    def person_pleasure(self):
        return max(0, min(5, self._calc_person_pleasure()))

    def calc_bonus(self, cards):
        value = 0
        bonuses = dict()
        for card in cards:
            if card.type() in bonuses:
                if card.activity() not in bonuses[card.type()]:
                    value += 1
                else:
                    bonuses[card.type()].append(card.activity())
            else:
                bonuses[card.type()] = [card.activity()]
        return value

    def _calc_person_pleasure(self):
        total = 0
        for card in self.player_played_cards:
            if self.person.sexuality.interaction_value(card.activity(), card.type()) > 0:
                total += 1
            else:
                total -= 1
        total += self.calc_bonus(self.player_played_cards)
        return total

    def _calc_player_pleasure(self):
        total = 0
        for card in self.person_cards:
            if self.player.sexuality.interaction_value(card.activity(), card.type()) > 0:
                total += 1
            else:
                total -= 1
        total += self.calc_bonus(self.person_cards)
        return total

    @property
    def player_pleasure(self):
        return max(0, min(self._calc_player_pleasure(), 5))

    def start(self, return_result=False):
        self.player_card_slots = self.player.sexuality.attractivness(self.person)
        self.person_card_slots = self.person.sexuality.attractivness(self.player)
        person_cards = self.person.sexuality.deck.get_cards()
        random.shuffle(person_cards)
        self.person_cards = person_cards[0:self.person_card_slots]
        renpy.call_in_new_context('lbl_sex_minigame', sex_game=self)
        if self._calc_person_pleasure() <= self._calc_player_pleasure():
            result = self.NPC_WIN
            renpy.call_in_new_context('lbl_sex_minigame_end', text='You came first - you lose')
        else:
            result = self.PLAYER_WIN
            renpy.call_in_new_context('lbl_sex_minigame_end', text='%s came first - you win' % self.person.name)
        if return_result:
            return result

    def get_card_slots(self):
        slots = list()
        for i in range(self.player_card_slots):
            try:
                card = self.player_played_cards[i]
            except IndexError:
                card = None
            slots.append(card)
        return slots

    def can_play(self):
        return any([i is None for i in self.get_card_slots()])

    def get_player_hand(self):
        return self.player.sexuality.deck.get_hand()

    def play_card(self, card):
        self.player.sexuality.deck.remove_from_hand(card)
        self.player_played_cards.append(card)

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