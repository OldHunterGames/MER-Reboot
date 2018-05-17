init python:
    sys.path.append(renpy.loader.transfn("extensions/Worlds/WildWorld"))
    import math

init 1 python:
    from wildworld import *
    for key, value in wildworld_features.items():
        Feature.register_feature(key, Feature(value))
    
    for key, value in wildworld_physical_features.items():
        Feature.register_feature(key, Feature(value))
    
    for key, value in wildworld_alignment_features.items():
        Feature.register_feature(key, Feature(value))
    
    for key, value in wildworld_items.items():
        Item.register_item(key, Item(key, value))

    class WildWorld(World):
        PLAYER = None
        def __init__(self, *args, **kwargs):
            super(WildWorld, self).__init__(*args, **kwargs)
            self.characters = list()
            self.locations = Locations()
            self.food = 0
            self.day = 1
            self.halt = False

        def entry_label(self):
            return 'lbl_wildworld'
    
        def get_path(self):
            return 'WildWorld/resources/'
        
        def on_visit(self, person):
            if getattr(WildWorld, 'PLAYER', None) is None:
                self.player = WildWorldPersonMaker.make_person(person)
                WildWorld.PLAYER = self.player
            else:
                self.player = WildWorld.PLAYER

        
        def add_character(self, person):
            self.characters.append(person)
        
        def change_location(self, pos):
            self.halt = True
            self.locations.current = pos
        
        def skip_turn(self):
            if self.locations.current_location().type() != 'city':
                self.slave_escape()
            for i in self.characters:
                self.food -= i.applied_item.food_consumption(1)
            self.food -= 1
            if self.food < 0:
                self.food = 0
                self.player.state -= 1
                self.characters = list()
                if self.player.state == 0:
                    renpy.call_in_new_context('lbl_wildworld_gameover')
            self.day += 1
        
        def get_slaves(self, gender='all'):
            if gender == 'all':
                return [i for i in self.characters]
            return [i for i in self.characters if i.gender == gender]
        
        def remove_character(self, person):
            self.characters.remove(person)
        
        def security_chance(self):
            chances = ['catch' for i in range(self.player.state)]
            chances.extend(['catch' for i in range(max(self.player.attributes().values()))])
            return chances
        
        def escape_chance(self, person):
            value = max(person.attributes().values())
            value = int(person.applied_item.escape_chance(value))
            return ['escape' for i in range(value)]
        
        def slave_escape(self):
            for i in self.characters:
                chances = self.escape_chance(i)
                chances.extend(self.security_chance())
                result = random.choice(chances)
                if result == 'escape':
                    self.remove_character(i)
                    renpy.call_in_new_context('lbl_wildworld_slave_escaped', self, i)
                    return
                elif result == 'catch':
                    pass
                    # return renpy.call('lbl_wildworld_slave_escape_prevented', self, i)                        


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
    
    class CatchSlave(object):
        
        def __init__(self, world, location, slave, items, tries):
            self.world = world
            self.location = location
            self.slave = slave
            self.items = items
            self.tries = tries
            self.catched = False
        
        def make_food(self):
            self.location.slaves[self.location.slaves.index(slave)] = None
            self.world.food += 5
            self.catched = True
        
        def catch(self, item):
            self.location.slaves[self.location.slaves.index(slave)] = None
            self.slave.applied_item = item
            self.world.add_character(self.slave)
            self.world.player.remove_item(item)
            self.catched = True
        
        def call(self):
            return renpy.call_screen('sc_wildworld_catch_slave', manager=self)

label lbl_wildworld_gameover():
    'Game is over'
    $ renpy.full_restart()
    return

label lbl_wildworld(world):
    "Wellcome to [world.archon.name]'s world"
    call lbl_wildworld_main(world)
    return

label lbl_wildworld_main(world):
    show screen sc_wildworld_stats(world)
    while True:
        if world.halt:
            call lbl_wildworld_halt(world)
        else:
            $ world.locations.current_location().visit(world)
    return

label lbl_wildworld_road(world):
    'Road'
    call screen sc_wildworld_map(world)
    return

label lbl_wildworld_halt(world):
    'Halt'
    while world.halt:
        menu:
            'Skip turn':
                $ world.halt = False
                $ world.skip_turn()
    return

label lbl_buy_item(world):
    python:
        slavery_items = Item.get_items('enslave')
        items = list()
        for item in slavery_items:
            amount = 1
            if float(item.price).is_integer():
                info = {'item': item, 'amount': amount, 'price': item.price}
                if item.price <= world.food:
                    items.append(("%s, price: %s" %(item.name, item.price), info))
            else:
                while amount < 5:
                    amount += 1
                price = item.price * amount
                if price < 1:
                    price = 1
                else:
                    price = int(math.floor(price))
                info = {'item': item, 'amount': amount, 'price': price}
                if price <= world.food:
                    items.append(( "%sx %s, price: %s" % (amount, item.name, price), info))
        items.append(('Leave', 'leave'))
        item = renpy.display_menu(items)
        if item != 'leave':
            world.food -= item['price']
            for i in range(item['amount']):
                world.player.add_item(item['item'])
    return

label lbl_wildworld_brothel_city(world):
    while True:
        menu:
            "In brothel city you can sell female slaves for 3x of it's maximum attribute"
            'Sell slaves':
                if len(world.get_slaves('female')) > 0:
                    $ SlaverMarket(world.get_slaves('female'), world, 3).show()
                else:
                    $ pass
            'Buy items':
                call lbl_buy_item(world)
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
            'Buy items':
                call lbl_buy_item(world)
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
            'Buy items':
                call lbl_buy_item(world)
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
            'Buy items':
                call lbl_buy_item(world)
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
                    $ SlaverMarket(world.get_slaves(), world, 5, ['competence']).call()
                else:
                    $ pass
            'Buy items':
                call lbl_buy_item(world)
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
            'Buy items':
                call lbl_buy_item(world)
            'Leave':
                call screen sc_wildworld_map(world)
                return
    return

label lbl_wildworld_wildness(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            loc.slaves = [WildWorldPersonMaker.make_person(person_maker=PersonCreator) for i in range(10)]
            loc.tries = 3
    while True:
        menu:
            'Catch slave' if any([i is not None for i in loc.slaves]) and loc.tries > 0:
                python:
                    slaves = [i for i in loc.slaves]
                    while loc.tries > 0 and any([i is not None for i in loc.slaves]):
                        slave = random.choice(slaves)
                        if slave is None:
                            renpy.say(None, 'Just an old trail...')
                            loc.tries -= 1
                            continue
                        items = world.player.items('enslave')
                        catch = CatchSlave(world, loc, slave, items, loc.tries)
                        catch.call()
                        if catch.catched:
                            loc.tries = 0
                            break
                        else:
                            loc.tries -= 1
                    
            'Go for halt':
                $ world.halt = True
                call lbl_wildworld_halt(world)
                $ loc.tries = 3

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