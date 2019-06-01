﻿# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

init -10 python:
    sys.path.append(renpy.loader.transfn("scripts"))
    # sys.path.append(renpy.loader.transfn("scripts/person"))
    # sys.path.append(renpy.loader.transfn("core"))
    from mer_person import *
    from mer_angel import *
    from mer_utilities import *
    from mer_core import *
    from mer_command import *
    from mer_sparks_festival import *
    from mer_sexuality import *
    from mer_duel import *
    from mer_class import *
    from mer_legacy_system import CoreRiteOfLegacy
    from mer_basics import *

init 1 python:
    for key, value in core_features.items():
        CoreFeature.register_feature(key, CoreFeature(key, value))

    for key, value in core_physical_features.items():
        CoreFeature.register_feature(key, CoreFeature(key, value))

    for key, value in core_alignment_features.items():
        CoreFeature.register_feature(key, CoreFeature(key, value))

    for key, value in core_age_features.items():
        CoreFeature.register_feature(key, CoreFeature(key, value))

    for key, value in core_homeworld_features.items():
        CoreFeature.register_feature(key, CoreFeature(key, value))
    
    for key, value in core_profession_features.items():
        CoreFeature.register_feature(key, CoreFeature(key, value))
    
    for key, value in core_family_features.items():
        CoreFeature.register_feature(key, CoreFeature(key, value))

    for key, value in sex_cards_data.items():
        CoreSexCard.register_card(key, CoreSexCard(key, value))

    for key, value in sexual_types_data.items():
        SexualType.register_type(key, SexualType(key, value))

    for key, value in sexual_orientations_data.items():
        SexualOrientation.register_orientation(key, SexualOrientation(key, value))

    for key, value in core_duel_suits_data.items():
        CoreDuelSuit.register_suit(key, CoreDuelSuit(key, value))

    for key, value in mer_class_data.items():
        PersonClass.register_class(key, value)

    for suit in CoreDuelSuit.get_suits():
        data = {'suit': suit}
        CoreDuelCard.register_card(suit.id, CoreDuelCard(suit.id, data))

    def make_gladiator(allowed_classes=None, person_generator_params=None, min_tier=0, max_tier=5):
        if person_generator_params is None:
            person_generator_params = {}
        while True:
            gladiator = PersonCreator.gen_person(genus='human', **person_generator_params)
            if allowed_classes is not None:
                classes = allowed_classes
            else:
                classes = PersonClass.pipe_filters(PersonClass.class_filter, PersonClass.gender_filter)(
                   gladiator, PersonClass.get_by_tag('gladiator'))
                classes = [i for i in classes if i.tier >= min_tier and i.tier <= max_tier]
            classes_to_give = []
            for i in classes:
                if gladiator.attribute(i.key_attributes[0]) >= i.tier:
                    classes_to_give.append(i)
            if len(classes_to_give) < 1:
                continue
            gladiator.person_class = random.choice(classes_to_give)

            return gladiator

        return gladiator
    
    def make_mudfight_gladiator():
        return make_gladiator(PersonClass.get_by_ids(['lucator']), {'gender': 'female'})
    
    def make_whipfight_gladiator():
        return make_gladiator(PersonClass.get_by_ids(['andabant']), {'gender': 'female'})
    
    def make_pitfight_gladiator():
        return make_gladiator(PersonClass.get_by_ids(['pugilist']), {'gender': 'male'})
    
    def make_gladiator_fit_raiting(low, high, calculator, max_tier=5):
        min_tier = 0
        def inner():
            while True:
                if low >= 30:
                    min_tier = 2
                if low >= 100:
                    min_tier = 3
                glad = make_gladiator(min_tier=min_tier, max_tier=max_tier)
                price = calculator(glad).training_price()
                if price >= low and price <= high:
                    return glad
        return inner
    
    def make_champion():
        return make_gladiator(PersonClass.get_by_tag('gladiator', PersonClass.get_by_tier(5)))
    
    def default_arena_prize(arena):
        sparks = arena.enemy.person_class.tier * 5
        if arena.fight.is_player_win():
            sparks *= 2
        return sparks
    
    def lupanarium_prize(arena):
        if arena.fight.is_player_win():
            prize = 15
        else:
            value = arena.fight.player_combatant.attribute('charisma')
            if value < 0:
                prize = 1
            else:
                prize = 5 + 5 * value
        if arena.fight.player_combatant.person_class == PersonClass.get_by_id('lucator'):
            prize += 5
        return prize
    
    def whipfight_prize(arena):
        return PriceCalculator(arena.enemy).training_price()
    
    def filter_equipment(card):
        return card.type != 'equipment'

