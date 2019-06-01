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
            background im.Scale('gui/marble_texture_bordered.jpg', 600, 720)
            vbox:
                spacing 10
                hbox:
                    ypos 10
                    xpos 10
                    vbox:
                        spacing 15
                        imagebutton:
                            if home.player.exhausted:
                                idle im.Scale(im.Grayscale(home.player.avatar), 150, 150)
                            else:
                                idle im.Scale(home.player.avatar, 150, 150)
                            action Function(home.select, home.player)
                        vbox:
                            text home.player.name color '#333333'
                            text 'Бюджет %s (-%s)' % (home.player.sparks, home.calc_upkeep())

                        
                            
                    vbox:
                        spacing 5
                        textbutton 'В город' action Return()
                        textbutton 'Отдыхать' action Function(home.skip_turn), Return()
                        textbutton 'Дождаться аукциона' action Function(auction.activate), Function(home.skip_turn), Return()
                        vbox:
                            text home.player.person_class.colored_name()
                            for attr in home.player.show_attributes().values():
                                text attr
                    
                vbox:
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
                                    if home.current_slave == slave:
                                        action Function(home.slave_actions)
                                    else:
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
        
        frame:
            xpos 600
            xsize 1280-600
            ysize 720
            background im.Scale('gui/marble_texture_bordered.jpg', 1280-600, 720)
            if home.current_slave is not None:
                hbox:
                    xpos 15
                    ypos 15
                    spacing 15
                    vbox:
                        spacing 15
                        
                        if home.current_slave.exhausted:
                            image im.Scale(im.Grayscale(home.current_slave.avatar), 150, 150)
                        else:
                            imagebutton:
                                idle im.Scale(home.current_slave.avatar, 150, 150)
                                action Function(home.slave_actions)
                        vbox:
                            textbutton 'Вызвать' action Function(home.slave_actions)
                            text home.current_slave.name color '#fff'
                            text home.current_slave.person_class.colored_name()
                            text 'Raiting: %s' % PriceCalculator(home.current_slave).training_price()
                            text 'Победы: %s (%s)' % (PriceCalculator(home.current_slave).current_class_wins(), PriceCalculator(home.current_slave).total_wins())
                            text encolor_text(core_souls[home.current_slave.soul_level], home.current_slave.soul_level)
                            for attr in home.current_slave.show_attributes().values():
                                text attr

                    hbox:
                        box_wrap True
                        spacing 5
                        for card in home.get_cards():
                            use fight_card_representation(card.suit(home.current_slave, {}), card.get_power(home.current_slave, {}), card.name, NullAction())
                

        