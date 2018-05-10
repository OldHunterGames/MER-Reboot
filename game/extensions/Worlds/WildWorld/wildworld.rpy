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
            self.locations = Locations()
            self.food = 0
            self.day = 1

        def entry_label(self):
            return 'lbl_wildworld'
    
        def get_path(self):
            return 'WildWorld/resources/'
        
        def on_visit(self, person):
            self.player = WildWorldPersonMaker.make_person(person)
        
        def add_character(self, person):
            self.characters.append(person)
        
        def change_location(self, pos):
            self.skip_turn()
            self.locations.current = pos
        
        def skip_turn(self):
            self.food -= len(self.characters)
            self.food -= 1
            if self.food < 0:
                self.food = 0
            self.day += 1
        
        def get_slaves(self, gender='all'):
            if gender == 'all':
                return [i for i in self.characters]
            return [i for i in self.characters if i.gender == gender]
        
        def remove_character(self, person):
            self.characters.remove(person)
    

    class SlaverMarket(object):
        
        def __init__(self, slaves, world, multiplier=1):
            self.slaves = slaves
            self.world = world
            self.multiplier = multiplier
            self.selected = None
        
        def select(self, slave):
            self.selected = slave
        
        def price(self):
            price = max(self.selected.attributes().values()) * self.multiplier
            if price <= 0:
                price = 1
            return price
        
        def sell(self):
            self.slaves.remove(self.selected)
            world.remove_character(self.selected)
            price = self.price()
            self.world.food += price
            self.selected = None
        
        def show(self):
            return renpy.show_screen('sc_wildworld_sell_slaves', market=self)


label lbl_wildworld(world):
    call lbl_wildworld_main(world)
    return

label lbl_wildworld_main(world):
    show screen sc_wildworld_stats(world)
    while True:
        $ world.locations.current_location().visit(world)
    return

label lbl_wildworld_road(world):
    while True:
        'Road'
    return

label lbl_wildworld_brothel_city(world):
    while True:
        menu:
            "In brothe city you can sell female slaves for 3x of it's maximum attribute"
            'Sell slaves':
                if len(world.get_slaves('female')) > 0:
                    $ SlaverMarket(world.get_slaves('female'), world, 3).show()
                else:
                    $ pass
    return

label lbl_wildworld_market_city(world):
    while True:
        menu:
            "In market city you can sell any slave for 2x of it's maximum attribute"
            'Sell slaves':
                if len(world.get_slaves()) > 0:
                    $ SlaverMarket(world.get_slaves(), world, 2).show()
                else:
                    $ pass
    return

label lbl_wildworld_wildness(world):
    while True:
        menu:
            'Catch slave':
                python:
                    world.add_character(WildWorldPersonMaker.make_person(person_maker=PersonCreator))
                    world.skip_turn()
    return