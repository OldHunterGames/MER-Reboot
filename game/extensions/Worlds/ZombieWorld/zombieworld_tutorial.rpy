label lbl_zombieworld_tutorial_main(world):
    $ zombieword_player = core.player
    python:
        location_forest = ZombieWorldLocation(
            'test1',
            {
                'description': "It's just a plain forest. Looks normal... but there is something eerie in the air.",
            }
        )
        location_forest_event = ZombieWorldEvent('test',{
            'name': 'Rape',
            'description': "Suddenly you hear the girl cry and some fussy noises nearby.",
            'label': 'lbl_zombieworld_tutorial_zombie_rape_event'

        })
        location_forest.add_event(location_forest_event)
    call screen sc_zombieworld_location(location_forest)
    return

label lbl_zombieworld_tutorial_zombie_rape_event(event, person):
    "You see a girl in teared clothes, forcefully pinned down by a strangely looking man. He is more like a half-rotten corpse than a living man, but moves vigorously. Strangely, this zombie-like monster don't trying to eat the girls brains, but fucks her violently instead."
    "A large knife lies on the ground nearby. The girl desperately reaches out to him but she misses a few inches. Stunned by this scene you trying to figure out what you should do. Meanwhile the monster and growls in pleasure... He is cumming!"
    menu:
        "You finally decide to act and grab a knife. At the same moment, the zombie loses interest in the woman lying on the ground and his interested look rushes toward you. It's not very clear whether he wants to kill or rape you, but in any case it's time to fight."
        'Fight!':
            #remove vitality
            "The knife gets handy. A few intense strokes and zombies falls on the ground, leaving you a few scratches and aching muscles."
            "You loot knife"
            python:
                girl_event = ZombieWorldEvent('test2', {
                    'name': 'Girl',
                    'description': "The rescued girl is still lying on the ground and is breathing heavily.",
                    'label': 'lbl_zombieworld_tutorial_girl_event'
                })
                location_forest.add_event(girl_event)
                location_forest.remove_event(event)
    return

label lbl_zombieworld_tutorial_girl_event(event, person):
    "You approach a girl raped by zombie. Her clothes is ruined so you can see her niked body and scratched, brised, dirty skin. The woman does not even look at you, instead she tries to scrape something out of her vagina. You see that it's not an ordinary cum on her fingers, but a hideous black slime."
    "Girl - Fuck-fuck-fuck... this ghoul infested me. Not again. I'm so fucked, oh..."
    "Player - Hey! What the hell is going on here? Who are you? And what this thing is?"
    menu:
        "Girl tells you that her name is Masha. The thing attacked her is a ghoul (...)"
        "I'll bring you some clothes and food":
            python:
                girl_event_2 = ZombieWorldEvent('test2', {
                    'name': 'Tent',
                    'description': "Masha told you where to find her tent. There must be some spare clothes and a bit of food there, but also a more ghouls.",
                    'label': 'lbl_zombieworld_tutorial_tent_event'
                })
                location_forest.add_event(girl_event_2)
                location_forest.remove_event(girl_event)
    return

label lbl_zombieworld_tutorial_tent_event(event, person):
    menu:
        "Two ghouls are stumbling meaninglessly near the Masha's tent. There is no way to get inside without a fight."
        "Fight ghouls":
            # remove vitality, knife
            # give loot
            python:
                tutorial_first_quest = ZombieWorldEvent('test2', {
                    'name': 'Tent',
                    'description': "Masha is waiting nearby, for food and cloth.",
                    'label': 'lbl_zombieworld_tutorial_cloth_event'
                })
                location_forest.add_event(tutorial_first_quest)
                location_forest.remove_event(girl_event_2)
        "Retreat":
            return
    return

label lbl_zombieworld_tutorial_cloth_event(event, person):
    menu:
        "Masha is waiting nearby, for food and cloth."
        "Give her food and cloth (cloth x1, food x1)":
            python:
                tutorial_first_sleep = ZombieWorldEvent('test2', {
                    'name': 'Sleep',
                    'description': "Masha got to the tent to get some sleep. It's late and you are tired to. You need to get some meal and a good night sleep too.",
                    'pseudo': True,
                    'label': 'lbl_zombieworld_tutorial_sleep_event'
                })
                location_forest.add_event(tutorial_first_sleep)
                location_forest.remove_event(tutorial_first_quest)
        "I need more time":
            return
    return

label lbl_zombieworld_tutorial_sleep_event(event, person):
    python:
        highway_event = ZombieWorldEvent('test2', {
                    'name': 'Highway',
                    'description': "Masha is gone, and I need to get out of this wilderness too.",
                    'label': 'lbl_zombieworld_tutorial_highway_event'
                })
        location_forest.add_event(highway_event)
        location_forest.remove_event(tutorial_first_sleep)

label lbl_zombieworld_tutorial_highway_event(event, person):
    'Highway lock transfer'