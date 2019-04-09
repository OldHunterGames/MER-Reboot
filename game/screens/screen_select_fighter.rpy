screen sc_select_fighter(selector):
    python:
        fighter1 = selector.current_fighter()
        fighter2 = selector.enemy

    tag info
    modal True
    zorder 10
    window:
        style 'char_info_window'
        text 'Select fighter':
            xalign 0.5
        textbutton 'Run away':
            xalign 0.5
            yalign 0.1
            action Function(selector.escape), Return()

        vbox:
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

        vbox:
            xalign 1.0
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
            hbox:
                xalign 0.5
                textbutton 'previous':
                    action Function(selector.prev), SensitiveIf(selector.prev_active())
                textbutton 'next':
                    action Function(selector.next), SensitiveIf(selector.next_active())

            
            textbutton 'select' action Return() xalign 0.5

        if fighter1 == selector.player:
                text "You gonna fight personaly. If you lose it's a game over. Are you shure?":
                    color '#ff0000'
                    xalign 0.5
                    yalign 0.95
