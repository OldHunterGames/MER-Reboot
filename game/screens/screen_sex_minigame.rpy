
screen sc_sex_minigame(sex_game):
    zorder 10
    modal True
    frame:
        background Color('FF69B480')
        xsize 1280
        ysize 720

        frame:
            xalign 0.5
            xsize 250
            ysize 30
            text sex_minigame_pleasure[sex_game.person_pleasure]:
                color value_color(sex_game.person_pleasure)
                xalign 0.5
                yalign 0.5
        frame:
            ypos 35
            xpos 40
            xsize 1200
            ysize 200
            hbox:
                spacing 10
                yalign 0.5
                vbox:
                    image im.Scale(sex_game.person.avatar, 160, 160)
                    text sex_game.person.name:
                        xalign 0.5
                    # TODO: orientation, fetishes
                for card in sex_game.person_cards:
                    use sc_sexcard_repr(card, 150, 190)

        imagebutton:
            idle im.Scale('gui/button_ok.png', 100, 100)
            action Return()
            ypos 290

        frame:
            ypos 240
            xsize 1060
            ysize 200
            xpos 110
            hbox:
                yalign 0.5
                spacing 10
                xalign 0.5
                for card in sex_game.get_card_slots():
                    if card is None:
                        image im.Scale(card_back(), 150, 190)
                    else:
                        use sc_sexcard_repr(card, 150, 190)

        frame:
            ypos 445
            xpos 40
            xsize 1200
            ysize 200
            hbox:
                spacing 10
                yalign 0.5
                vbox:
                    image im.Scale(sex_game.player.avatar, 160, 160)
                    text sex_game.player.name:
                        xalign 0.5
                for card in sex_game.get_player_hand():
                    if sex_game.can_play():
                        $ action=(Function(sex_game.play_card, card), "Play")
                    else:
                        $ action = None
                    use sc_sexcard_repr(card, 150, 190, action=action)

        frame:
            xalign 0.5
            xsize 250
            ysize 30
            ypos 650
            text sex_minigame_pleasure[sex_game.player_pleasure]:
                color value_color(sex_game.player_pleasure)
                xalign 0.5
                yalign 0.5
