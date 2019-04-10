screen sc_home(home):

    tag info
    modal True
    zorder 10
    window:
        style 'char_info_window'
        
        vbox:
            ypos 10
            spacing 15
            image im.Scale(home.player.avatar, 250, 250)
            vbox:
                xalign 0.5
                text home.player.name xalign 0.5 color '#fff'
                text home.player.person_class.colored_name() xalign 0.5

        textbutton 'Leave' xalign 0.5 action Return()
        textbutton 'Skip turn' xalign 0.5 yalign 0.1 action Function(home.skip_turn), Return()
        text 'Current upkeep: %s' % home.calc_upkeep() xalign 0.5 yalign 0.2

        if home.current_slave is not None:
            vbox:
                xalign 1.0
                ypos 10
                spacing 15
                image im.Scale(home.current_slave.avatar, 250, 250)
                vbox:
                    xalign 0.5
                    text home.current_slave.name xalign 0.5 color '#fff'
                    text home.current_slave.person_class.colored_name() xalign 0.5
                    text home.current_slave.armor.name xalign 0.5 color '#fff'
                    text encolor_text(core_souls[home.current_slave.soul_level], home.current_slave.soul_level) xalign 0.5
                    for attr in home.current_slave.show_attributes().values():
                        text attr xalign 0.5
                    for attack in home.current_slave.person_class.attack_suits:
                        if attack != 'skull':
                            text Suits.as_attack_type(attack) xalign 0.5 color '#fff'
                    for attack in home.current_slave.person_class.attack_types:
                        text attack xalign 0.5 color '#fff'

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

        hbox:
            yalign 0.9
            spacing 15
            for slave in home.slaves:
                vbox:
                    xpos 10
                    ypos 10
                    spacing 15
                    imagebutton:
                        idle im.Scale(slave.avatar, 200, 200)
                        action Function(home.select, slave)
                    vbox:
                        xalign 0.5
                        text slave.name xalign 0.5 color '#fff'
                        text slave.person_class.colored_name() xalign 0.5