init python:
    class FighterSelector(object):
        def __init__(self, player, arena_maker, exclude=None, team=None, start_text=__('select')):
            self.player = player
            self.index = 0
            self.arena_maker = arena_maker
            self.escaped = False
            self.exclude = exclude or []
            self.team = team or []
            self.start_text = start_text
        
        @property
        def enemy(self):
            return self.arena_maker.current_enemy

        def escape(self):
            self.escaped = True

        def run(self):
            return renpy.call_screen('sc_select_fighter', self)

        @property
        def fighters(self):
            if len(self.team) > 0:
                return self.team
            return [i for i in self.arena_maker.filter_fighters(self.player) if i not in self.exclude]

        def current_fighter(self):
            if self.escaped:
                return None
            return self.fighters[self.index]

        def next(self):
            self.index += 1
            if self.index >= len(self.fighters):
                self.index = 0

        # def prev(self):
        #     self.index -= 1

        # def next_active(self):
        #     return self.index < len(self.fighters) - 1

        # def prev_active(self):
        #     return self.index > 0


    class FuncCommand(object):
        def __init__(self, func, *args):
            self.func = func
            self.args = list(args)

        def add_arg(self, arg):
            self.args.append(arg)

        def run(self):
            self.func(*self.args)

    class HomeManager(object):
        MAX_SLAVES = 5
        def __init__(self, player):
            self.player = player
            self.current_slave = None
            self.core = core
            self.should_skip_turn = False
            self.mode = 'stats'
            self.cards_mode = 'combat'
        
        def get_cards(self):
            cards = self.current_slave.get_cards(self.cards_mode)
            cards.extend(self.current_slave.get_cards(self.cards_mode, get_support=True))
            return cards
        
        def show_cards(self, mode):
            self.cards_mode = mode
        
        def switch_mode(self, value):
            self.mode = value

        def calc_upkeep(self):
            return 5 + len(self.player.slaves) * 5

        def on_skip_turn(self, *args, **kwargs):
            self.player.sparks -= self.calc_upkeep()

        @property
        def slaves(self):
            return [i for i in self.player.slaves]

        def select(self, slave):
            self.current_slave = slave

        def call(self):
            renpy.call_screen('sc_home', self)
            self.current_slave = None

        def skip_turn(self):
            self.should_skip_turn = True

        def can_upgrade_slave(self, person):
            exhausted = person.exhausted
            if person.person_class.tier == 1:
                return self.player.person_class.tier > 1 and not exhausted
            else:
                arena_winner = getattr(person, 'win_arena', False)
                tier = self.player.person_class.tier > person.person_class.tier 
                upgrades = len(PersonClass.available_upgrades(person)) > 0
                return arena_winner and tier and upgrades and not exhausted

        def slave_upgrades(self, person):
            return PersonClass.available_upgrades(person)

        def upgrade_slave(self, slave, person_class):
            slave.person_class = person_class
            self.player.sparks -= person_class.cost
            slave.exhausted = True
            if getattr(slave, 'win_arena', False) and person_class.tier == 2:
                return
            slave.win_arena = False

        def can_make_love(self, person1, person2):
            return person1.gender != person2.gender and not person1.exhausted and not person2.exhausted

        def make_love(self, person1, person2):
            person1.grove = True
            person2.grove = True
            person1.set_temporary_card(PersonClassCard.get_card('satisfaction', person2), 'love')
            person2.set_temporary_card(PersonClassCard.get_card('satisfaction', person1), 'love')
            if person1.get_relation('lover') is not None and person1.get_relation('lover') != person2 and person1 != self.player and person2 != self.player:
                person1.set_temporary_card(PersonClassCard.get_card('betrayal', person1.get_relation('lover')), 'sabotage')
            person1.add_relation('lover', person2)
            person1.exhausted = True
            person2.exhausted = True

        def can_attend_party(self, person1, person2):
            return person1.gender == person2.gender and not person1.exhausted and not person2.exhausted

        def persons_for_selection(self, checker):
            persons = [i for i in self.slaves if i != self.current_slave]
            persons.append(self.player)
            return [i for i in persons if checker(self.current_slave, i)]

        def attend_party(self, person1, person2):
            person1.grove = True
            person2.grove = True
            person1.set_temporary_card(PersonClassCard.get_card('bravado', person2), 'fellowship')
            person2.set_temporary_card(PersonClassCard.get_card('bravado', person1), 'fellowship')
            person1.add_relation('best_friend', person2)
            person1.exhausted = True
            person2.exhausted = True

        def can_train(self, slave):
            if self.current_slave == self.player:
                return False
            cards = self.player.get_cards('combat', True)
            return not slave.exhausted and not self.player.exhausted and len(cards) > 0

        def train(self, slave):
            print([i.id for i in self.player.get_cards('combat', True)])
            slave.set_temporary_card(random.choice(self.player.get_cards('combat', True)), 'support')
            self.player.exhausted = True
        
        def can_sell(self, slave):
            return not slave.exhausted and slave != self.player
        
        def sell(self, slave):
            self.player.slaves.remove(slave)
            self.player.sparks += PriceCalculator(slave).price()
            self.current_slave = None
        
        def slave_actions(self):
            renpy.call_in_new_context('lbl_slave_actions', self.current_slave)

    class SimpleSelector(object):
        def __init__(self, items, on_select):
            self._items = items
            self.on_select_command = on_select
        
        @property
        def items(self):
            try:
                items = self._items()
            except TypeError:
                items = self._items
            return items

        def select(self, item):
            self.on_select_command.add_arg(item)
            self.on_select_command.run()

        def show(self):
            return renpy.show_screen('sc_simple_selector', selector=self)
    
    class PriceCalculator(object):
        _RAITINGS = defaultdict(int)
        _WINS = defaultdict(dict)
        attrs_table = {
            0: 0,
            1: 1,
            2: 5,
            3: 10,
            4: 20,
            5: 50,
        }
        
        def __init__(self, person):
            self.person = person
        
        def add_win(self):
            if self._WINS[self.person].get(self.person.person_class.id) is not None:
                self._WINS[self.person][self.person.person_class.id] += 1
            else:
                self._WINS[self.person][self.person.person_class.id] = 1
            
        def current_class_wins(self):
            return self._WINS[self.person].get(self.person.person_class.id, 0)
        
        def total_wins(self):
            if len(self._WINS[self.person].values()) > 0:
                return sum(self._WINS[self.person].values())
            return 0
        
        def add_raiting(self, value):
            self._RAITINGS[self.person] += value - self._rating_modifier()
        
        def potential_price(self):
            price = 0
            for value in self.person.attributes().values():
                price += self.attrs_table.get(value, -10)
            price += self.attrs_table.get(self.person.soul_level, -10)
            return price
        
        def training_price(self):
            price = 0
            for card in self.person.get_cards('combat', get_temporary=False):
                suit = card.suit(self.person)
                if suit == Suits.SKULL:
                    price += card.get_power(self.person)
                elif suit == Suits.JOKER:
                    price += 100
                else:
                    price += 10 + 5 * card.get_power(self.person)
            return price
        
        def raiting_price(self):
            return self._RAITINGS.get(self.person, 0)
        
        def _rating_modifier(self):
            return self.raiting_price() / 20
        
        def price(self):
            return max(5, max(self.potential_price(), self.training_price(), self.raiting_price()))
        
        def entertainment_raiting_formula(self):
            return self.training_price() * self.person.person_class.tier ** 2
    
    class MarketDescription:
        def __init__(self, person):
            self.person = person
        
        def make_description(self):
            top_attr = self.person.max_attribute()
            gender = self.person.gender
            attr = slavemarket_attribute[gender][top_attr]
            genderage = slavemarket_genderage[gender][self.person.age]
            world = self.person.feature_by_slot('homeworld') and self.person.feature_by_slot('homeworld').market_description
            profession = self.person.feature_by_slot('profession') and self.person.feature_by_slot('profession').market_description
            family = self.person.feature_by_slot('family') and self.person.feature_by_slot('family').market_description
            soul = slavemarket_soul[slave.soul_level]
            features = self.features_description()
            price = PriceCalculator(self.person).price()
            return "{name}, {attr} {genderage} {world}. {profession}{family}. {soul}. Особенности: {features} Цена: {price} искр".format(
                name=self.person.name,
                attr=attr,
                genderage=genderage,
                world=world,
                profession=profession,
                family=family,
                soul=soul,
                features=features,
                price=price,
            )
        
        def features_description(self):
            description = ""
            excluded = ['homeworld', 'profession', 'family', 'gender', 'age']
            features = [i for i in self.person.get_features() if i.slot not in excluded]
            for i in features:
                if i.market_description:
                    description += '{0}'.format(i.market_description)
            return description
        
    class Auction(object):
        def __init__(self, core, player):
            self.core = core
            self.player = player
            self.should_show_after_turn = False
        
        def activate(self):
            self.should_show_after_turn = True
        
        def on_skip_turn(self, *args, **kwargs):
            if self.player.sparks < 5 or not self.should_show_after_turn:
                return
            self.should_show_after_turn = False
            renpy.call_in_new_context('lbl_market', player=self.player, core=self.core)
    
    class Triggers(object):

        def __init__(self):
            self.lupanarium_win = False
            self.taberna_win = False
            self.lanista_3 = False
            self.lanista_4 = False
            self.slave_party = False
            self.slave_sex = False
            self.tournament = False

        def lupanarium_first_win(self):
            self.lupanarium_win = True
            renpy.call_in_new_context('lbl_storylanista_luctatorbang')
        
        def taberna_first_win(self):
            self.taberna_first_win = True
            renpy.call_in_new_context('lbl_storylanista_wenchsex')
        
        def lanista_3_level(self):
            self.lanista_3 = True
            renpy.call_in_new_context('lbl_storylanista_coleventpunish')
        
        def lanista_4_level(self):
            self.lanista_4 = True
            renpy.call_in_new_context('lbl_storylanista_sonyabang')
        
        def slave_party_first(self):
            self.slave_party = True
            renpy.call_in_new_context('lbl_storylanista_brobang')
        
        def slave_sex_first(self):
            self.slave_sex = True
            renpy.call_in_new_context('lbl_storylanista_slavesex')
        
        def win_tournamet(self):
            self.tournament = True
            renpy.call_in_new_context('lbl_storylanista_endofstory')

