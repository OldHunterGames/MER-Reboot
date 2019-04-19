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

    def make_gladiator(allowed_classes=None):
        gladiator = PersonCreator.gen_person(genus='human')
        if allowed_classes is not None:
            classes = allowed_classes
        else:
            classes = PersonClass.pipe_filters(PersonClass.class_filter, PersonClass.gender_filter)(
                gladiator, PersonClass.get_by_tag('gladiator'))

        gladiator.person_class = random.choice(classes)
        gladiator.armor = Armor.random_by_type(gladiator.person_class.available_garments[0])

        return gladiator

    def make_starter_salve():
        slave = PersonCreator.gen_person(genus='human')
        slave.person_class = PersonClass.random_by_tag('starter')
        slave.armor = Armor.random_by_type(slave.person_class.available_garments[0])

        return slave
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
        # for i in range(10000):
        #     gladiator1 = PersonCreator.gen_person(gender='male', genus='human')
        #     gladiator1.person_class = PersonClass.random_by_tag('gladiator')
            
        #     gladiator2 = PersonCreator.gen_person(gender='male', genus='human')
        #     gladiator2.person_class = PersonClass.random_by_tag('gladiator')
            
        #     gladiator1.armor = Armor.random_by_type(gladiator1.person_class.available_garments[0])
        #     gladiator2.armor = Armor.random_by_type(gladiator2.person_class.available_garments[0])

        #     act1 = random.choice(gladiator1.person_class.get_attacks())
        #     act2 = random.choice(gladiator2.person_class.get_attacks())
        #     Standoff(gladiator1, act1, gladiator2, act2).run()
        class SlaveMarket(object):
            def __init__(self, player):
                self.slaves = [make_starter_salve() for i in xrange(3)]
                self.state = 'buy'
                self.player = player

            def switch_mode(self):
                self.state = 'sell' if self.state == 'buy' else 'buy'

            def buy(self, slave):
                self.player.slaves.append(slave)
                self.slaves.remove(slave)
                self.player.sparks -= self.calc_price(slave)
                if len(self.slaves) < 1:
                    self.state = 'sell'

            def sell(self, slave):
                self.player.slaves.remove(slave)
                self.player.sparks += self.calc_price(slave)
                if len(self.player.slaves) < 1:
                    self.state = 'buy'

            def can_buy(self, slave):
                return self.player.sparks >= self.calc_price(slave) and HomeManager.MAX_SLAVES > len(self.player.slaves)

            def update_slaves(self, *args, **kwargs):
                self.slaves = [make_starter_salve() for i in xrange(3)]

            def open(self):
                if len(self.slaves) > 0:
                    self.state = 'buy'
                return renpy.call_screen('sc_slave_market', self)

            def calc_price(self, slave):
                attr = min(0, max(slave.attributes().values()))
                return (attr + slave.soul_level) * 5 * slave.person_class.tier

        class FighterSelector(object):
            def __init__(self, player, enemy, arena_maker):
                self.player = player
                self.enemy = enemy
                self.index = 0
                self.arena_maker = arena_maker
                self.escaped = False

            def escape(self):
                self.escaped = True

            def run(self):
                return renpy.call_screen('sc_select_fighter', self)

            @property
            def fighters(self):
                return arena_maker.filter_fighters(self.player)

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


        class HomeManager(object):
            MAX_SLAVES = 1
            def __init__(self, player):
                self.player = player
                self.current_slave = None
                self.core = core
                self.should_skip_turn = False

            def calc_upkeep(self):
                return self.MAX_SLAVES * 5 + len(self.player.slaves) * 5

            def on_skip_turn(self, *args, **kwargs):
                self.player.sparks -= self.calc_upkeep()

            @property
            def slaves(self):
                return [i for i in self.player.slaves]

            def select(self, slave):
                self.current_slave = slave

            def call(self):
                return renpy.call_screen('sc_home', self)

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

            def can_make_love(self, slave):
                return slave.gender != self.player.gender and not slave.exhausted and not self.player.exhausted

            def make_love(self, slave):
                slave.grove = True
                slave.temporary_card = PersonClassCard.get_card('satisfaction')
                self.player.temporary_card = PersonClassCard.get_card('satisfaction')
                if player.get_relation('lover') is not None:
                    self.player.temporary_card = PersonClassCard.get_card('betrayal')
                self.player.add_relation('lover', slave)
                slave.exhausted = True
                self.player.exhausted = True

            def can_attend_party(self, slave):
                return slave.gender == self.player.gender and not slave.exhausted and not self.player.exhausted

            def attend_party(self, slave):
                slave.grove = True
                slave.temporary_card = PersonClassCard.get_card('shared_wisdom')
                self.player.temporary_card = PersonClassCard.get_card('shared_wisdom')
                self.player.add_relation('best_friend', slave)
                slave.exhausted = True
                self.player.exhausted = True
            

        slavestore = SlaveMarket(player)
        pitfight_classes = PersonClass.get_by_tag('lanista')
        pitfight_classes.extend(PersonClass.get_by_ids(['lucator', 'pugilist', 'menial_slave']))
        heat_up_classes = list(set(PersonClass.get_by_tag('gladiator'))
            .difference(set(PersonClass.get_by_tier(4)))
            .difference(set(PersonClass.get_by_tier(5)))
        )
        enemies = list(set(heat_up_classes).intersection(set(PersonClass.get_by_tier(3))))
        grand_fight_classes = PersonClass.get_by_tag('gladiator')

        available_arenas = {
            'mudfight': MerArenaMaker(make_gladiator, allowed_classes=PersonClass.get_by_ids(['sex_slave', 'lucator']), sparks=5),
            'whip_fight': MerArenaMaker(make_gladiator, 3, allowed_classes=PersonClass.get_by_ids(['andabant']), sparks=10),
            'pitfight': MerArenaMaker(
                make_gladiator,
                allowed_classes=pitfight_classes,
                fixed_enemy=[PersonClass.get_by_id('pugilist')],
                sparks=5
            ),
            'practice': MerArenaMaker(
                make_gladiator,
                2,
                allowed_classes=[PersonClass.get_by_id('pegniarius')],
                sparks=5
            ),
            'heat_up': MerArenaMaker(
                make_gladiator,
                3,
                allowed_classes=heat_up_classes,
                fixed_enemy=enemies,
                sparks=15,
            ),
            'grand_fight': MerArenaMaker(
                make_gladiator,
                4,
                allowed_classes=grand_fight_classes,
                fixed_enemy=enemies,
                sparks=50,
            ),
        }
        for arena in available_arenas.values():
            core.skip_turn.add_callback(arena.set_gladiator)

        home_manager = HomeManager(player)
        core.skip_turn.add_callback(slavestore.update_slaves)
        core.skip_turn.add_callback(home_manager.on_skip_turn)

    call lbl_make_initial_characters() from _call_lbl_make_initial_characters
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
        practice = available_arenas['practice']
        heat_up = available_arenas['heat_up']
        grand_fight = available_arenas['grand_fight']
        if practice.is_active(player):
            choices.append(('Practice', practice))
        else:
            choices.append(('Practice', None))
        if heat_up.is_active(player):
            choices.append(('Heat up', heat_up))
        else:
            choices.append(('Heat up', None))
        if grand_fight.is_active(player):
            choices.append(('Grand fight', grand_fight))
        else:
            choices.append(('Grand fight', None))

        choice = renpy.display_menu(choices)
    if choice == 'return':
        return
    call lbl_arena(choice)
    return

