style slavercaravan_button_text:
    color '#405A0E'
    hover_color '#1b2900'

style slavercaravan_button:
    background Color((27, 41, 0))
    hover_background '#405a0e'

screen sc_slavercaravan_stats(world):

    window:
        background Color((32, 32, 32, 100))
        xfill True
        yfill True
        ysize 720
        xsize 192
        xpos 1188

        vbox:
            spacing 10
            xalign 0.5
            xsize 180
            image im.Scale(world.player.avatar, 180, 180):
                xalign 0.5
            text world.player.name:
                xalign 0.5
                color '#ffffff'

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
                text '%s: %s' % (key.name, value)


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