# The game starts here.

label start:
    $ player = PersonCreator.gen_person(name='Player', gender='male', genus='human')
    $ player.person_class = PersonClass.get_by_id('infamous_lanista')
    $ player.armor = Armor.random_by_type(player.person_class.available_garments[0])
    $ player.slaves = []
    $ core = MERCore()
    $ core.player = player
    $ triggers = Triggers()
    # $ core.skip_turn.add_callback(CoreAddCards(player).run)
    # $ core.skip_turn.add_callback(CoreDuel.drop_skulls_callback)
    # $ core.skip_turn.add_callback(CoreSexMinigame.decade_skip_callback)

    python:
        AngelMaker.add_observer('archon_generated', lambda archon: World.get_random_world()(archon))

        slavestore = SlaveMarket(player, PriceCalculator)
        pitfight_classes = PersonClass.get_by_ids(['lucator', 'pugilist', 'menial_slave'])
        heat_up_classes = list(set(PersonClass.get_by_tag('gladiator'))
            .difference(set(PersonClass.get_by_tier(4)))
            .difference(set(PersonClass.get_by_tier(5)))
        )
        enemies = list(set(heat_up_classes).intersection(set(PersonClass.get_by_tier(3))))
        grand_fight_classes = PersonClass.get_by_tag('gladiator')
        available_arenas = {
            'mudfight': MerArenaMaker(make_mudfight_gladiator, lambda person: person.gender == 'female', lupanarium_prize, die_after_fight=False, cards_filter=filter_equipment),
            'whip_fight': MerArenaMaker(make_whipfight_gladiator, lambda person: person.gender == 'female', lupanarium_prize, min_player_level=3, die_after_fight=False),
            'pitfight': MerArenaMaker(
                make_pitfight_gladiator,
                lambda person: person.gender == 'male',
                default_arena_prize,
                die_after_fight=False,
                cards_filter=filter_equipment,
            ),
            'chaotic_fights': MerArenaMaker(
                make_gladiator,
                lambda person: True,
                lambda _: 0,
                die_after_fight=False,
                gain_prestige=False,
                can_skip_enemy=True,
            ),
            'common_fight': MerArenaMaker(
                make_gladiator_fit_raiting(30, 100, PriceCalculator, max_tier=3),
                lambda person: True,
                default_arena_prize,
                min_player_level=2,
            ),
            'premium_fights': MerArenaMaker(
                make_gladiator_fit_raiting(100, 150, PriceCalculator),
                lambda person: True,
                default_arena_prize,
                min_player_level=3,
            ),
            'tournament': MerArenaMaker(
                make_gladiator,
                lambda person: True,
                default_arena_prize,
                min_player_level=4,
            )
        }
        for arena in available_arenas.values():
            core.skip_turn.add_callback(arena.set_gladiator)

        home_manager = HomeManager(player)
        auction = Auction(core, player)
        core.skip_turn.add_callback(auction.on_skip_turn)
        core.skip_turn.add_callback(slavestore.update_slaves)
        core.before_skip_turn.add_callback(home_manager.on_skip_turn)
        # for i in range(10):
        #     test()

    call lbl_make_initial_characters() from _call_lbl_make_initial_characters
    call lbl_storylanista_start
    call lbl_market(core, player)
    call _main from _call__main

    return

