screen sc_simple_selector(selector):
    modal True
    zorder 100
    frame:
        xalign 0.5
        yalign 0.5
        hbox:
            for i in selector.items:
                imagebutton:
                    idle im.Scale(i.avatar, 150, 150)
                    action Function(selector.select, i), Hide('sc_simple_selector')