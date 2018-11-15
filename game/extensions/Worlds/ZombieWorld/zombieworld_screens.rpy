screen sc_zombieworld_event(event):

    window:
        pass


screen sc_zombieworld_location(location):
    $ events = location.events()
    window:
        xfill True
        yfill True
        ysize 720
        xsize 1280

        frame:
            ysize 220
            xsize 1280
            viewport:
                scrollbars 'horizontal'
                draggable True
                mousewheel "horizontal"
                xmaximum 1280
                hbox:
                    spacing 10
                    for event in events:
                        vbox:
                            image im.Scale(event.image(), 120, 145)
                            text event.name()
                            textbutton 'Select':
                                action Function(location.select_event, event)
        frame:
            ypos 221
            ysize 300

            if location.selected_event is not None:
                vbox:
                    image im.Scale(location.selected_event.image(), 180, 250)
                    if not location.selected_event.is_pseudo():
                        textbutton 'Start event':
                            action [Function(ZombieWorldActivateEvent(zombieword_player, location.selected_event).run),
                                Function(location.select_event, None)]

                text location.selected_event.description():
                    xpos 185

        frame:
            ypos 522
            ysize 198
            xsize 1280
            text location.description()
