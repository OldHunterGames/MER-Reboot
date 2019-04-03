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

    for suit in CoreDuelSuit.get_suits():
        data = {'suit': suit}
        CoreDuelCard.register_card(suit.id, CoreDuelCard(suit.id, data))

    def make_gladiator():
        gladiator = PersonCreator.gen_person(gender='male', genus='human')
        gladiator.person_class = PersonClass.random_by_tag('gladiator')  
        gladiator.armor = Armor.random_by_type(gladiator.person_class.available_garments[0])
        gladiator.soul_level = random.randint(0, 5)

        return gladiator
# The game starts here.

label start:
    $ player = PersonCreator.gen_person(name='Player', gender='male', genus='human')
    $ player.slaves = []
    $ core = MERCore()
    $ core.player = player
    $ core.skip_turn.add_callback(CoreAddCards(player).run)
    $ core.skip_turn.add_callback(CoreDuel.drop_skulls_callback)
    $ core.skip_turn.add_callback(CoreSexMinigame.decade_skip_callback)
    python:
        AngelMaker.add_observer('archon_generated', lambda archon: World.get_random_world()(archon))
        # for i in range(10000):
        #     gladiator1 = PersonCreator.gen_person(gender='male', genus='human')
        #     gladiator1.person_class = PersonClass.random_by_tag('gladiator')
            
        #     gladiator2 = PersonCreator.gen_person(gender='male', genus='human')
        #     gladiator2.person_class = PersonClass.random_by_tag('gladiator')
            
        #     gladiator1.armor = Armor.random_by_type(gladiator1.person_class.available_garments[0])
        #     gladiator2.armor = Armor.random_by_type(gladiator2.person_class.available_garments[0])
            
        #     gladiator1.soul_level = random.randint(0, 5)
        #     gladiator2.soul_level = random.randint(0, 5)

        #     act1 = random.choice(gladiator1.person_class.get_attacks())
        #     act2 = random.choice(gladiator2.person_class.get_attacks())
        #     Standoff(gladiator1, act1, gladiator2, act2).run()
        class SlaveMarket(object):
            def __init__(self, player):
                self.slaves = [make_gladiator() for i in xrange(3)]
                self.state = 'buy'
                self.player = player

            def switch_mode(self):
                self.state = 'sell' if self.state == 'buy' else 'buy'

            def buy(self, slave):
                self.player.slaves.append(slave)
                self.slaves.remove(slave)
                if len(self.slaves) < 1:
                    self.state = 'sell'

            def sell(self, slave):
                self.player.slaves.remove(slave)
                self.slaves.append(slave)
                if len(self.player.slaves) < 1:
                    self.state = 'buy'

            def update_slaves(self):
                self.slaves = [make_gladiator() for i in xrange(3)]

            def open(self):
                if len(self.slaves) > 0:
                    self.state = 'buy'
                return renpy.call_screen('sc_slave_market', self)

        class FighterSelector(object):
            def __init__(self, player, enemy):
                self.player = player
                self.enemy = enemy
                self.index = 0

            def run(self):
                return renpy.call_screen('sc_select_fighter', self)

            @property
            def fighters(self):
                return self.player.slaves

            def current_fighter(self):
                return self.fighters[self.index]

            def next(self):
                self.index += 1

            def prev(self):
                self.index -= 1

            def next_active(self):
                return self.index < len(self.fighters) - 1

            def prev_active(self):
                return self.index > 0

        slavestore = SlaveMarket(player)

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
        'Decade: [core.decade]'
        'Me':
            $ CharacterInfoScreen(player).show()
        'Others':
            $ ContactsInfo(core.characters).show()
        'Travel to outer worlds':
            python:
                angel = AngelMaker.gen_archon()
                MistTravel(angel.world, player, core).run()
        'Arena':
            call lbl_arena()

        'Рынок':
            call lbl_slave_market()

    return


label lbl_slave_market():
    $ slavestore.open()
    return

label lbl_arena():
    $ res = None
    $ disabled = None if len(player.slaves) < 1 else 'put'
    $ choice = renpy.display_menu([('make bet', 'bet'), ('put fighter', disabled), ('Return', 'leave')])
    if choice == 'bet':
        while res != 'leave_arena':
            python:
                gladiator1 = make_gladiator()            
                gladiator2 = make_gladiator()

                arena = MerArena(gladiator1, gladiator2)
                res = arena.start()
                if res != 'leave_arena' and res != 'next':
                    fight = arena.fight
                    result = 'won' if fight.is_player_win() else 'lost'

            if res != 'leave_arena' and res != 'next':
                show screen sc_arena_results(fight)
                'Fight'
                python:
                    for i in xrange(len(fight.results)):
                        fight.update_counter()
                        renpy.say(None, fight.messages[i])
                'Winner is [fight.winner.name] / player [result] his bet'
                hide screen sc_arena_results
            

    if choice == 'put':
        python:
            gladiator1 = make_gladiator()
            selector = FighterSelector(player, gladiator1)
            selector.run()
            gladiator2 = selector.current_fighter()
            arena = MerArena(gladiator1, gladiator2)
            arena.make_bet(gladiator2)
            arena.start()
            fight = arena.fight
            result = 'won' if fight.is_player_win() else 'lost'
            if result != 'won':
                player.slaves.remove(gladiator2)
            slavestore.update_slaves()

        show screen sc_arena_results(fight)
        'Fight'
        python:
            for i in xrange(len(fight.results)):
                fight.update_counter()
                renpy.say(None, fight.messages[i])
        if result != 'won':
            'Winner is [fight.winner.name] / player [result] his bet / [fight.loser.name] is killed'
        else:
            'Winner is [fight.winner.name] / player [result] his bet'
        hide screen sc_arena_results

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