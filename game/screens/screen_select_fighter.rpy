screen sc_select_fighter(selector):
    python:
        fighter1 = selector.current_fighter()
        fighter2 = selector.enemy

    tag info
    modal True
    zorder 10
    window:
        background gui_image('arena/Arena_BG.png')
        image gui_image('arena/UI_overlay.png')
        style 'char_info_window'
        text 'Select fighter':
            xalign 0.5
        textbutton 'Run away':
            xalign 0.5
            yalign 0.1
            action Function(selector.escape), Return()

        vbox:
            spacing 15
            xpos 10
            ypos 10
            image im.Scale(fighter2.avatar, 333, 346)
            text fighter2.name xalign 0.5 color '#ffffff'
            text fighter2.person_class.colored_name() xalign 0.5
            text encolor_text(core_souls[fighter2.soul_level], fighter2.soul_level) xalign 0.5
            hbox:
                xalign 0.5
                spacing 5
                for card in fighter2.get_cards('combat'):
                    use fight_card_representation(card.suit(fighter2, {}), card.get_power(fighter2, {}), card.name, NullAction())

        vbox:
            spacing 15
            xpos 935
            ypos 10
            image im.Scale(fighter1.avatar, 333, 346)
            text fighter1.name xalign 0.5 color '#ffffff'
            text fighter1.person_class.colored_name() xalign 0.5
            hbox:
                spacing 5
                xalign 0.5
                for card in fighter1.get_cards('combat'):
                    use fight_card_representation(card.suit(fighter1, {}), card.get_power(fighter1, {}), card.name, NullAction())
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
                    yalign 0.9
                    xmaximum 500
