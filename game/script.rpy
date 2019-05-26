# The script of the game goes in this file.

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
                    None, PersonClass.get_by_tag('gladiator'))
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
                glad = make_gladiator(min_tier=min_tier)
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
        def __init__(self, player, arena_maker, exclude=None, team=None):
            self.player = player
            self.index = 0
            self.arena_maker = arena_maker
            self.escaped = False
            self.exclude = exclude or []
            self.team = team or []
        
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

        def prev(self):
            self.index -= 1

        def next_active(self):
            return self.index < len(self.fighters) - 1

        def prev_active(self):
            return self.index > 0


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
            slave.armor = Armor.random_by_type(slave.person_class.available_garments[0])
            self.player.sparks -= person_class.cost
            slave.exhausted = True
            slave.win_arena = False

        def can_make_love(self, person1, person2):
            return person1.gender != person2.gender and not person1.exhausted and not person2.exhausted

        def make_love(self, person1, person2):
            person1.grove = True
            person2.grove = True
            person1.set_temporary_card(PersonClassCard.get_card('satisfaction', person2), 'love')
            person2.set_temporary_card(PersonClassCard.get_card('satisfaction', person1), 'love')
            if person1.get_relation('lover') is not None and person1.get_relation('lover') != person2:
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
            cards = self.player.get_cards('combat', True)
            return not slave.exhausted and not self.player.exhausted and len(cards) > 0

        def train(self, slave):
            print([i.id for i in self.player.get_cards('combat', True)])
            slave.set_temporary_card(random.choice(self.player.get_cards('combat', True)), 'support')
            slave.exhausted = True
            self.player.exhausted = True

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

# The game starts here.

label start:
    $ player = PersonCreator.gen_person(name='Player', gender='male', genus='human')
    $ player.person_class = PersonClass.get_by_id('infamous_lanista')
    $ player.armor = Armor.random_by_type(player.person_class.available_garments[0])
    $ player.slaves = []
    $ core = MERCore()
    $ core.player = player
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
            # 'practice': MerArenaMaker(
            #     make_gladiator,
            #     2,
            #     allowed_classes=[PersonClass.get_by_id('pegniarius')],
            #     sparks=5,
            #     die_after_fight=False
            # ),
            # 'heat_up': MerArenaMaker(
            #     make_gladiator,
            #     3,
            #     allowed_classes=heat_up_classes,
            #     fixed_enemy=enemies,
            #     sparks=15,
            # ),
            # 'grand_fight': MerArenaMaker(
            #     make_gladiator,
            #     4,
            #     allowed_classes=grand_fight_classes,
            #     fixed_enemy=enemies,
            #     sparks=50,
            # ),
        }
        for arena in available_arenas.values():
            core.skip_turn.add_callback(arena.set_gladiator)

        home_manager = HomeManager(player)
        core.skip_turn.add_callback(slavestore.update_slaves)
        core.skip_turn.add_callback(home_manager.on_skip_turn)
        # for i in range(10):
        #     test()

    call lbl_make_initial_characters() from _call_lbl_make_initial_characters
    call lbl_storylanista_start
    call _main from _call__main

    return

label _main:
    while True:
        call lbl_main from _call_lbl_main
    return

label lbl_main:
    scene expression 'images/bg/vatican.png'
    menu:
        'Decade: [core.decade]; Sparks: [player.sparks]'
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
        'Рынок':
            call lbl_slave_market()

    return


label lbl_slave_market():
    $ slavestore.open()
    return

label lbl_lupanarium():
    python:
        choices = [('Return', 'return')]
        mudfight = available_arenas['mudfight']
        whip_fight = available_arenas['whip_fight']
        if mudfight.is_active(player):
            choices.append(('Mudfight', mudfight))
        else:
            choices.append(('Mudfight', None))

        if whip_fight.is_active(player):
            choices.append(('Whip fight', whip_fight))
        else:
            choices.append(('Whip fight', None))
        choice = renpy.display_menu(choices)
    if choice == 'return':
        return
    call lbl_arena(choice)
    return

label lbl_taberna():
    python:
        choices = [('Return', 'return')]
        pitfight = available_arenas['pitfight']
        if pitfight.is_active(player):
            choices.append(('Pitfight', pitfight))
        else:
            choices.append(('Pitfight', None))

        choice = renpy.display_menu(choices)
    if choice == 'return':
        return
    call lbl_arena(choice)
    return

label lbl_colosseum():
    python:
        choices = [('Return', 'return')]
        chaotic = available_arenas['chaotic_fights']
        common_fight = available_arenas['common_fight']
        premium_fight = available_arenas['premium_fights']
        tournament = available_arenas['tournament']
        if chaotic.is_active(player):
            choices.append(('Chaotic fights', chaotic))
        else:
            choices.append(('Chaotic fights', None))
        if common_fight.is_active(player):
            choices.append(('Common fight', common_fight))
        else:
            choices.append(('Common fight', None))
        if premium_fight.is_active(player):
            choices.append(('Premium fight', premium_fight))
        else:
            choices.append(('Premium fight', None))

        if tournament.is_active(player) and len(tournament.filter_fighters(player)) >= 3:
            choices.append(('Tournament', tournament))
        else:
            choices.append(('Tournament', None))
        choice = renpy.display_menu(choices)
    if choice == 'return':
        return
    call lbl_arena(choice)
    return

label lbl_grand_fight(arena_maker):
    python:
        team = []
        enemies = [make_gladiator_fit_raiting(30, 100)() for i in xrange(2)]
        enemies.extend([make_gladiator_fit_raiting(100, 150) for i in xrange(2)])
        enemies.append(make_champion())
        arena_maker.current_enemy = enemies.pop(0)
    'Select you team (3 fighters)'
    python:
        while len(team) < 3:
            selector = FighterSelector(player, arena_maker, team)
            selector.run()
            team.append(selector.current_fighter())
    'Tournament is going to begin'
    python:
        while len(team > 0) or len(enemies) > 0:
            selector = FighterSelector(player, arena_maker, team=team)
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
    return

label lbl_arena(arena_maker):
    $ res = None

    python:
        selector = FighterSelector(player, arena_maker)
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
                fame_changed = True
                fame_message = 'Player gain fame'
                fame = arena.raise_fame(PriceCalculator, player)
                arena_maker.is_winned = fame
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