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


label lbl_zombieworld(world):
    'Zombieworld'
    return


label lbl_zombieworld_loose(world, person):
    'You lost all your vitality. GG'
    $ renpy.quit()
    return