screen sc_arena(arena):
    python:
        fighter1 = arena.fighter1
        fighter2 = arena.fighter2

    tag info
    modal True
    zorder 10
    window:
        style 'char_info_window'
        
        if arena.state == 'selection':
            background gui_image('arena/Arena_BG.png')
            image gui_image('arena/UI_overlay.png')
            text 'Next fight preview':
                xalign 0.5
                ypos 10

            vbox:
                xpos 10
                ypos 10
                spacing 15
                image im.Scale(fighter1.avatar, 333, 346)
                vbox:
                    xalign 0.5
                    text fighter1.name xalign 0.5
                    text fighter1.person_class.colored_name() xalign 0.5
                    text fighter1.armor.name xalign 0.5 color '#fff'
                    text encolor_text(core_souls[fighter1.soul_level], fighter1.soul_level) xalign 0.5
                    for attr in fighter1.show_attributes().values():
                        text attr xalign 0.5
                    for attack in fighter1.person_class.attack_suits:
                        if attack != 'skull':
                            text Suits.as_attack_type(attack) xalign 0.5 color '#fff'
                    for attack in fighter1.person_class.attack_types:
                        text attack xalign 0.5 color '#fff'
                    textbutton 'make a bet' action Function(arena.make_bet, fighter1) xalign 0.5

            textbutton 'Next fight' action Return('next') xalign 0.5 yalign 0.9:
                text_color '#fff'
                text_hover_color '#00ff00'
            textbutton 'Leave' action Return('leave_arena') xalign 0.5 yalign 1.0:
                text_color '#fff'
                text_hover_color '#ffff00'
            vbox:
                xpos 935
                ypos 10
                spacing 15
                image im.Scale(fighter2.avatar, 333, 346)
                vbox:
                    xalign 0.5
                    text fighter2.name xalign 0.5 color '#fff'
                    text fighter2.person_class.colored_name() xalign 0.5
                    text fighter2.armor.name xalign 0.5 color '#fff'
                    text encolor_text(core_souls[fighter2.soul_level], fighter2.soul_level) xalign 0.5
                    for attr in fighter2.show_attributes().values():
                        text attr xalign 0.5
                    for attack in fighter2.person_class.attack_suits:
                        if attack != 'skull':
                            text Suits.as_attack_type(attack) xalign 0.5 color '#fff'
                    for attack in fighter2.person_class.attack_types:
                        text attack xalign 0.5 color '#fff'
                    textbutton 'make a bet' action Function(arena.make_bet, fighter2) xalign 0.5

        if arena.state == 'prefight':
            image gui_image('arena/Arena_BG.png')
            image gui_image('arena/UI_overlay.png')
            vbox:
                xalign 0.5
                ypos 15
                text 'Choose a strategy'
                for attack in arena.ally.person_class.get_attacks():
                    textbutton str(attack):
                        action Function(arena.select_attack, attack), Return()
                        text_color value_color(attack.power(arena.ally))
                        text_hover_color '#fff'
            vbox:
                xpos 10
                ypos 10
                spacing 15
                image im.Scale(arena.ally.avatar, 333, 346)
                vbox:
                    xalign 0.5
                    text arena.ally.name color '#fff'
                    text arena.ally.person_class.colored_name()                    

            vbox:
                xpos 935
                ypos 10
                spacing 15
                image im.Scale(arena.enemy.avatar, 333, 346)
                vbox:
                    xalign 0.5
                    text arena.enemy.name color '#fff'
                    text arena.enemy.person_class.colored_name()
                    text arena.enemy_attack.colored(arena.enemy) xalign 0.5

            

screen sc_arena_results(fight):

    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        ysize 300

        if fight.counter < 1:
            hbox:
                xalign 0.5
                yalign 0.5
                for i in range(abs(fight.counter - 1)):
                    image gui_image('loser.png')
        else:
            hbox:
                xalign 0.5
                yalign 0.5
                for i in range(fight.counter):
                    image gui_image('winner.png')