label _main:
    show screen sc_main_stats(core, player)
    while True:
        call lbl_main from _call_lbl_main
    return

label lbl_main:
    scene expression 'images/bg/vatican.png'
    menu:
        # 'Me':
        #     $ CharacterInfoScreen(player).show()
        # 'Others':
        #     $ ContactsInfo(core.characters).show()
        # 'Travel to outer worlds':
        #     python:
        #         angel = AngelMaker.gen_archon()
        #         MistTravel(angel.world, player, core).run()
        'Taberna':
            call lbl_taberna()
        'Lupanarium':
            call lbl_lupanarium()
        'Colosseum':
            call lbl_colosseum()
        'Home':
            python:
                home_manager.call()
                if home_manager.should_skip_turn:
                    home_manager.should_skip_turn = False
                    core.skip_turn()
        'Отдыхать':
            python:
                core.skip_turn()
        'Дождаться аукциона':
            $ auction.activate()
            $ core.skip_turn()

    return

# Anton is awesome!
# 01/06/2019 - 17:48

label lbl_slave_actions(slave):
    show expression 'images/bg/empty_room.png'
    show expression im.Scale(slave.avatar, 150, 150) at left
    python:
        icon = 'gui/heart_small.png'
        can_upgrade = home_manager.can_upgrade_slave(slave)
        has_temp = slave.temporary_cards['support'] is not None
        is_all_exhausted = [i.exhausted for i in player.slaves if i != slave]
        is_all_exhausted.append(player.exhausted)
        is_all_exhausted = all(is_all_exhausted)
        description = MarketDescription(slave).make_description()
    while True:
        menu:
            '[description]'
            'Оценка вариантов':
                call lbl_storylanista_actionanalys
            'Продвинутое обучение [[{image=[icon]}]' if can_upgrade:
                python:
                    choice = True
                    while choice:
                        items = [(i.name, i) for i in home_manager.slave_upgrades(slave)]
                        items.append(('Передумать', False))
                        choice = renpy.display_menu(items)
                        if choice:
                            variants = []
                            text = 'Начать тренировки (%s)' % choice.cost
                            if choice.cost <= player.sparks:
                                variants.append((text, choice))
                            else:
                                variants.append((text, None))
                            variants.append(('Передумать', False))
                            renpy.say(None, choice.description, interact=False)
                            next_choice = renpy.display_menu(variants)
                            if next_choice:
                                home_manager.upgrade_slave(slave, next_choice)

            'Продвинутое обучение [[X]' if not can_upgrade:
                python:
                    text = ''
                    if player.person_class.tier <= slave.person_class.tier:
                        text = 'Простите, хозяин, но прежде чем вы сможете готовить более сильных гладиаторов Вам нужно заработать больше опыта и славы. Нужна достойная победа на новой арене.'
                    elif not getattr(slave, 'win_arena', False):
                        text = 'Мне нужно больше боевого опыта прежде чем я смогу выступать с новым снаряжением, Хозяин. Позвольте мне победить хотя бы одного достойного противника.'
                    elif slave.person_class.tier == 5:
                        text = 'Я уже чемпион арены. Более сильных гладиаторов Рим не знал.'
                    
                slave '[text]'
            'Отработать тактику боя' if not has_temp:
                if player.exhausted:
                    player 'Я слишком устал чтобы этим заниматься'
                else:
                    $ home_manager.train(slave)
                    return
            'Оплатить развлечение (5 искр)':
                if is_all_exhausted:
                    slave "Вы очень щедры, Хозяин, но какой смысл развлекаться водиночку? Мне нужна компания, а все уже заняты другими делами на этой декаде."
                else:
                    python:
                        variants = []
                        if not player.exhausted:
                            variants.append((player.name, player))
                        friend = slave.get_relation('best_friend')
                        lover = slave.get_relation('lover')
                        if friend is not None:
                            variants.append(
                                ('{0} (лучший друг'.format(friend.name), fiend if not friend.exhausted else None)
                            )
                        if lover is not None:
                            variants.append(
                                ('{0} (любовник'.format(lover.name), lover if not lover.exhausted else None)
                            )
                        for i in player.slaves:
                            if i != friend and i != lover and i != player and not i.exhausted and i != slave:
                                variants.append((i.name, i))
                        variants.append(('Передумать', False))
                        choice = renpy.display_menu(variants)
                        if choice:
                            if choice.gender == slave.gender:
                                if not triggers.slave_party:
                                    triggers.slave_party_first()
                                home_manager.attend_party(choice, slave)
                            else:
                                if not triggers.slave_sex:
                                    triggers.slave_sex_first()
                                home_manager.make_love(choice, slave)
                    if choice:
                        return
            'Продать на рынке':
                $ home_manager.sell(slave)
                return
            'Закончить разговор':
                return


        
