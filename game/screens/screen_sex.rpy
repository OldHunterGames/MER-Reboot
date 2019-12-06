screen sc_sex(sex):
    $ participants = sex.participants
    
    window:
        style 'char_info_window'
        use sc_gui
        background '#777777'

        textbutton 'Leave' action Return():
            xalign 1.0
            yalign 1.0
        frame:
            vbox:
                image im.Scale(sex.participants[0].person.avatar, 100, 100)
        frame:
            xalign 1.0
            vbox:
                image im.Scale(sex.participants[1].person.avatar, 100, 100)
        frame:
            xalign 0.5
            text 'Placeholder'

        frame:
            yalign 0.3
            xsize 1260
            text sex.current_description()

        frame:
            yalign 1.0

            hbox:
                vbox:
                    text 'Select action'
                    if sex.can_go_back():
                        textbutton 'Back' action Function(sex.go_back)
                    for i in sex.available_actions():
                        textbutton i.name:
                            action Function(sex.apply_action, i)