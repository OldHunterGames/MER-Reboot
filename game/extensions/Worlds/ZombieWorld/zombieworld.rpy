init python:
    sys.path.append(renpy.loader.transfn("extensions/Worlds/ZombieWorld"))

init 1 python:
    from zombieworld import *

    class ZombieWorld(World):
        DAYS_TO_SURVIVE = 30

        def __init__(self, *args, **kwargs):
            super(ZombieWorld, self).__init__(*args, **kwargs)
            self.current_location = None

        def set_location(self, location):
            self.current_location = location




