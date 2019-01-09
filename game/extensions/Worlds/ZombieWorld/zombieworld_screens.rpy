style mer_window:
    background '#FFFFFF'
    color '#1C1E15'
    xfill True
    yfill True

# window:
#                 style 'mer_window'
#                 ysize 220
#                 xsize x_size
#                 background Frame(
#                     im.MatrixColor(
#                         location.image(), 
#                         im.matrix.brightness(0.1) 
#                         * im.matrix.opacity(0.8)),
#                     30, 
#                     30
#                 )


screen sc_zombieworld_player_info(player, world):
    $ utils = ZombieWorldUtilities(world)
    $ zombie_level = min(3, player.zombification)
    frame:
        xpos 1060
        xsize 220
        yfill True
        vbox:
            xalign 0.5
            image im.Scale(player.avatar, 200, 200)
            text 'Turns: %s' % world.turn
            hbox:
                for i in range(1, player.vitality + 1):
                    if i <= player.filth:
                        image im.Scale(utils.cursed_heart_image(), 25, 25)
                    else:
                        image im.Scale(utils.normal_heart_image(), 25, 25)
            text zombification_data[zombie_level]
            textbutton 'Sleep' action Function(world.skip_turn)
            textbutton 'Add filth' action SetField(player, 'filth', player.filth + 1)
            textbutton 'Add zombification' action SetField(player, 'zombification', player.zombification + 1)
                

screen sc_zombieworld_location(world):
    $ x_size = 1060
    $ location = world.current_location
    $ events = world.current_location.events()
    use sc_zombieworld_player_info(world.player, world)
    window:
        yfill True
        ysize 720
        xsize x_size
        xalign 0.0
        if location.image() is not None:
            image im.Scale(location.image(), x_size, 500):
                ypos 220
        image Solid('ffffff30')
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
                            image im.Scale(event.list_image(), 120, 145)
                            text event.name()
                            textbutton 'Select':
                                action Function(location.select_event, event)
        frame:
            ypos 220
            ysize 300
            xmaximum x_size
            background '#00000000'
            if location.selected_event is not None:
                vbox:
                    image im.Scale(location.selected_event.select_image(), 180, 250)
                    if not location.selected_event.is_pseudo():
                        textbutton 'Start event':
                            action [Function(ZombieWorldActivateEvent(world.player, location.selected_event, world).run),
                                Function(location.select_event, None)]

                text location.selected_event.description():
                    xpos 185
                    xmaximum x_size-185
                    color '#000000'

        frame:
            background '#00000000'
            ypos 522
            ysize 198
            xsize x_size
            text location.description() color 'ffffffc0'
                
            
