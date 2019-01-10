init python:
    sys.path.append(renpy.loader.transfn("extensions/Worlds/ZombieWorld"))

init 1 python:
    from zombieworld import *

    class ZombieWorld(World):
        DAYS_TO_SURVIVE = 30
        _VISITS = 0

        def __init__(self, *args, **kwargs):
            super(ZombieWorld, self).__init__(*args, **kwargs)
            self.current_location = None
            self.turn = 1
            self.locations = dict()

        def set_location(self, location):
            self.current_location = location

        def add_available_location(self, id, location):
            self.locations[id] = location

        def get_available_location(self, id):
            return self.locations.get(id)

        @Observable
        def skip_turn(self):
            self.turn += 1
            renpy.call_in_new_context('lbl_zombieword_sleep', world=self)
            self.player.vitality += 10

        def entry_label(self):
            if ZombieWorld._VISITS > 1:
                return 'lbl_zombieworld'
            else:
                return 'lbl_zombieworld_tutorial'

        def get_path(self):
            return 'ZombieWorld/'

        def on_visit(self, person):
            ZombieWorld._VISITS += 1
            if getattr(ZombieWorld, 'PLAYER', None) is None:
                self.player = ZombieWorldPersonMaker.make_person(person)
                ZombieWorld.PLAYER = self.player
                self.player.add_eventlistener('vitality_changed', self.vitality_change_callback)
            else:
                self.player = ZombieWorld.PLAYER

        def vitality_change_callback(self, vitality):
            if vitality <= 0:
                renpy.call_in_new_context('lbl_zombieworld_loose', world=self, person=person)

    class ZombieWorldUtilities(object):

        def __init__(self, world):
            self._world = world

        def normal_heart_image(self):
            return self._world.path('resources/icons/heart_normal.png')

        def cursed_heart_image(self):
            return self._world.path('resources/icons/heart_cursed.png')

        def food_icon(self):
            return self._world.path('resources/icons/item_food.png')

        def drugs_icon(self):
            return self._world.path('resources/icons/item_drugs.png')


label lbl_zombieworld(world):
    'Zombieworld'
    return


label lbl_zombieworld_loose(world, person):
    'You lost all your vitality. GG'
    $ renpy.quit()
    return

label lbl_zombieword_sleep(world):
    menu:
        "Eat" if world.player.food > 0:
            python:
                ZombieWorldChangeVitality(world.player, 1).run()
                world.player.food -= 1
            if world.player.vitality < world.player.max_vitality:
                menu:
                    'Use drugs' if world.player.drugs > 0:
                        python:
                            ZombieWorldChangeVitality(world.player, 1).run()
                            world.player.drugs -= 1
                    'Go to sleep':
                        $ pass
        "Hungry sleep":
            $ ZombieWorldChangeVitality(world.player, -1).run()
        "I must go":
            return
    'You sleep'
    python:
        if world.player.gender != 'female':
            ZombieWorldChangeFilth(world.player, 1).run()
    return