label lbl_market(core, player):
    # scene expression 'images/bg/slavemarket.png'
    show screen sc_main_stats(core, player)
    python:
        slaves = [make_starter_slave() for i in range(5)]
    while len(slaves) > 0:
        python:
            slave = slaves.pop()
            price = PriceCalculator(slave).price()
            buy_action = 'buy' if price <= player.sparks else None
            actions = [('Buy %s sparks' % price, buy_action), ('Skip', 'skip'), ('Leave', 'leave')]
            description = MarketDescription(slave).make_description()
        menu:
            '[description]'
            'Buy' if price <= player.sparks:
                python:
                    player.slaves.append(slave)
                    player.sparks -= price
            'Skip':
                $ pass
            'Leave':
                $ slaves = []
    hide sc_main_stats
    return


label lbl_slave_market():
    $ slavestore.open()
    return

label lbl_lupanarium():
    if not lupaintro:
        $ lupaintro = True
        call lbl_storylanista_lupaintro
    python:
        choices = []
        mudfight = available_arenas['mudfight']
        whip_fight = available_arenas['whip_fight']
        if mudfight.is_active(player):
            choices.append(('Mudfight', mudfight))

        if whip_fight.is_active(player):
            choices.append(('Whip fight', whip_fight))

        choices.append(('Return', 'return'))
        choice = renpy.display_menu(choices)
    if choice == 'return':
        return
    call lbl_arena(choice, location='lupanarium')
    return

