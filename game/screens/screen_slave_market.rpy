screen sc_slave_market(market):
    python:
        slaves = market.slaves if market.state == 'buy' else market.player.slaves
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
