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

    for key in slavercaravan_quests:
        SlaverCaravanQuest.register_quest(key, SlaverCaravanQuest(key))

    class SlaverCaravan(World):
        PLAYER = None
        SLAVE_GUT_FOOD = 5
        FOOD_TO_WIN = 100
        MAX_DAYS = 90

        def get_event(self, loc=None):
            if loc is None:
                loc = self.locations.current_location()
            events = loc.events()
            if events is None:
                return None
            pool = list()
            for key, value in events.items():
                if isinstance(value, int):
                    pool.append((key, value))
                else:
                    pool.append((key, renpy.call_in_new_context(value, world=self)))
            return weighted_random(pool)

        def call_event(self):
            event = self.get_event()
            if event is None:
                return
            else:
                return renpy.call_in_new_context(event, world=self)

        def __init__(self, *args, **kwargs):
            super(SlaverCaravan, self).__init__(*args, **kwargs)
            self.characters = list()
            self.locations = Locations(world=self, quests=SlaverCaravanQuest.get_quests())
            self.food = 0
            self.day = 1
            self.halt = False
            self.is_at_halt = False
            self.halt_acted = False

        def critical_state_callback(self, person):
            renpy.call_in_new_context('lbl_slavercaravan_critialstate', world=self, person=person)

        def entry_label(self):
            return 'lbl_slavercaravan'

        def get_path(self):
            return 'SlaverCaravan/'

        def on_visit(self, person):
            if getattr(SlaverCaravan, 'PLAYER', None) is None:
                self.player = SlaverCaravanPersonMaker.make_person(person)
                SlaverCaravan.PLAYER = self.player
                self.player.add_event('critical_state', self.critical_state_callback)
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
            self.day += 1
            self.halt_acted = False
            if self.day > self.MAX_DAYS:
                renpy.call_in_new_context('lbl_slavercaravan_archon_end_screen', world=self, condition='loose')

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
            if person.has_status('tamed'):
                value -= 1
            return ['escape' for i in range(value)]

        def slave_to_loc(self, person):
            closest_wild = self.locations.get_closest_wildness()
            if hasattr(closest_wild, 'slaves'):
                closest_wild.slaves.append(person)
            else:
                closest_wild.slaves = [SlaverCaravanPersonMaker.make_person(person_maker=PersonCreator) for i in range(10)]
                closest_wild.slaves.append(person)

        def slaves_escape(self, value=None):
            if value is None:
                value = len(self.characters)
            for i in self.characters[0:value]:
                self.slave_to_loc(i)
                self.characters.remove(i)
        def slave_escape(self):
            for i in self.characters:
                chances = self.escape_chance(i)
                chances.extend(self.security_chance())
                result = random.choice(chances)
                if result == 'escape':
                    self.remove_character(i)
                    closest_wild = self.locations.get_closest_wildness()
                    self.slave_to_loc(i)
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
                price = max(self.selected.attributes().values())
            else:
                price = max([self.selected.attribute(i) for i in self.attributes])
            if self.selected.has_status('tamed'):
                price += 1
            price *= self.multiplier
            if self.selected.has_status('wounded'):
                price = int(price/2)
            if price <= 0:
                price = self.world.SLAVE_GUT_FOOD
            else:
                price += self.world.SLAVE_GUT_FOOD
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
            self.world.food += self.world.SLAVE_GUT_FOOD
            self.selected = None

        def tame(self):
            self.selected.add_status('tamed')
            self.world.halt_acted = True
            renpy.call_in_new_context('lbl_slavercaravan_tame', world=self.world, target=self.selected)

        def rape(self):
            self.selected.add_status('wounded')
            self.world.player.state += 1
            self.world.halt_acted = True
            renpy.call_in_new_context('lbl_slavercaravan_rape', world=self.world, target=self.selected)

        def can_tame(self):
            status_check =self.selected.has_status('wounded') or self.selected.has_status('tamed')
            return not status_check and self.world.is_at_halt and not self.world.halt_acted

        def can_rape(self):
            return not self.selected.has_status('wounded') and self.world.is_at_halt and not self.world.halt_acted

        def can_make_food(self):
            return not self.world.halt_acted and self.world.is_at_halt
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
            self.world.food += self.world.SLAVE_GUT_FOOD
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
    show expression world.path('bg/archon.png') as bg
    menu:
        "Kneel in ave before me, mortal for as the archon of this world, [world.archon.name]. The adventure of the slave hunt is beyound this gates."
        "How can I please you?":
            "Make a hundred food before the summer passes (90 days) and I'll make you my apostole."
            call lbl_slavercaravan(world)
        "Let me in":
            call lbl_slavercaravan_main(world)
        "I'll return to Eternal Rome":
            $ pass
    return

