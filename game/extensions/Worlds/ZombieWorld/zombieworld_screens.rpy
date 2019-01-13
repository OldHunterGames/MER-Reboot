style mer_window:
    background '#FFFFFF'
    color '#1C1E15'
    xfill True
    yfill True

style zw_button_text:
    drop_shadow (1, 1)
    drop_shadow_color '#000'
    color "#FFF" 
    hover_color "#F00" 
    insensitive_color "#999"


screen sc_zombieworld_event(event, person, world):
    $ context = object()
    $ context.player = person
    $ utils = ZombieWorldUtilities(world)
    modal True
    zorder 100
    frame:
        ysize 444
        xsize 700
        xalign 0.5
        yalign 0.5
        background utils.event_screen()
        image im.Scale(event.select_image(), 260, 444):
            yalign 0.5
        side ("c r"):
            xpos 265
            ypos 75
            area(0, 0, 430, 280)

            viewport id "zombieworld_event_text":
                mousewheel "vertical"
                vbox:
                    xsize 430
                    ysize 280
                    spacing 10
                    text event.description()
            vbar value YScrollValue("zombieworld_event_text"):
                top_gutter 10
                bottom_gutter 10
                base_bar im.Scale(utils.scrollbar(), 10, 280)
                thumb utils.scrollbar_thumb()
        button:

            xpos 255
            yalign 1.0
            xsize 157
            ysize 57
            action Hide('sc_zombieworld_event')
            background utils.button_1()
            hover_background utils.button_1_hover()
            text 'Leave':
                style 'zw_button_text'
                xalign 0.5
                yalign 0.5
            # button 'Start' action NullAction():
            #     xalign 1.0

        button:

            xpos 530
            yalign 1.0
            xsize 157
            ysize 57
            action Function(ZombieWorldActivateEvent(world.player, event, world).run), Hide('sc_zombieworld_event')
            background utils.button_1()
            hover_background utils.button_1_hover()
            text 'Start':
                style 'zw_button_text'
                xalign 0.5
                yalign 0.5
            # button 'Start' action NullAction():
            #     xalign 1.0

screen sc_zombieworld_location(world):
    $ x_size = 1280
    $ location = world.current_location
    $ events = world.current_location.events()
    $ utils = ZombieWorldUtilities(world)
    $ player = world.player

    window:
        yfill True
        ysize 720
        xsize x_size
        xalign 0.0
        background location.image()
        image utils.main_screen()

        hbox:
            xpos 25
            ypos 640
            for i in range(1, player.vitality + 1):
                if i <= player.filth:
                    image utils.cursed_heart_image()
                else:
                    image utils.normal_heart_image()

        viewport:
            scrollbars 'horizontal'
            draggable True
            mousewheel "horizontal"
            xmaximum x_size
            ypos 200
            hbox:
                spacing 10
                for event in events:
                    vbox:
                        imagebutton:
                            idle im.Scale(event.list_image(), 120, 145)
                            action Function(ZombieWorldShowEvent(world.player, event, world).run)
                        text event.name()                            

        vbox:
            xpos 1070
            ypos 460
            hbox:
                image utils.food_icon()
                text ': %s' % player.food
            hbox:
                image utils.drugs_icon()
                text ': %s' % player.drugs
            hbox:
                image utils.ammo_icon()
                text ': %s' % player.ammo
            hbox:
                image utils.fuel_icon()
                text ': %s' % player.fuel
        text location.description():
            color '#000000'
            ypos 480
            xmaximum 820
            xpos 220
                
            