label lbl_taberna():
    if not tabernintro:
        $ tabernintro = True
        call lbl_storylanista_tabernintro
    python:
        choices = []
        pitfight = available_arenas['pitfight']
        if pitfight.is_active(player):
            choices.append(('Pitfight', pitfight))

        choices.append(('Return', 'return'))
        choice = renpy.display_menu(choices)
    if choice == 'return':
        return
    call lbl_arena(choice, location='taberna')
    return

label lbl_colosseum():
    if not colintro:
        $ colintro = True
        call lbl_storylanista_colintro
    python:
        choices = []
        chaotic = available_arenas['chaotic_fights']
        common_fight = available_arenas['common_fight']
        premium_fight = available_arenas['premium_fights']
        tournament = available_arenas['tournament']
        if chaotic.is_active(player):
            choices.append(('Chaotic fights', chaotic))

        if common_fight.is_active(player):
            choices.append(('Common fight', common_fight))

        if premium_fight.is_active(player):
            choices.append(('Premium fight', premium_fight))

        if tournament.is_active(player) and len(tournament.filter_fighters(player)) >= 3:
            choices.append(('Tournament', tournament))
    
        choices.append(('Return', 'return'))
        choice = renpy.display_menu(choices)
    if choice == 'return':
        return
    if choice == tournament:
        call lbl_grand_fight(choice)
        return
    call lbl_arena(choice)
    return