label lbl_pray_archon(world):
    show expression world.path('bg/archon.png') as bg
    while True:
        menu:
            "Kneel in ave before me, mortal for as the archon of this world, [world.archon.name]. The adventure of the slave hunt is beyound this gates."
            "How can I please you?":
                "Make a hundred food before month get old and I'll make you my apostole."
            "Become apostol" if world.food >= 100:
                $ world.sync()
            "I'll return to Eternal Rome":
                $ world.leave()
            "Leave":
                return
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
        event = world.call_event()
    show expression loc.image as bg
    'Road'
    while True:
        menu:
            'Leave' if not world.halt:
                call lbl_slavercaravan_change_location(world)
                return
            'Setup a camp':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
    return

label lbl_slavercaravan_halt(world):
    $ world.halt = True
    $ world.is_at_halt = True
    while world.halt:
        menu:
            'You have some time before night falls.'
            'Go to sleep':
                $ world.halt = False
                $ world.is_at_halt = False
                $ world.skip_turn()
            'Pray to archon':
                $ renpy.call_in_new_context('lbl_pray_archon', world=world)

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
    show expression loc.image as bg
    while True:
        $ text = loc.random_text('entry_text')
        menu:
            "[text]"
            'Sell slaves' if len(world.characters) > 0:
                if len(world.get_slaves('female')) > 0:
                    $ SlaverMarket(world.get_slaves('female'), world, 3).show()
                else:
                    $ pass
            'Buy items':
                call lbl_buy_item(world)
            'Rent a room':
                $ world.player.state += 1
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Quest' if loc.quest is not None:
                $ renpy.call_in_new_context(loc.quest.label(), world=world)
            'Leave' if not world.halt:
                call lbl_slavercaravan_change_location(world)
                return
    return

label lbl_slavercaravan_market_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
    show expression loc.image as bg
    while True:
        $ text = loc.random_text('entry_text')
        menu:
            "[text]"
            'Sell slaves' if len(world.characters) > 0:
                if len(world.get_slaves()) > 0:
                    $ SlaverMarket(world.get_slaves(), world, 2).show()
                else:
                    $ pass
            'Buy items':
                call lbl_buy_item(world)
            'Rent a room':
                $ world.player.state += 1
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Quest' if loc.quest is not None:
                $ renpy.call_in_new_context(loc.quest.label(), world=world)
            'Leave' if not world.halt:
                call lbl_slavercaravan_change_location(world)
                return
    return

