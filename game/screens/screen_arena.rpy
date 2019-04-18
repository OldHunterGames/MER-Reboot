init python:
    glad_images = {
        'golplynia': 'hoplinie.png',
        'dimacheros': {
            'female': 'dimacher_f.png',
        },
        'pugilist': {
            'female': 'pugilist_f.png'
        },
        'secutor': 'Secutor.png'
    }

    def get_glad_image(person_class, gender):
        data = glad_images.get(person_class.id)

        if isinstance(data, dict):
            return data.get(gender)
        else:
            return data
    


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
                    text fighter1.name xalign 0.5 color '#fff'
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
                    textbutton 'make a bet (%s sparks)' % arena.sparks action Function(arena.make_bet, fighter1) xalign 0.5

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
                    textbutton 'make a bet (%s sparks)' % arena.sparks action Function(arena.make_bet, fighter2) xalign 0.5

        if arena.state == 'prefight':
            $ img = get_glad_image(arena.enemy.person_class, arena.enemy.gender)
            $ standoff = arena.fight
            $ enemy_card = standoff.enemy_current_card
            image gui_image('arena/Arena_BG.png')
            if img is not None:
                image gui_image('arena/{0}'.format(img)):
                    xpos 465
                    ypos 190
            image gui_image('arena/UI_overlay.png')
            vbox:
                xalign 0.5
                ypos 15
                if standoff.winner is None:
                    text 'Choose a strategy'
                    for card in standoff.player_cards:
                        textbutton str(card.description(arena.ally, {})):
                            action Function(standoff.select_card, card)
                            text_color value_color(card.get_power(arena.ally, {}))
                            text_hover_color '#fff'
                else:
                    text 'Fight is over'
                    textbutton 'Leave' action Return()
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
                    text encolor_text(enemy_card.description(arena.enemy, {}), enemy_card.get_power(arena.enemy, {})) xalign 0.5
