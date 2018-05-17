init python:
    sys.path.append(renpy.loader.transfn("extensions/Worlds/SlaverCaravan"))
    import math

init 1 python:
    from slavercaravan import *
    for key, value in slavercaravan_features.items():
        Feature.register_feature(key, Feature(value))
    
    for key, value in slavercaravan_physical_features.items():
        Feature.register_feature(key, Feature(value))
    
    for key, value in slavercaravan_alignment_features.items():
        Feature.register_feature(key, Feature(value))
    
    for key, value in slavercaravan_items.items():
        Item.register_item(key, Item(key, value))

    class SlaverCaravan(World):
        PLAYER = None
        def __init__(self, *args, **kwargs):
            super(SlaverCaravan, self).__init__(*args, **kwargs)
            self.characters = list()
            self.locations = Locations()
            self.food = 0
            self.day = 1
            self.halt = False

        def entry_label(self):
            return 'lbl_slavercaravan'
    
        def get_path(self):
            return 'SlaverCaravan/'
        
        def on_visit(self, person):
            if getattr(SlaverCaravan, 'PLAYER', None) is None:
                self.player = SlaverCaravanPersonMaker.make_person(person)
                SlaverCaravan.PLAYER = self.player
            else:
                self.player = SlaverCaravan.PLAYER

        
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
                    renpy.call_in_new_context('lbl_slavercaravan_gameover')
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
                    renpy.call_in_new_context('lbl_slavercaravan_slave_escaped', self, i)
                    return
                elif result == 'catch':
                    pass
                    # return renpy.call('lbl_slavercaravan_slave_escape_prevented', self, i)                        


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
            return renpy.show_screen('sc_slavercaravan_sell_slaves', market=self)
        
    class SlaveManager(object):
        
        def __init__(self, slaves, world):
            self.slaves = slaves
            self.world = world
            self.selected = None
        
        def escape_chance(self):
            chances = self.world.escape_chance(self.selected)
            chances.extend(self.world.security_chance())
            return '%s of %s' % (chances.count('escape'), len(chances))
        
        def select(self, slave):
            self.selected = slave
        
        def make_food(self):
            self.world.remove_character(self.selected)
            self.slaves.remove(self.selected)
            self.world.food += 2
            self.selected = None
        
        def show(self):
            return renpy.show_screen('sc_slavercaravan_slaves', manager=self)
    
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
            return renpy.call_screen('sc_slavercaravan_catch_slave', manager=self)

label lbl_slavercaravan_gameover():
    'Game is over'
    $ renpy.full_restart()
    return

label lbl_slavercaravan(world):
    "Wellcome to [world.archon.name]'s world"
    call lbl_slavercaravan_main(world)
    return

label lbl_slavercaravan_main(world):
    show screen sc_slavercaravan_stats(world)
    while True:
        $ world.locations.current_location().visit(world)
    return

label lbl_slavercaravan_road(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            img = random.choice(slavercaravan_locations['road']['images'])
            img = world.path(img)
            loc.image = img
    show expression loc.image as bg
    'Road'
    while True:
        menu:
            'Leave' if not world.halt:
                call screen sc_slavercaravan_map(world)
                return
            'Go for halt':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
    return

label lbl_slavercaravan_halt(world):
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

label lbl_slavercaravan_brothel_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            img = random.choice(slavercaravan_cities['brothel_city']['images'])
            img = world.path(img)
            loc.image = img
    show expression loc.image as bg
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
            'Go for halt':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Leave' if not world.halt:
                call screen sc_slavercaravan_map(world)
                return
    return

label lbl_slavercaravan_market_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            img = random.choice(slavercaravan_cities['market_city']['images'])
            img = world.path(img)
            loc.image = img
    show expression loc.image as bg
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
            'Go for halt':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Leave' if not world.halt:
                call screen sc_slavercaravan_map(world)
                return
    return

label lbl_slavercaravan_amazon_village(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            img = random.choice(slavercaravan_cities['amazon_village']['images'])
            img = world.path(img)
            loc.image = img
    show expression loc.image as bg
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
            'Go for halt':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Leave' if not world.halt:
                call screen sc_slavercaravan_map(world)
                return
    return

label lbl_slavercaravan_sawmill_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            img = random.choice(slavercaravan_cities['sawmill_city']['images'])
            img = world.path(img)
            loc.image = img
    show expression loc.image as bg
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
            'Go for halt':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Leave' if not world.halt:
                call screen sc_slavercaravan_map(world)
                return
    return

label lbl_slavercaravan_artisan_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            img = random.choice(slavercaravan_cities['artisan_city']['images'])
            img = world.path(img)
            loc.image = img
    show expression loc.image as bg
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
            'Go for halt':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Leave' if not world.halt:
                call screen sc_slavercaravan_map(world)
                return
    return

label lbl_slavercaravan_rich_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            img = random.choice(slavercaravan_cities['rich_city']['images'])
            img = world.path(img)
            loc.image = img
    show expression loc.image as bg
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
            'Go for halt':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Leave' if not world.halt:
                call screen sc_slavercaravan_map(world)
                return
    return

label lbl_slavercaravan_wildness(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            loc.slaves = [SlaverCaravanPersonMaker.make_person(person_maker=PersonCreator) for i in range(10)]
            loc.tries = 3
            img = random.choice(slavercaravan_locations['wildness']['images'])
            img = world.path(img)
            loc.image = img
        else:
            loc.tries = 3
    show expression loc.image as bg
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
                            world.halt = True
                            break
                        else:
                            loc.tries -= 1
                    world.halt = True
                    
            'Go for halt':
                call lbl_slavercaravan_halt(world)
                $ loc.tries = 3

            'Leave' if not world.halt:
                call screen sc_slavercaravan_map(world)
                return
    return

label lbl_slavercaravan_slave_escaped(world, person):
    '[person.name] escaped'
    return

label lbl_slavercaravan_slave_escape_prevented(world, person):
    '[world.player.name] prevented escape of [person.name]'
    return