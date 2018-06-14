label lbl_core_duel(duel):
    call screen sc_core_duel(duel)
    return

label lbl_core_duel_end(text):
    '[text]'
    return


screen sc_duel_card_repr(card):
    frame:
        xsize 100
        ysize 150
        vbox:
            text card.name()
        transclude

label lbl_duel_drop_card(cards):
    $ card = renpy.call_screen('sc_duel_drop_card', cards=cards)
    return card

screen sc_duel_drop_card(cards):
    
    frame:
        xalign 0.5
        yalign 0.5
        xsize 400
        ysize 200
        text 'Drop a card':
            xalign 0.5

        hbox:
            spacing 10
            yalign 0.5
            xalign 0.5
            for i in cards:
                use sc_duel_card_repr(i):
                    textbutton 'Drop':
                        yalign 1.0
                        action Return(i)


screen sc_core_duel(duel):
    
    frame:
        xsize 1000
        xalign 0.5
        ysize 170
        hbox:
            xalign 0.5
            spacing 5
            yalign 0.5
            for i in duel.hand[duel.person]:
                use sc_duel_card_repr(i)

    fixed:
        use sc_duel_card_repr(duel.played_cards[duel.person])
        xpos 590
        ypos 180

    textbutton 'End turn':
        ypos 340
        xpos 590
        action Function(duel.get_round_winner)
        sensitive (duel.played_cards[duel.player] is not None)

    if duel.played_cards[duel.player] is not None:
        fixed:
            use sc_duel_card_repr(duel.played_cards[duel.player])
            xpos 590
            ypos 390

    frame:
        xsize 1000
        xalign 0.5
        ypos 550
        ysize 170
        hbox:
            xalign 0.5
            spacing 5
            yalign 0.5
            for i in duel.hand[duel.player]:
                use sc_duel_card_repr(i):
                    textbutton 'Play':
                        action Function(duel.player_play_card, i)
                        yalign 1.0