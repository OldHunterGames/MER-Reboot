screen sc_slavercaravan_stats(world):
    
    window:
        background Color((0, 0, 0, 100))
        xfill True
        yfill True
        ysize 720
        xsize 192
        xpos 1168

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
            text 'State: %s' % world.player.state color '#ffffff'
            vbox:
                for value in world.player.show_attributes().values():
                    text value
            
            textbutton 'Slaves (%s)' % len(world.get_slaves()):
                action Function(SlaveManager(world.get_slaves(), world).show)
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
                            background '#f0f0f0'
                            if loc == world.locations.current_location():
                                text_color '#00ff00'
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
        background '#C0FDFB'
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
                    text 'Price: %s' % market.price():
                        xalign 0.5
                    textbutton 'Sell':
                        action Function(market.sell)
        
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
                        textbutton 'Gut into food':
                            action Function(manager.make_food)
                    vbox:
                        text manager.selected.gender
                        text 'escape chance: %s' % manager.escape_chance():
                            color '#ff0000'
                    
        
        textbutton 'Leave':
            xalign 1.0
            yalign 1.0
            action Hide('sc_slavercaravan_slaves')
            

screen sc_slavercaravan_catch_slave(manager=self):
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
                    textbutton 'Gut into food':
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