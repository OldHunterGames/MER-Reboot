init python:
    sys.path.append(renpy.loader.transfn("extensions/Worlds/WildWorld"))
init 1 python:
    from wildworld import *
    for key, value in wildworld_features.items():
        Feature.register_feature(key, Feature(value))

    class WildWorld(World):

        def entry_label(self):
            return 'lbl_wildworld'
    
        def get_path(self):
            return 'WildWorld/resources/'
        
        def on_visit(self, person):
            self.player = WildWorldPersonMaker.make_person(person)

label lbl_wildworld(world):
    show screen sc_wildworld_stats(world)
    'WildWorld'
    return
