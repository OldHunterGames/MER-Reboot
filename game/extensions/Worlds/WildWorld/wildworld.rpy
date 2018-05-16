init python:
    sys.path.append(renpy.loader.transfn("extensions/Worlds/WildWorld"))

init 1 python:
    from wildworld import *
    for key, value in wildworld_features.items():
        Feature.register_feature(key, Feature(value))
    
    for key, value in wildworld_items.items():
        Item.register_item(key, Item(key, value))

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
            self.slave_escape()
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
        
        def security_chance(self):
            value = 2
            return value > random.randint(0, 6)
        
        def escape_chance(self, person):
            attr = max(person.attributes().values())
            if person.applied_item is not None:
                attr = person.applied_item.escape_chance(attr)
            roll = random.randint(0, 5)
            if attr > roll:
                return True
            return False
        
        def slave_escape(self):
            for i in self.characters:
                result = self.escape_chance(i)
                security = self.security_chance()
                if result:
                    if security:
                        pass
                        # return renpy.call('lbl_wildworld_slave_escape_prevented', self, i)
                    else:
                        self.remove_character(i)
                        renpy.call_in_new_context('lbl_wildworld_slave_escaped', self, i)


    class SlaverMarket(object):
        
        def __init__(self, slaves, world, multiplier=1, attributes='all'):
            self.slaves = slaves
            self.world = world
            self.multiplier = multiplier
            self.selected = None
            self.attributes = attributes
        
        def select(self, slave):
            self.selected = slave
        
        def price(self):
            if self.attributes == 'all':
                price = max(self.selected.attributes().values()) * self.multiplier
            else:
                price = max([self.selected.attribute(i) for i in self.attributes])
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
        
    class SlaveManager(object):
        
        def __init__(self, slaves, world):
            self.slaves = slaves
            self.world = world
            self.selected = None
        
        def select(self, slave):
            self.selected = slave
        
        def make_food(self):
            self.world.remove_character(self.selected)
            self.slaves.remove(self.selected)
            self.world.food += 2
            self.selected = None
        
        def show(self):
            return renpy.show_screen('sc_wildworld_slaves', manager=self)


label lbl_wildworld(world):
    "Wellcome to [world.archon.name]'s world"
    $ item = Item.get_item('sturdy_rope')
    $ world.player.add_item(item)
    "You found 1 [item.name]"
    call lbl_wildworld_main(world)
    return

label lbl_wildworld_main(world):
    show screen sc_wildworld_stats(world)
    while True:
        $ world.locations.current_location().visit(world)
    return

label lbl_wildworld_road(world):
    'Road'
    call screen sc_wildworld_map(world)
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
            'Leave':
                call screen sc_wildworld_map(world)
                return
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
            'Leave':
                call screen sc_wildworld_map(world)
                return
    return

label lbl_wildworld_amazon_village(world):
    while True:
        menu:
            "In amazon village you can sell any male slave for 3x of it's maximum attribute"
            'Sell slaves':
                if len(world.get_slaves('male')) > 0:
                    $ SlaverMarket(world.get_slaves('male'), world, 3).show()
                else:
                    $ pass
            'Leave':
                call screen sc_wildworld_map(world)
                return
    return

label lbl_wildworld_sawmill_city(world):
    while True:
        menu:
            "In sawmill city you can sell any slave for 5x of it's might"
            'Sell slaves':
                if len(world.get_slaves()) > 0:
                    $ SlaverMarket(world.get_slaves(), world, 5, ['might']).show()
                else:
                    $ pass
            'Leave':
                call screen sc_wildworld_map(world)
                return
    return

label lbl_wildworld_artisan_city(world):
    while True:
        menu:
            "In artisan city you can sell any slave for 5x of it's competence"
            'Sell slaves':
                if len(world.get_slaves()) > 0:
                    $ SlaverMarket(world.get_slaves(), world, 5, ['competence']).show()
                else:
                    $ pass
            'Leave':
                call screen sc_wildworld_map(world)
                return
    return

label lbl_wildworld_rich_city(world):
    while True:
        menu:
            "In rich city you can sell any slave for 4x of it's charisma or subtlety"
            'Sell slaves':
                if len(world.get_slaves()) > 0:
                    $ SlaverMarket(world.get_slaves(), world, 5, ['charisma', 'subtlety']).show()
                else:
                    $ pass
            'Leave':
                call screen sc_wildworld_map(world)
                return
    return

label lbl_wildworld_wildness(world):
    while True:
        menu:
            'Catch slave':
                python:
                    items = sorted([(i.name, i) for i in world.player.items('enslave')])
                    if len(items) > 0:
                        item = renpy.display_menu(items)
                        slave = WildWorldPersonMaker.make_person(person_maker=PersonCreator)
                        world.add_character(slave)
                        slave.applied_item = item
                        world.player.remove_item(item)
                        world.skip_turn()
                if len(items) < 1:
                    'You have no items to catch slave'
            'Leave':
                call screen sc_wildworld_map(world)
                return
    return

label lbl_wildworld_slave_escaped(world, person):
    '[person.name] escaped'
    return

label lbl_wildworld_slave_escape_prevented(world, person):
    '[world.player.name] prevented escape of [person.name]'
    return