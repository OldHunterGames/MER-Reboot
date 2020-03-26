screen sc_quirk_selection(quirks_suggestions, field):
    tag quirk
    zorder 20
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        vbox:
            for quirk in Quirk.get_quirks():
                textbutton quirk.name action Function(quirks_suggestions.suggest, field, quirk), Hide('sc_quirk_selection')

screen sc_nature_selection(quirks_suggestions):
    tag quirk
    zorder 20
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        vbox:
            for nature in NatureData.natures():
                textbutton nature action Function(quirks_suggestions.suggest, 'nature', nature), Hide('sc_nature_selection')


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
                            if not core.player_can_act():
                                idle im.Scale(im.Grayscale(home.player.avatar), 150, 150)
                            else:
                                idle im.Scale(home.player.avatar, 150, 150)
                            action NullAction()
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
                                    if not core.can_act(slave):
                                        idle im.Scale(im.Grayscale(slave.avatar), 150, 150)
                                    else:
                                        idle im.Scale(slave.avatar, 150, 150)
                                    if home.current_slave == slave and core.can_act(slave):
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
                                    if not core.can_act(slave):
                                        idle im.Scale(im.Grayscale(slave.avatar), 150, 150)
                                    else:
                                        idle im.Scale(slave.avatar, 150, 150)
                                    if home.current_slave == slave and core.can_act(slave):
                                        action Function(home.slave_actions)
                                    else:
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
                $ quirks_suggestions = QuirksSuggestions(home.current_slave)
                $ class_data = ClassData(home.current_slave)
                python:
                    quirk1_text = '???' if quirks_suggestions.get_suggestion('quirk1') is None else quirks_suggestions.get_suggestion('quirk1').name
                    quirk2_text = '???' if quirks_suggestions.get_suggestion('quirk2') is None else quirks_suggestions.get_suggestion('quirk2').name
                    nature_text = '???' if quirks_suggestions.get_suggestion('nature') is None else quirks_suggestions.get_suggestion('nature')
                hbox:
                    xpos 15
                    ypos 15
                    spacing 15
                    vbox:
                        spacing 15
                        
                        if not core.can_act(home.current_slave):
                            image im.Scale(im.Grayscale(home.current_slave.avatar), 150, 150)
                        else:
                            imagebutton:
                                idle im.Scale(home.current_slave.avatar, 150, 150)
                                action Function(home.slave_actions)
                        vbox:
                            if core.can_act(home.current_slave):
                                imagebutton:
                                    idle 'gui/btn_callslave.png'
                                    action Function(home.slave_actions)
                            # Gladiators info block
                            # text home.current_slave.name color '#fff'
                            # text home.current_slave.person_class.colored_name()
                            # text 'Победы: %s (%s)' % (PriceCalculator(home.current_slave).total_wins(), PriceCalculator(home.current_slave).current_class_wins())
                            # text encolor_text(core_souls[home.current_slave.soul_level], home.current_slave.soul_level)
                            # for attr in home.current_slave.show_attributes().values():
                            #     text attr
                            text SlaveClassTree(home.current_slave).get_class()
                            text 'Backgound: %s' % class_data.get_background().name()
                            text 'Class: %s' % class_data.get_class().name()
                            text home.current_slave.feature_by_slot('background').name()
                            text 'Obedience: %s' % Slave(home.current_slave).obedience()
                            textbutton quirk1_text action Show('sc_quirk_selection', None, quirks_suggestions, 'quirk1')
                            textbutton quirk2_text action Show('sc_quirk_selection', None, quirks_suggestions, 'quirk2')
                            textbutton nature_text action Show('sc_nature_selection', None, quirks_suggestions)
                    # Gladiators cards
                    # hbox:
                    #     box_wrap True
                    #     spacing 5
                    #     for card in home.get_cards():
                    #         use fight_card_representation(card, card.suit(home.current_slave, {}), card.get_power(home.current_slave, {}), card.name, NullAction())
                

        