# -*- coding: UTF-8 -*-
import random
from collections import defaultdict

import renpy.store as store
import renpy.exports as renpy

from mer_command import Command, SetAngelApostol
from mer_duel import CoreDuel
from mer_sexuality import CoreSexMinigame


class RiteOfLegacyDispute(object):


    def __init__(self, player, person, money):

        self.player = player
        self.person = person
        self.money = money
        self.sex_game = CoreSexMinigame(self.player, self.person)
        self.winner = None

    def start(self):
        renpy.call_in_new_context('lbl_legacy_dispute', dispute=self)
        return self.winner

    def can_accept_person(self):
        return self.person.sparks >= self.money

    def can_raize_player(self):
        return self.player.sparks >= self.money * 2

    def dice_decision(self):
        self.winner = random.choice([self.player, self.person])

    def money_accept(self):
        self.player.sparks += self.money
        self.person.sparks -= self.money
        self.winner = self.person

    def money_raise(self):
        self.player.sparks -= self.money * 2
        self.person.sparks += self.money * 2
        self.winner = self.player

    def fight(self):
        duel = CoreDuel(self.player, self.person)
        result = duel.start(return_result=True)
        if result == CoreDuel.PLAYER_LOOSE:
            self.winner = self.person
        elif result == CoreDuel.PLAYER_WIN:
            self.winner = self.player
        else:
            raise Exception('invalid duel result')

    def can_sex(self):
        return self.sex_game.can_start()

    def sex(self):
        result = self.sex_game.start(return_result=True)
        if result == CoreSexMinigame.PLAYER_WIN:
            self.winner = self.player
        elif result == CoreSexMinigame.NPC_WIN:
            self.winner = self.person


class CoreRiteOfLegacy(object):


    def __init__(self, dead_person, core, festival, hierarchy):
        self.core = core
        self.festival = festival
        self.dead_person = dead_person
        self.hierarchy = hierarchy

    def run(self):
        successors = {successor: 1 for successor in self.dead_person.successors()}
        print(successors)
        angels = self.dead_person.get_host()
        archons = [i for i in angels if i.level() == 3]
        cherubs = [i for i in angels if len(i.ensemble) > 0 and i.level() == 4]
        seraphs = [i for i in angels if len(i.ensemble) > 0 and i.level() == 5]
        print('archons: %s' % archons)
        print('cherubs: %s' % cherubs)
        print('seraphs: %s' % seraphs)
        cherubs_points = {
            kanonarch: defaultdict(int) for kanonarch in cherubs
        }
        seraphs_points = {
            kanonarch: defaultdict(int) for kanonarch in seraphs
        }
        # TODO: archons for leader of house when we'll implement house
        self._distribute_angles(archons, cherubs_points, successors)
        for key, value in cherubs_points.items():
            self.dead_person.remove_angel(key)
            max_points = max(value.values())
            applicants = [person for person, points in value.items() if points == max_points]
            if len(applicants) > 1:
                key.apostol = None
                dead_person.remove_angel(key)
            else:
                SetAngelApostol(key, applicants[0]).run()
                print('%s got angel: %s' % (applicants[0], key))
                if key.kanonarch is not None:
                    seraphs_points[key.kanonarch][applicants[0]] += 1
        for key, value in seraphs_points.items():
            max_points = max(value.values())
            applicants = [person for person, points in value.items() if points == max_points]
            if len(applicants) > 1:
                key.apostol = None
                dead_person.remove_angel(key)
            else:
                SetAngelApostol(key, applicants[0]).run()
                print('%s got angel: %s' % (applicants[0], key))

    def _distribute_angles(self, angels, points, successors):
        for archon in angels:
            if len(successors.keys()) < 2:
                successors.keys()[0].add_angel(archon)
            else:
                applicants = [i[0] for i in sorted(successors.items(), key=lambda x: x[1])][0:2]
                for i in successors.keys():
                    if i not in applicants:
                        successors[i] += 1
                if any([i == self.core.player for i in applicants]):
                    person = [i for i in applicants if i != self.core.player][0]
                    winner = self.dispute(self.core.player, person)
                else:
                    winner = random.choice(applicants)
                print('%s got angel: %s' % (winner, archon))
                SetAngelApostol(archon, winner).run()
                kanonarch = archon.kanonarch
                if kanonarch is not None:
                    try:
                        points[kanonarch][winner] += 1
                    except KeyError:
                        pass

    def dispute(self, player, person):
        price = self.festival.default_bonus(person, self.hierarchy)
        winner = RiteOfLegacyDispute(player, person, price).start()
        return winner




