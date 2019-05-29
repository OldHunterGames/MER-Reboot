screen sc_home(home):
    python:
        first_row = home.slaves[0:3]
        second_row = home.slaves[3:5]
    tag info
    modal True
    zorder 10
    window:
        style 'char_info_window'
        frame:
            xsize 600
            ysize 720
            hbox:
                vbox:
                    ypos 10
                    spacing 15
                    imagebutton:
                        if home.player.exhausted:
                            idle im.Scale(im.Grayscale(home.player.avatar), 150, 150)
                        else:
                            idle im.Scale(home.player.avatar, 150, 150)
                        action Function(home.select, home.player)
                    vbox:
                        xalign 0.5
                        text home.player.name xalign 0.5 color '#fff'
                        text home.player.person_class.colored_name() xalign 0.5
                vbox:
                    spacing 5
                    textbutton 'Leave' action Return()
                    textbutton 'Skip turn' action Function(home.skip_turn), Return()
                    text 'Current upkeep: %s' % home.calc_upkeep()
            vbox:
                yalign 0.9
                spacing 10
                hbox:
                    spacing 15
                    for slave in first_row:
                        vbox:
                            xpos 10
                            ypos 10
                            spacing 15
                            imagebutton:
                                if slave.exhausted:
                                    idle im.Scale(im.Grayscale(slave.avatar), 150, 150)
                                else:
                                    idle im.Scale(slave.avatar, 150, 150)
                                action Function(home.select, slave)
                            vbox:
                                xalign 0.5
                                text slave.name xalign 0.5 color '#fff'
                                text slave.person_class.colored_name() xalign 0.5
                hbox:
                    xalign 0.5
                    spacing 15
                    for slave in second_row:
                        vbox:
                            xpos 10
                            ypos 10
                            spacing 15
                            imagebutton:
                                if slave.exhausted:
                                    idle im.Scale(im.Grayscale(slave.avatar), 150, 150)
                                else:
                                    idle im.Scale(slave.avatar, 150, 150)
                                action Function(home.select, slave)
                            vbox:
                                xalign 0.5
                                text slave.name xalign 0.5 color '#fff'
                                text slave.person_class.colored_name() xalign 0.5
        
        if home.current_slave is not None:
            vbox:
                spacing 15
                xpos 600
                if home.current_slave.exhausted:
                    image im.Scale(im.Grayscale(home.current_slave.avatar), 150, 150)
                else:
                    image im.Scale(home.current_slave.avatar, 150, 150)
                hbox:
                    xsize 150
                    textbutton 'Stats':
                        action Function(home.switch_mode, 'stats')
                        selected home.mode == 'stats'
                    textbutton 'Actions':
                        action Function(home.switch_mode, 'actions'), SensitiveIf(not home.current_slave.exhausted)
                        xalign 1.0
                        selected home.mode == 'actions'
                if home.mode == 'stats':
                    vbox:
                        text home.current_slave.name color '#fff'
                        text home.current_slave.person_class.colored_name()
                        text 'Raiting: %s' % PriceCalculator(home.current_slave).training_price()
                        text encolor_text(core_souls[home.current_slave.soul_level], home.current_slave.soul_level)
                        for attr in home.current_slave.show_attributes().values():
                            text attr
                if home.mode == 'actions':
                    if home.can_upgrade_slave(home.current_slave):
                        text 'Available upgrades'
                        for i in home.slave_upgrades(home.current_slave):
                            python:
                                text = i.name
                                if i.cost > 0:
                                    text += '(%s sparks)' % i.cost
                            textbutton text:
                                text_color value_color(i.tier)
                                action Function(home.upgrade_slave, home.current_slave, i), SensitiveIf(home.player.sparks >= i.cost)
                                text_hover_color '#000'

                    if not home.current_slave.exhausted:
                        text 'Actions'
                        if len(home.persons_for_selection(home.can_attend_party)) > 0:
                            textbutton 'Attend party' action Function(SimpleSelector(home.persons_for_selection(home.can_attend_party), FuncCommand(home.attend_party, home.current_slave)).show)
                        if len(home.persons_for_selection(home.can_make_love)) > 0:
                            textbutton 'Make love' action Function(SimpleSelector(home.persons_for_selection(home.can_make_love), FuncCommand(home.make_love, home.current_slave)).show)
                        if home.can_train(home.current_slave):
                            textbutton 'Train' action Function(home.train, home.current_slave)
                        if home.can_sell(home.current_slave):
                            textbutton 'Sell (%s sparks)' % PriceCalculator(home.current_slave).price() action Function(home.sell, home.current_slave)

        
        if home.current_slave is not None:
            frame:
                xpos 800
                xsize 1280-800
                ysize 720
                background im.Scale('gui/marble_texture_bordered.jpg', 1280-800, 720)
                hbox:
                    xalign 0.05
                    yalign 0.02
                    textbutton 'Combat':
                        action Function(home.show_cards, 'combat')
                        selected home.cards_mode == 'combat'
                    textbutton 'Social':
                        action Function(home.show_cards, 'social')
                        selected home.cards_mode == 'social'
                hbox:
                    yalign 0.1
                    xalign 0.05
                    box_wrap True
                    spacing 5
                    for card in home.get_cards():
                        use fight_card_representation(card.suit(home.current_slave, {}), card.get_power(home.current_slave, {}), card.name, NullAction())
                

        