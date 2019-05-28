screen sc_home(home):

    tag info
    modal True
    zorder 10
    window:
        style 'char_info_window'
        
        hbox:
            vbox:
                ypos 10
                spacing 15
                if home.player.exhausted:
                    image im.Scale(im.Grayscale(home.player.avatar), 150, 150)
                else:
                    image im.Scale(home.player.avatar, 150, 150)
                vbox:
                    xalign 0.5
                    text home.player.name xalign 0.5 color '#fff'
                    text home.player.person_class.colored_name() xalign 0.5
            vbox:
                spacing 5
                textbutton 'Leave' action Return()
                textbutton 'Skip turn' action Function(home.skip_turn), Return()
                text 'Current upkeep: %s' % home.calc_upkeep()

        if home.current_slave is not None:
            hbox:
                xalign 0.95
                ypos 10
                spacing 10
                hbox:
                    box_wrap True
                    xmaximum 400
                    spacing 5
                    for card in home.current_slave.get_cards('all'):
                        use fight_card_representation(card.suit(home.current_slave, {}), card.get_power(home.current_slave, {}), card.name, NullAction())
                vbox:
                    spacing 15
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
                            xalign 0.5
                            text home.current_slave.name xalign 0.5 color '#fff'
                            text home.current_slave.person_class.colored_name() xalign 0.5
                            text 'Raiting: %s' % PriceCalculator(home.current_slave).training_price()
                            text encolor_text(core_souls[home.current_slave.soul_level], home.current_slave.soul_level) xalign 0.5
                            for attr in home.current_slave.show_attributes().values():
                                text attr xalign 0.5
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

        hbox:
            yalign 0.9
            spacing 15
            for slave in home.slaves:
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