label lbl_slavercaravan_amazon_village(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
    show expression loc.image as bg
    while True:
        $ text = loc.random_text('entry_text')
        menu:
            "[text]"
            'Sell slaves' if len(world.characters) > 0:
                if len(world.get_slaves('male')) > 0:
                    $ SlaverMarket(world.get_slaves('male'), world, 3).show()
                else:
                    $ pass
            'Buy items':
                call lbl_buy_item(world)
            'Rent a room':
                $ world.player.state += 1
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Quest' if loc.quest is not None:
                $ renpy.call_in_new_context(loc.quest.label(), world=world)
            'Leave' if not world.halt:
                call lbl_slavercaravan_change_location(world)
                return
    return

label lbl_slavercaravan_sawmill_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
    show expression loc.image as bg
    while True:
        $ text = loc.random_text('entry_text')
        menu:
            "[text]"
            'Sell slaves' if len(world.characters) > 0:
                if len(world.get_slaves()) > 0:
                    $ SlaverMarket(world.get_slaves(), world, 5, ['might']).show()
                else:
                    $ pass
            'Buy items':
                call lbl_buy_item(world)
            'Rent a room':
                $ world.player.state += 1
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Quest' if loc.quest is not None:
                $ renpy.call_in_new_context(loc.quest.label(), world=world)
            'Leave' if not world.halt:
                call lbl_slavercaravan_change_location(world)
                return
    return

label lbl_slavercaravan_artisan_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
    show expression loc.image as bg
    while True:
        $ text = loc.random_text('entry_text')
        menu:
            "[text]"
            'Sell slaves' if len(world.characters) > 0:
                if len(world.get_slaves()) > 0:
                    $ SlaverMarket(world.get_slaves(), world, 5, ['competence']).show()
                else:
                    $ pass
            'Buy items':
                call lbl_buy_item(world)
            'Rent a room':
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Quest' if loc.quest is not None:
                $ renpy.call_in_new_context(loc.quest.label(), world=world)
            'Leave' if not world.halt:
                call lbl_slavercaravan_change_location(world)
                return
    return

label lbl_slavercaravan_rich_city(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
    show expression loc.image as bg
    while True:
        $ text = loc.random_text('entry_text')
        menu:
            "[text]"
            'Sell slaves' if len(world.characters) > 0:
                if len(world.get_slaves()) > 0:
                    $ SlaverMarket(world.get_slaves(), world, 5, ['charisma', 'subtlety']).show()
                else:
                    $ pass
            'Buy items':
                call lbl_buy_item(world)
            'Rent a room':
                $ world.player.state += 1
                $ world.halt = True
                call lbl_slavercaravan_halt(world)
            'Quest' if loc.quest is not None:
                $ renpy.call_in_new_context(loc.quest.label(), world=world)
            'Leave' if not world.halt:
                call lbl_slavercaravan_change_location(world)
                return
    return

label lbl_slavercaravan_wildness(world):
    python:
        loc = world.locations.current_location()
        if not loc.visited:
            loc.visited = True
            if not hasattr(loc, 'slaves'):
                loc.slaves = [SlaverCaravanPersonMaker.make_person(person_maker=PersonCreator) for i in range(10)]
            loc.tries = 3
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
                            if loc.tries > 1:
                                choice = renpy.display_menu(
                                    [('Try again', 'try')]
                                )
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
                    if slave is not None and not catch.catched:
                        renpy.display_menu(
                            [('End of the day', 'end')]
                        )
                    world.halt = True

            'Setup a camp':
                call lbl_slavercaravan_halt(world)
                $ loc.tries = 3

            'Travel' if not world.halt:
                call lbl_slavercaravan_change_location(world)
                return
    return

label lbl_slavercaravan_slave_escaped(world, person):
    '[person.name] escaped'
    return

label lbl_slavercaravan_slave_escape_prevented(world, person):
    '[world.player.name] prevented escape of [person.name]'
    return

label lbl_slavercaravan_change_location(world):
    python:
        available_locations = world.locations.locs_to_go()
    menu:
        'North' if available_locations['top'] is not None:
            $ world.change_location(available_locations['top'])
        'South' if available_locations['bot'] is not None:
            $ world.change_location(available_locations['bot'])
        'West' if available_locations['left'] is not None:
            $ world.change_location(available_locations['left'])
        'East' if available_locations['right'] is not None:
            $ world.change_location(available_locations['right'])
    return

label lbl_slavercaravan_archon_end_screen(world, condition):
    if condition == 'win':
        world.archon 'You win'
    elif condition == 'loose':
        world.archon 'You loose'
    $ world.leave()
    return

label lbl_slavercaravan_tame(world, target):
    return

label lbl_slavercaravan_rape(world, target):
    return

label lbl_slavercaravan_critialstate(world, person):
    return
