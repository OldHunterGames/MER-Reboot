## Slaver's caravan slavercaravan_alignment_features


lbl_slavercaravan_event_noevent(world):
    $ pass

    return

lbl_slavercaravan_event_fruittree(world):
    show expression world.path('bg/event_fruittree.png') as bg
    menu:
        'You find a tree full of ripe fruits standing right behind the roadside'
        "Gather fruits":
            'You got 3 days worth of food'
            $ world.food += 3
        'Make yourself a small feast':
            'The ripe fruits are good addition to meat and dry iron-rations. Your stste is better now.'
            $ world.player.state += 1
        'Let it be':
            "You just pass by the tree."
            $ pass
    return

lbl_slavercaravan_event_bandits(world):
    show expression world.path('bg/event_bandits.png') as bg
    menu:
        "A nasty looking gang of bandits closes your pass"
        'Run':
            "You run away from thugs, and your slaves run away from you!"
            $ world.slaves_escape()
        '{color=#0000ffff}(State > 0){/color} Fend them off' if world.player.state > 0:
            'Your fight fierecly and babdits run away, leaving you with a fresh wound {color=#f00}(state drops){/color}'
            $ world.player.state -= 1

    return
