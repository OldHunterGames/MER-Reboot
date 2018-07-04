style slavercaravan_button_text:
    color '#405A0E'
    hover_color '#1b2900'

style slavercaravan_button:
    background Color((27, 41, 0))
    hover_background '#405a0e'

screen sc_slavercaravan_stats(world):

    window:
        background im.Scale(world.path('resources/img/gui/main_screen.png'), 1280, 720)
        xfill True
        yfill True
        ysize 720
        xsize 1280

        vbox:
            xpos 1084
            ypos 8
            spacing 10
            xsize 180
            image im.Scale(world.player.avatar, 188, 170):
                xalign 0.5

            text 'Food: %s' % world.food color '#ffffff'
            text 'Day: %s' % world.day color '#ffffff'
            text 'State: %s' % world.player.state color value_color(world.player.state)
            vbox:
                for value in world.player.show_attributes().values():
                    text value

            textbutton 'Slaves (%s)' % len(world.get_slaves()):
                action Function(SlaveManager(world.get_slaves(), world).show)
                text_style 'slavercaravan_button_text'
                style 'slavercaravan_button'

            for key, value in world.player.items(as_dict=True).items():
                text '%s: %s' % (key.name, value) color '#ffffff'


screen sc_slavercaravan_map(world):
    $ locations = world.locations.locations
    python:
        width= world.locations._width
        height = world.locations._height
        available = world.locations.can_go(world.locations.current)[1]
    modal True
    window:
        xfill True
        yfill True
        ysize 720
        xsize 1280
        background '#000000'
        vbox:
            xalign 0.5
            yalign 0.2
            spacing 5
            for i in range(0, height):
                hbox:
                    spacing 5
                    for j in range(i*width, i*width+width):
                        $ loc = locations[j]

                        textbutton loc.name():
                            xsize 200
                            ysize 35
                            background im.Scale(loc.image, 200, 35)
                            if loc == world.locations.current_location():
                                text_color '#00ff00'
                            else:
                                text_color '#ffffff'
                            text_hover_color '#aa70ff'
                            action  Function(world.change_location, j), Return(),
                            sensitive (j in available and loc != world.locations.current_location())

        textbutton 'Leave':
            action Return()


screen sc_slavercaravan_compas(world):
    python:
        available_locations = world.locations.locs_to_go()
    window:
        xfill True
        yfill True
        ysize 720
        xsize 1280
        background '#00000000'        
        imagebutton:
            xcenter 638
            ycenter 320
            focus_mask True
            idle im.Scale(world.path('resources/img/map/btn_cross_e.png'), 200, 200)
            hover im.Scale(world.path('resources/img/map/btn_cross_e_hover.png'), 200, 200)
            insensitive im.Scale(world.path('resources/img/map/btn_cross_e_inactive.png'), 200, 200)
            action Return(available_locations['left'])
            sensitive (available_locations['left'] is not None)
        imagebutton:
            xcenter 460
            ycenter 320
            focus_mask True
            idle im.Scale(world.path('resources/img/map/btn_cross_w.png'), 200, 200)
            hover im.Scale(world.path('resources/img/map/btn_cross_w_hover.png'), 200, 200)
            insensitive im.Scale(world.path('resources/img/map/btn_cross_w_inactive.png'), 200, 200)
            action Return(available_locations['right'])
            sensitive (available_locations['right'] is not None)
        imagebutton:
            xcenter 550
            ycenter 236
            focus_mask True
            idle im.Scale(world.path('resources/img/map/btn_cross_n.png'), 200, 200)
            hover im.Scale(world.path('resources/img/map/btn_cross_n_hover.png'), 200, 200)
            insensitive im.Scale(world.path('resources/img/map/btn_cross_n_inactive.png'), 200, 200)
            action Return(available_locations['top'])
            sensitive (available_locations['top'] is not None)
        imagebutton:
            xcenter 551
            ycenter 405
            focus_mask True
            idle im.Scale(world.path('resources/img/map/btn_cross_s.png'), 200, 200)
            hover im.Scale(world.path('resources/img/map/btn_cross_s_hover.png'), 200, 200)
            insensitive im.Scale(world.path('resources/img/map/btn_cross_s_inactive.png'), 200, 200)
            action Return(available_locations['bot'])
            sensitive (available_locations['bot'] is not None)

        imagebutton:
            xcenter 550
            ycenter 320
            focus_mask True
            idle im.Scale(world.path('resources/img/map/btn_cross_center.png'), 70, 70)
            hover im.Scale(world.path('resources/img/map/btn_cross_center_hover.png'), 70, 70)
            action Return('stay')


