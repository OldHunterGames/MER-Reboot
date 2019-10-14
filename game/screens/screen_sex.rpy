screen sc_sex(sex):
    $ participants = sex.participants
    $ positions = sex.filter(SexAction.get_by_type('pose'))
    $ behaviors = sex.filter(SexAction.get_by_type('behavior'))
    $ actions = sex.filter(SexAction.get_by_type('action'))
    
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
                text 'thrill: %s' % sex.participants[0].thrill
                text 'interest: %s' % sex.participants[0].interest
        frame:
            xalign 1.0
            vbox:
                image im.Scale(sex.target.person.avatar, 100, 100)
                text 'thrill: %s' % sex.target.thrill
                text 'interest: %s' % sex.target.interest

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
                if sex.next_action() == 'pose':
                    vbox:
                        text 'Select pose'
                        for i in sex.filter_actions(positions):
                            textbutton i.name():
                                action Function(sex.apply_action, i)
                if sex.next_action() == 'behavior':
                    vbox:
                        text 'Select behavior'
                        for i in sex.filter_actions(behaviors):
                            textbutton i.name():
                                text_bold sex.is_active_behavior(i)
                                action Function(sex.apply_action, i)
                if sex.next_action() == 'action':
                    vbox:
                        text 'Select action'
                        for i in sex.filter_actions(actions):
                            textbutton i.name():
                                action Function(sex.apply_action, i)