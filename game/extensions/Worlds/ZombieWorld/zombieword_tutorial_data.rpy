init python:
    zombieworld_tutorial_events = {
        'rape': {
            'name': __('Rape'),
            'description': __("Suddenly you hear the girl cry and some fussy noises nearby."),
            'label': 'lbl_zombieworld_tutorial_zombie_rape_event'
        },
        'girl': {
            'name': __('Girl'),
            'description': __("The rescued girl is still lying on the ground and is breathing heavily."),
            'label': 'lbl_zombieworld_tutorial_girl_event'
        },
        'tent': {
            'name': __('Tent'),
            'description': __("Masha told you where to find her tent. There must be some spare clothes and a bit of food there, but also a more ghouls."),
            'label': 'lbl_zombieworld_tutorial_tent_event'
        },
        'first_quest': {
            'name': __('First quest'),
            'description': __("Masha is waiting nearby, for food and cloth."),
            'label': 'lbl_zombieworld_tutorial_cloth_event'
        },
        'first_sleep': {
            'name': __('Sleep'),
            'description': __("Masha got to the tent to get some sleep. It's late and you are tired to. You need to get some meal and a good night sleep too."),
            'pseudo': True,
            'label': 'lbl_zombieworld_tutorial_sleep_event'
        },
        'highway': {
            'name': 'Highway',
            'description': "Masha is gone, and I need to get out of this wilderness too.",
            'label': 'lbl_zombieworld_tutorial_highway_event'
        },
        'go_east': {
            'name': __('Go east'),
            'description': "The path to the east is clear.",
            'label': 'lbl_zombieworld_tutorial_go_east_event'
        },
        'tutorial_hunters_encampment_male': {
            'name': __("Encampment"),
            'description': "You are called by an armed man standing on the watchtower.",
            'label': 'lbl_zombieworld_tutorial_encampment_male_event'
        },
        'tutorial_hunters_encampment_female': {
            'name': __("Encampment"),
            'description': "You are called by an armed man standing on the watchtower.",
            'label': 'lbl_zombieworld_tutorial_encampment_female_event'
        },
        'tutorial_zombie_mob': {
            'name': __("Mob"),
            "description": "The past to the west is blocked by a large ghoul mob, wandering around a bunch of wrecked and burned cars.",
            'label': 'lbl_zombieworld_tutorial_mob_event'
        }
    }

    zombieworld_tutorial_locations = {
        'forest': {   
            'name': __("Forest"),
            'description': __("It's just a plain forest. Looks normal... but there is something eerie in the air.")
        },
        'highway': {
            'name': __("Highway"),
            'description': __("In the middle of the woods you found a straight highway leading from east to west.")
        },
        'hunters_encampment': {
            'name': __("Hunters encampment"),
            'description': __("There is a fortified encampment on the roadside. It's surrounded by a barricade built of old cars, rusty metal sheets, croaker and old tires. The only passage is closed by a barrage of stakes sticking out in different directions, on which sluggishly moving ghouls are planted.")
        }
    }

label lbl_zombieworld_tutorial_zombie_rape_event(event, person, world):
    show expression event.image() as bg
    "You see a girl in teared clothes, forcefully pinned down by a strangely looking man. He is more like a half-rotten corpse than a living man, but moves vigorously. Strangely, this zombie-like monster don't trying to eat the girls brains, but fucks her violently instead."
    "A large knife lies on the ground nearby. The girl desperately reaches out to him but she misses a few inches. Stunned by this scene you trying to figure out what you should do. Meanwhile the monster and growls in pleasure... He is cumming!"
    menu:
        "You finally decide to act and grab a knife. At the same moment, the zombie loses interest in the woman lying on the ground and his interested look rushes toward you. It's not very clear whether he wants to kill or rape you, but in any case it's time to fight."
        'Fight! (Vitality -20\%)':
            "The knife gets handy. A few intense strokes and zombies falls on the ground, leaving you a few scratches and aching muscles."
            "You loot knife"
            python:
                person.vitality -= 20
                person.add_item(ZombieWorldItem('knife'))
                girl_event = ZombieWorldEvent('girl', zombieworld_tutorial_events['girl'])
                world.current_location.add_event(girl_event)
                world.current_location.remove_event_by_id('rape')
    return

label lbl_zombieworld_tutorial_girl_event(event, person, world):
    "You approach a girl raped by zombie. Her clothes is ruined so you can see her niked body and scratched, brised, dirty skin. The woman does not even look at you, instead she tries to scrape something out of her vagina. You see that it's not an ordinary cum on her fingers, but a hideous black slime."
    "Girl - Fuck-fuck-fuck... this ghoul infested me. Not again. I'm so fucked, oh..."
    "Player - Hey! What the hell is going on here? Who are you? And what this thing is?"
    menu:
        "Girl tells you that her name is Masha. The thing attacked her is a ghoul (...)"
        "I'll bring you some clothes and food":
            python:
                girl_event_2 = ZombieWorldEvent('tent', zombieworld_tutorial_events['tent'])
                world.current_location.add_event(girl_event_2)
                world.current_location.remove_event(girl_event)
    return

