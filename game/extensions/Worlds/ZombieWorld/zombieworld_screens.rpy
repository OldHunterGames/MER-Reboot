screen sc_zombieworld_event(event):

    window:
        pass


screen sc_zombieworld_player_info(player, world):
    frame:
        xpos 1060
        xsize 220
        yfill True
        vbox:
            xalign 0.5
            image im.Scale(player.avatar, 200, 200)
            text 'Turns: %s' % world.turn
            text 'Vitality: {}%'.format(player.vitality)
            textbutton 'Sleep' action Function(world.skip_turn)
                

screen sc_zombieworld_location(world):
    $ x_size = 1059
    $ location = world.current_location
    $ events = world.current_location.events()
    use sc_zombieworld_player_info(world.player, world)
    window:
        yfill True
        ysize 720
        xsize x_size
        xalign 0.0
        
        frame:
            ysize 220
            xsize x_size
            viewport:
                scrollbars 'horizontal'
                draggable True
                mousewheel "horizontal"
                xmaximum x_size
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
            xmaximum x_size
            if location.selected_event is not None:
                vbox:
                    image im.Scale(location.selected_event.image(), 180, 250)
                    if not location.selected_event.is_pseudo():
                        textbutton 'Start event':
                            action [Function(ZombieWorldActivateEvent(world.player, location.selected_event, world).run),
                                Function(location.select_event, None)]

                text location.selected_event.description():
                    xpos 185
                    xmaximum x_size-185

        frame:
            ypos 522
            ysize 198
            xsize x_size
            text location.description()
