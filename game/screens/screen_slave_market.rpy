init python:
    def make_starter_slave():
        slave = PersonCreator.gen_person(genus='human')
        slave.person_class = PersonClass.random_by_tag('starter')
        slave.armor = Armor.random_by_type(slave.person_class.available_garments[0])

        return slave

    class SlaveMarket(object):
        def __init__(self, player, calculator):
            self.slaves = [make_starter_slave() for i in xrange(3)]
            self.state = 'buy'
            self.player = player
            self.calculator = calculator

        def switch_mode(self):
            self.state = 'sell' if self.state == 'buy' else 'buy'

        def buy(self, slave):
            slave.exhausted = True
            self.player.slaves.append(slave)
            self.slaves.remove(slave)
            self.player.sparks -= self.calc_price(slave)
            if len(self.slaves) < 1:
                self.state = 'sell'

        def sell(self, slave):
            self.player.slaves.remove(slave)
            self.player.sparks += self.calc_price(slave)
            if len(self.player.slaves) < 1:
                self.state = 'buy'

        def can_buy(self, slave):
            return self.player.sparks >= self.calc_price(slave) and HomeManager.MAX_SLAVES > len(self.player.slaves)

        def update_slaves(self, *args, **kwargs):
            self.slaves = [make_starter_slave() for i in xrange(3)]

        def open(self):
            if len(self.slaves) > 0:
                self.state = 'buy'
            return renpy.call_screen('sc_slave_market', self)

        def calc_price(self, slave):
            return self.calculator(slave).price()

screen sc_slave_market(market):
    python:
        slaves = market.slaves if market.state == 'buy' else [i for i in market.player.slaves if not i.exhausted]
        action = market.buy if market.state == 'buy' else market.sell
        sensitivity = market.can_buy if market.state == 'buy' else lambda x: True
    tag info
    modal True
    zorder 10
    window:
        style 'char_info_window'
        hbox:
            for slave in slaves:
                vbox:
                    image slave.avatar
                    text slave.name xalign 0.5
                    text slave.person_class.colored_name() xalign 0.5
                    text 'Raiting: %s' % PriceCalculator(slave).training_price() xalign 0.5
                    text encolor_text(core_souls[slave.soul_level], slave.soul_level) xalign 0.5
                    for attr in slave.show_attributes().values():
                        text attr xalign 0.5
                    textbutton market.state + '(%s sparks)' % market.calc_price(slave):
                        action Function(action, slave), SensitiveIf(sensitivity(slave))
                        xalign 0.5

        textbutton 'leave' yalign 1.0 action Return()

        if market.state == 'sell':
            textbutton 'buy slave' action Function(market.switch_mode) xalign 1.0 yalign 1.0
        else:
            textbutton 'sell slave':
                action Function(market.switch_mode), SensitiveIf(len(market.player.slaves) > 0)
                xalign 1.0 
                yalign 1.0