label lbl_grand_fight(arena_maker):
    python:
        team = []
        # enemies = [make_gladiator_fit_raiting(30, 100, PriceCalculator, 3)() for i in xrange(2)]
        # enemies.extend([make_gladiator_fit_raiting(100, 150, PriceCalculator)() for i in xrange(2)])
        # enemies.append(make_champion())
        class_ids = ['myrmidon', 'retiarius', 'cenobite', 'dimacheros', 'goplynia', 'secutor']
        enemies = [make_gladiator(allowed_classes=[PersonClass.get_by_id(i)]) for i in class_ids]
        arena_maker.current_enemy = enemies.pop(0)
    'Select you team (3 fighters)'
    python:
        while len(team) < 3:
            selector = FighterSelector(player, arena_maker, team)
            selector.run()
            team.append(selector.current_fighter())
    'Tournament is going to begin'
    python:
        while len(team) > 0 and len(enemies) > 0:
            selector = FighterSelector(player, arena_maker, team=team, start_text=__('Начать бой'))
            selector.run()
            ally = selector.current_fighter()
            arena = MerArena(arena_maker.current_enemy, ally, arena_maker.cards_filter)
            arena.make_bet(ally)
            arena.start()
            fight = arena.fight
            if fight.is_player_win():
                arena_maker.current_enemy = enemies.pop(0)
            else:
                team.remove(ally)
                player.slaves.remove(ally)
        if len(team) > 0:
            player_win = True
        else:
            player_win = False
    'Tournament ended'

    python:
        if player_win:
            player.person_class = PersonClass.get_by_id('famous_lanista')
            for i in team:
                i.after_fight()
                i.win_arena = True
                i.exhausted = True
            if not triggers.tournament:
                triggers.win_tournamet()
    return

label lbl_arena(arena_maker, location=None):
    $ res = None

    python:
        selector = FighterSelector(player, arena_maker, start_text=__('Начать бой'))
        gladiator1 = arena_maker.current_enemy
        selector.run()
        gladiator2 = selector.current_fighter()
        if gladiator2 is not None:
            arena = MerArena(gladiator1, gladiator2, cards_filter=arena_maker.cards_filter)
            arena.make_bet(gladiator2)
            arena.start()
            fight = arena.fight
            result = 'won' if fight.is_player_win() else 'lost'
            fame_changed = False
            gladiator2.exhausted = True
            prize = arena_maker.get_prize(arena)
            player.sparks += prize
            gladiator2.after_fight()
            if result != 'won' and fight.loser != player and arena_maker.die_after_fight:
                player.slaves.remove(gladiator2)
            rule = player.person_class.tier >= 2 and not arena_maker.die_after_fight
            print(rule)
            if result == 'won' and not arena_maker.is_winned and not rule and arena_maker.gain_prestige:
                fame_message = 'Player gain fame'
                fame = arena.raise_fame(PriceCalculator, player)
                fame_changed = fame
                arena_maker.is_winned = fame
                if fame:
                    if location == 'lupanarium' and not triggers.lupanarium_win:
                        triggers.lupanarium_first_win()
                    if location == 'taberna' and not triggers.taberna_win:
                        triggers.taberna_first_win()
                    if player.person_class.tier == 3 and not triggers.lanista_3:
                        triggers.lanista_3_level()
                    if player.person_class.tier == 4 and not triggers.lanista_4:
                        triggers.lanista_4_level()
            if result == 'won':
                arena_maker.set_gladiator()
                gladiator2.win_arena = True
            
            if fight.is_player_win():
                PriceCalculator(gladiator2).add_raiting(fight.enemy_cards_amount ** 2)
            else:
                PriceCalculator(gladiator1).add_raiting(fight.player_cards_amount ** 2)
            # if not fame_changed:
            #     fame_changed = arena.drop_fame(PriceCalculator, player)
            #     fame_message = 'Player lose fame'
    if gladiator2 is None:
        return

    if result != 'won' and arena_maker.die_after_fight:
        'Winner is [fight.winner.name] / player [result]/ [fight.loser.name] is killed'
    else:
        'Winner is [fight.winner.name] / player [result]'
    if fame_changed:
        '[fame_message]'
    'You prize is [prize] sparks'
    python:
        if fight.loser == player:
            renpy.full_restart()
    return


