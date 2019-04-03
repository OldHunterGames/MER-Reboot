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
            text 'Next fight preview':
                xalign 0.5

            vbox:
                image fighter1.avatar
                text fighter1.name xalign 0.5
                text fighter1.person_class.colored_name() xalign 0.5
                text fighter1.armor.name xalign 0.5
                text encolor_text(core_souls[fighter1.soul_level], fighter1.soul_level) xalign 0.5
                for attr in fighter1.show_attributes().values():
                    text attr xalign 0.5
                for attack in fighter1.person_class.attack_suits:
                    if attack != 'skull':
                        text Suits.as_attack_type(attack) xalign 0.5
                for attack in fighter1.person_class.attack_types:
                    text attack xalign 0.5
                textbutton 'make a bet' action Function(arena.make_bet, fighter1)  xalign 0.5

            textbutton 'Next fight' action Return(True) xalign 0.5 yalign 0.9

            vbox:
                xalign 1.0
                image fighter2.avatar
                text fighter2.name xalign 0.5
                text fighter2.person_class.colored_name() xalign 0.5
                text fighter2.armor.name xalign 0.5
                text encolor_text(core_souls[fighter2.soul_level], fighter2.soul_level) xalign 0.5
                for attr in fighter2.show_attributes().values():
                    text attr xalign 0.5
                for attack in fighter2.person_class.attack_suits:
                    if attack != 'skull':
                        text Suits.as_attack_type(attack) xalign 0.5
                for attack in fighter2.person_class.attack_types:
                    text attack xalign 0.5
                textbutton 'make a bet' action Function(arena.make_bet, fighter2) xalign 0.5
        if arena.state == 'prefight':
            vbox:
                xalign 0.5
                text 'Choose a strategy'
                for attack in arena.ally.person_class.get_attacks():
                    textbutton str(attack):
                        action Function(arena.select_attack, attack), Return()
                        text_color value_color(attack.power(arena.ally))
                        text_hover_color '#fff'
                
            hbox:
                vbox:
                    image arena.enemy.avatar
                    text arena.enemy_attack.colored(arena.enemy) xalign 0.5
                vbox:
                    text arena.enemy.name
                    text arena.enemy.person_class.colored_name()

            hbox:
                xalign 1.0
                yalign 1.0
                vbox:
                    text arena.ally.name
                    text arena.ally.person_class.colored_name()
                vbox:
                    image arena.ally.avatar

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

