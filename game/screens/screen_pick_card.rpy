screen sc_pick_sex_card(picker):
    zorder 10
    modal True
    $ cards = picker.cards
    window:
        xsize 400
        ysize 400
        xalign 0.5
        yalign 0.5
        background None
        text 'Pick a card':
            xalign 0.5

        if not picker.revealed:
            frame:
                ysize 200
                xsize 150
                yalign 0.2
                vbox:
                    text cards[0].id
                    text cards[0].type()
                    text cards[0].activity()
                    textbutton 'Pick':
                        action Return(cards[0])

        frame:
            ysize 200
            xsize 150
            xalign 1.0
            yalign 0.2
            if not picker.revealed:
                vbox:
                    text 'Hidden Card'
                    textbutton 'Reveal':
                        action Function(picker.reveal)
            else:
                vbox:
                    text cards[1].id
                    text cards[1].type()
                    text cards[1].activity()
                    textbutton 'Pick':
                        action Return(cards[1])