label lbl_arena(arena_maker):
    $ res = None
    $ disabled = None if len(arena_maker.filter_fighters(player)) < 1 else 'put'
    $ choice = renpy.display_menu([('make bet', 'bet'), ('put fighter', disabled), ('Return', 'leave')])
    if choice == 'bet':
        while res != 'leave_arena':
            python:
                gladiator1 = arena_maker.make_gladiator()            
                gladiator2 = arena_maker.make_gladiator()

                arena = MerArena(gladiator1, gladiator2, sparks=5)
                res = arena.start()
                if res != 'leave_arena' and res != 'next':
                    fight = arena.fight
                    result = 'won' if fight.is_player_win() else 'lost'
                    if result == 'won':
                        player.sparks += arena.sparks
                    else:
                        player.sparks -= arena.sparks

            if res != 'leave_arena' and res != 'next':
                'Winner is [fight.winner.name] / player [result] his bet'            

    if choice == 'put':
        python:
            gladiator1 = arena_maker.current_enemy
            selector = FighterSelector(player, gladiator1, arena_maker.allowed_classes)
            selector.run()
            gladiator2 = selector.current_fighter()
            if gladiator2 is not None:
                arena = MerArena(gladiator1, gladiator2)
                arena.make_bet(gladiator2)
                arena.start()
                fight = arena.fight
                result = 'won' if fight.is_player_win() else 'lost'
                gladiator2.exhausted = True
                if result != 'won' and fight.loser != player:
                    player.slaves.remove(gladiator2)
                if result == 'won' and not arena_maker.is_winned:
                    gladiator2.after_fight()
                    new_classes = PersonClass.available_upgrades(player)
                    if len(new_classes) > 0:
                        player.person_class = random.choice(new_classes)
                    arena_maker.is_winned = True
                if result == 'won':
                    gladiator2.win_arena = True
                    player.sparks += arena_maker.sparks
        if gladiator2 is None:
            return

        if result != 'won':
            'Winner is [fight.winner.name] / player [result]/ [fight.loser.name] is killed'
        else:
            'Winner is [fight.winner.name] / player [result]'
        python:
            if fight.loser == player:
                renpy.full_restart()
    if choice == 'leave':
        return
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