label lbl_make_initial_characters():
    python:
        patricians = [renpy.call_in_new_context('lbl_make_patrician') for i in range(12)]
        free_patricians = [renpy.call_in_new_context('lbl_make_patrician') for i in range(4)]
        senators = [renpy.call_in_new_context('lbl_make_senator') for i in range(6)]
        free_senators =[renpy.call_in_new_context('lbl_make_senator') for i in range(2)]
        nobles = [renpy.call_in_new_context('lbl_make_noble') for i in range(2)]
        free_nobles = [renpy.call_in_new_context('lbl_make_noble') for i in range(2)]
        princeps = renpy.call_in_new_context('lbl_make_princeps', 'serpis')
        for i in senators + free_senators:
            Hierarchy(i).add_clientela(patricians.pop())
        Hierarchy(random.choice(senators)).add_clientela(patricians.pop())
        Hierarchy(random.choice(free_senators)).add_clientela(patricians.pop())
        for i in nobles + free_nobles:
            Hierarchy(i).add_clientela(senators.pop())
        Hierarchy(random.choice(nobles)).add_clientela(senators.pop())
        Hierarchy(random.choice(free_nobles)).add_clientela(senators.pop())
        for i in nobles:
            Hierarchy(princeps).add_clientela(i)
    return 

label lbl_make_patrician():
    python:
        angel = AngelMaker.gen_archon()
        person = PersonCreator.gen_person()
        SetAngelApostol(angel, person).run()
        core.add_character(person)
    return person

label lbl_make_senator():
    python:
        senator = PersonCreator.gen_person()
        angel = AngelMaker.gen_ellochim()
        for i in range(2):
            a = AngelMaker.gen_archon()
            angel.add_angel(a)
            SetAngelApostol(a, senator).run()
        SetAngelApostol(angel, senator).run()
        core.add_character(senator)
    return senator

label lbl_make_noble():
    python:
        noble = PersonCreator.gen_person()
        cherub = AngelMaker.gen_cherub()
        ellohims = [AngelMaker.gen_ellochim() for i in range(2)]
        archons = [AngelMaker.gen_archon() for i in range(4)]
        for i in ellohims:
            cherub.add_angel(i)
            SetAngelApostol(i, noble).run()
        for i in range(2):
            ellohim = ellohims[i]
            for n in archons[i*2: i*2+2]:
                ellohim.add_angel(n)
                SetAngelApostol(n, noble).run()
        SetAngelApostol(cherub, noble).run()
        core.add_character(noble)
    return noble

label lbl_make_princeps(house):
    python:
        princeps = PersonCreator.gen_person()
        seraph = AngelMaker.gen_seraph(house)
        cherubs = [AngelMaker.gen_cherub() for i in range(2)]
        ellohims = [AngelMaker.gen_ellochim() for i in range(4)]
        archons = [AngelMaker.gen_archon() for i in range(8)]
        core.add_character(princeps)
        for i in cherubs:
            SetAngelApostol(i, princeps).run()
            seraph.add_angel(i)
        for i in range(2):
            cherub = cherubs[i]
            for n in ellohims[i*2: i*2+2]:
                cherub.add_angel(n)
                SetAngelApostol(n, princeps).run()
        for i in range(4):
            ellohim = ellohims[i]
            for n in archons[i*2: i*2+2]:
                ellohim.add_angel(n)
                SetAngelApostol(n, princeps).run()
        SetAngelApostol(seraph, princeps).run()
    return princeps


label lbl_successor_challenge_result(winner, looser):
    if winner == player:
        'You win and become peer for [looser.firstname]'
    else:
        'You loose. [winner.firstname] is your peer now'
    return

label lbl_world_dummy(world):
    "Hello to [world.archon.name]'s world"
    $ cost = world.archon.apostol_cost()
    while True:
        if cost > player.sparks:
            'You have no sparks to sync this world'
        menu:
            'Talk to [world.archon.name]':
                $ AngelInfoScreen(world.archon, show_world_btn=False).show()
            'Sync ([cost] sparks)' if world.can_sync():
                python:
                    world.sync()
                "You synced [world.archon.name]'s world"
            'Back to Rome':
                return


label lbl_gameover():
    'You are broke'
    'GAME OVER'
    $ renpy.full_restart()
    return

label lbl_world_return():
    # This is needed to safely return from any outer world via world.leave method
    $ depth = renpy.context_nesting_level()
    if depth > 1:
        $ renpy.jump_out_of_context('lbl_world_return')
    else:
        $ renpy.set_return_stack([])
    return