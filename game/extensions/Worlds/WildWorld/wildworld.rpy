init python:
    sys.path.append(renpy.loader.transfn("extensions/Worlds/WildWorld"))
init 1 python:
    from wildworld import *
    for key, value in wildworld_features.items():
        Feature.register_feature(key, Feature(value))

    class WildWorld(World):
        
        def __init__(self, *args, **kwargs):
            super(WildWorld, self).__init__(*args, **kwargs)
            self.characters = list()

        def entry_label(self):
            return 'lbl_wildworld'
    
        def get_path(self):
            return 'WildWorld/resources/'
        
        def on_visit(self, person):
            self.player = WildWorldPersonMaker.make_person(person)
        
        def add_character(self, person):
            self.characters.append(person)

label lbl_wildworld(world):
    show screen sc_wildworld_stats(world)
    python:
        captive = WildWorldPersonMaker.make_person(person_maker=PersonCreator)
    captive 'Hello'
    return
