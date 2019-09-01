screen sc_sex(sex):
    $ participants = sex.participants
    $ positions = sex.filter(SexAction.get_by_type('pose'))
    $ behaviors = sex.filter(SexAction.get_by_type('behavior'))
    $ actions = sex.filter(SexAction.get_by_type('action'))
    window:
        style 'char_info_window'
        background '#777777'

        textbutton 'Leave' action Return():
            xalign 1.0
            yalign 1.0
        frame:
            image im.Scale(sex.participants[0].person.avatar, 100, 100)

        frame:
            xalign 0.5
            text 'Placeholder'

        frame:
            yalign 0.3
            xsize 1260
            text sex.action_multikey_description()

        frame:
            yalign 1.0

            hbox:
                vbox:
                    for i in positions:
                        textbutton i.name():
                            action Function(sex.apply_action, i)
                vbox:
                    for i in behaviors:
                        textbutton i.name():
                            action Function(sex.apply_action, i)
                vbox:
                    for i in actions:
                        textbutton i.name():
                            action Function(sex.apply_action, i)