label lbl_zombieworld_tutorial_tent_event(event, person, world):
    menu:
        "Two ghouls are stumbling meaninglessly near the Masha's tent. There is no way to get inside without a fight."
        "Fight ghouls (Knife, vitality -40\%)":
            python:
                person.add_item(ZombieWorldItem('cloth'))
                [person.add_item(ZombieWorldItem('food')) for i in xrange(2)]
                person.remove_item(person.find_item("knife"))
                person.vitality -= 40
                tutorial_first_quest = ZombieWorldEvent('first_quest', zombieworld_tutorial_events['first_quest'])
                world.current_location.add_event(tutorial_first_quest)
                world.current_location.remove_event(girl_event_2)
        "Retreat":
            return
    return

label lbl_zombieworld_tutorial_cloth_event(event, person, world):
    menu:
        "Masha is waiting nearby, for food and cloth."
        "Give her food and cloth (cloth x1, food x1)":
            python:
                person.remove_item(person.find_item('cloth'))
                person.remove_item(person.find_item('food'))
                tutorial_first_sleep = ZombieWorldEvent('first_sleep', zombieworld_tutorial_events['first_sleep'])
                tutorial_first_sleep.sleep_callback = lambda *args, **kwargs: ZombieWorldActivateEvent(person, tutorial_first_sleep, world).run()
                world.skip_turn.add_callback(tutorial_first_sleep.sleep_callback)
                world.current_location.add_event(tutorial_first_sleep)
                world.current_location.remove_event(tutorial_first_quest)
        "I need more time":
            return
    return

label lbl_zombieworld_tutorial_sleep_event(event, person, world):
    'Sleeping'
    python:
        highway_event = ZombieWorldEvent('highway', zombieworld_tutorial_events['highway'])
        world.skip_turn.remove_callback(tutorial_first_sleep.sleep_callback)
        world.current_location.add_event(highway_event)
        world.current_location.remove_event(tutorial_first_sleep)
    return

label lbl_zombieworld_tutorial_highway_event(event, person, world):
    menu:
        "I must get out of here."
        "Let's go (vitality -20\%)":
            python:
                person.vitality -= 20
                location = world.get_available_location('highway')
                if location is None:
                    location = ZombieWorldLocation('highway', zombieworld_tutorial_locations['highway'])
                    world.add_available_location('highway', location)
                    location.add_event(ZombieWorldEvent(
                        'go_east',
                        zombieworld_tutorial_events['go_east']
                    ))
                    location.add_event(ZombieWorldEvent('tutorial_zombie_mob', zombieworld_tutorial_events['tutorial_zombie_mob']))
                world.set_location(location)
    return


label lbl_zombieworld_tutorial_go_east_event(event, person, world):
    menu:
        "The path to the east is clear."
        "Go east (vitality -20\%)":
            python:
                person.vitality -= 20
                location = world.get_available_location('hunters_encampment')
                if location is None:
                    location = ZombieWorldLocation('hunters_encampment', zombieworld_tutorial_locations['hunters_encampment'])
                    world.add_available_location('hunters_encampment', location)
                    if person.gender == 'male':
                        location.add_event(ZombieWorldEvent(
                            'tutorial_hunters_encampment_male',
                            zombieworld_tutorial_events['tutorial_hunters_encampment_male']
                        ))
                    else:
                        location.add_event(ZombieWorldEvent(
                            'tutorial_hunters_encampment_female',
                            zombieworld_tutorial_events['tutorial_hunters_encampment_female']
                        ))

                world.set_location(location)
    return


label lbl_zombieworld_tutorial_encampment_male_event(event, person, world):
    menu:
        "Man - Hey! You are not a ghoul. Get in if you want to trade, pal."
        "Get in":
            "To be implemented"
            return
        "Reconsider":
            return
    return

label lbl_zombieworld_tutorial_encampment_female_event(event, person, world):
    menu:
        "Man - Hey! Are you a leech? [person.name] - What?! No. I'm normal. Please let me in. Man - You will not be safe here if no one will guard you. The camp is full of mans desperate to spunk of some filth in a cunt like you. But I can guarantee your safety if you let ME fuck you, babe. I need to drop some black goo off."
        "Uh. Ok. (vitality -20\%, female_filth +20\%)":
            "To be implemented"
            return
        "Reconsider":
            return
    return


label lbl_zombieworld_tutorial_mob_event(event, person, world):
    menu:
        "You will need a considerable force to clear the path. It's risky..."
        "Fight the ghoul mob (follower x3, gun(x3 rounds), machete, motorcycle helmet, thick leather jacket, vitality -20\%)":
            python:
                person.vitality -= 20
            return
        "Reconsider":
            return
    return