screen sc_slavercaravan_sell_slaves(market):
    modal True
    zorder 10
    window:
        xfill True
        yfill True
        ysize 720
        xsize 1280
        background world.path('bg/action_sell_slave.png')
        vbox:
            for i in market.slaves:
                hbox:
                    spacing 5
                    xmaximum 350
                    image im.Scale(i.avatar, 32, 32)
                    textbutton i.name:
                        action Function(market.select, i)
                        selected market.selected == i

        if market.selected is not None:
            frame:
                xalign 0.5
                xsize 500
                ysize 720
                vbox:
                    image im.Scale(market.selected.avatar, 200, 200)
                    text market.selected.name:
                        xalign 0.5
                    vbox:
                        xalign 0.5
                        for value in market.selected.show_attributes().values():
                            text value
                        for value in market.selected.statuses():
                            text value
                    text 'Price: %s' % market.price():
                        xalign 0.5
                    textbutton 'Sell':
                        action Function(market.sell), If(len(market.slaves) < 1, Hide('sc_slavercaravan_sell_slaves'))

        textbutton 'Leave':
            xalign 1.0
            yalign 1.0
            action Hide('sc_slavercaravan_sell_slaves')


screen sc_slavercaravan_slaves(manager):
    modal True
    zorder 10
    window:
        xfill True
        yfill True
        ysize 720
        xsize 1280
        background '#C0FDFB'
        vbox:
            for i in manager.slaves:
                hbox:
                    spacing 5
                    xmaximum 350
                    image im.Scale(i.avatar, 32, 32)
                    textbutton i.name:
                        action Function(manager.select, i)
                        selected manager.selected == i

        if manager.selected is not None:
            frame:
                xalign 0.5
                xsize 500
                ysize 720
                hbox:
                    spacing 5
                    vbox:
                        image im.Scale(manager.selected.avatar, 200, 200)
                        text manager.selected.name:
                            xalign 0.5
                        vbox:
                            xalign 0.5
                            for value in manager.selected.show_attributes().values():
                                text value
                            for value in manager.selected.statuses():
                                text value
                        if manager.can_make_food():
                            textbutton 'Butcher for food':
                                action Function(manager.make_food)
                        if manager.can_rape():
                            textbutton 'Rape':
                                action Function(manager.rape)
                        if manager.can_tame():
                            textbutton 'Tame':
                                action Function(manager.tame)
                    vbox:
                        text manager.selected.gender
                        text 'escape chance: %s' % manager.escape_chance():
                            color '#ff0000'


        textbutton 'Leave':
            xalign 1.0
            yalign 1.0
            action Hide('sc_slavercaravan_slaves')


screen sc_slavercaravan_catch_slave(manager):
    modal True
    zorder 10
    window:
        xfill True
        yfill True
        ysize 720
        xsize 1280
        background '#C0FDFB'
        frame:
            xalign 0.5
            xsize 500
            ysize 720
            hbox:
                spacing 5
                vbox:
                    image im.Scale(manager.slave.avatar, 200, 200)
                    textbutton 'Butcher for food':
                        action Function(manager.make_food), Return()
                    for i in manager.items:
                        textbutton i.name:
                            action Function(manager.catch, i), Return()
                    if manager.tries > 1:
                        textbutton 'Try again':
                            action Return()
                    else:
                        textbutton 'End for today':
                            action Return()
                vbox:
                    text slave.gender
                    for value in manager.slave.show_attributes().values():
                        text value


screen sc_slavercaravan_pick_slave(manager):
    modal True
    zorder 10
    window:
        xfill True
        yfill True
        ysize 720
        xsize 1280
        background '#C0FDFB'
        vbox:
            for i in manager.slaves:
                hbox:
                    spacing 5
                    xmaximum 350
                    image im.Scale(i.avatar, 32, 32)
                    textbutton i.name:
                        action Function(manager.select, i)
                        selected manager.selected == i

        if manager.selected is not None:
            frame:
                xalign 0.5
                xsize 500
                ysize 720
                hbox:
                    spacing 5
                    vbox:
                        image im.Scale(manager.selected.avatar, 200, 200)
                        text manager.selected.name:
                            xalign 0.5
                        text manager.selected.gender:
                            xalign 0.5
                        vbox:
                            xalign 0.5
                            for value in manager.selected.show_attributes().values():
                                text value
                            for value in manager.selected.statuses():
                                text value
                        textbutton 'Pick':
                            action Function(manager.pick), Return()