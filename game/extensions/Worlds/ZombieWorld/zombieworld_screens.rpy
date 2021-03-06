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
    $ utils = ZombieWorldUtilities
    modal True
    zorder 100
    frame:
        background '#00000000'
        ysize 444
        xsize 700
        xalign 0.5
        yalign 0.5
        image im.Scale(event.select_image(), 260, 444):
            ypos 0

        image utils.event_screen()
        
        frame:
            xpos 340
            xsize 280
            background '#00000000'
            text event.name():
                xalign 0.5
                
        side ("c r"):
            xpos 273
            ypos 79
            area(0, 0, 420, 298)

            viewport id "zombieworld_event_text":
                mousewheel "vertical"
                vbox:
                    xsize 410
                    ysize 280
                    spacing 10
                    if event.fight is None:
                        for i in event.texts():
                            text i
                        for i in event.options():
                            hbox:
                                textbutton i[1]:
                                    action Function(ZombieWorldEventAction(person, event, world, i[0]).run)
                    else:
                        python:
                            combat = event.fight
                            normal_heart = ZombieWorldUtilities.normal_heart_image()
                            black_heart = ZombieWorldUtilities.cursed_heart_image()
                            skull = ZombieWorldUtilities.small_skull_icon()
                            icon = normal_heart if combat.player.vitality > combat.player.filth else black_heart
                            if combat.player.vitality < 1:
                                icon = skull
                            power = combat.player_power()
                            ghouls = combat.ghoul_power
                            ammo_cons = combat.ammo_consumption()
            
                        text 'Ghouls: %s' % ghouls
                            
                        hbox:
                            button:
                                hbox:
                                    text 'Fight (%s, ' % power:
                                        style 'zw_button_text'
                                    image icon
                                    text ')':
                                        style 'zw_button_text'
                                action Function(event.fight.fight)
                            if combat.can_shoot():
                                textbutton 'Shoot the ghoul (%s)' % ammo_cons:
                                    action Function(event.fight.shoot)

            vbar value YScrollValue("zombieworld_event_text"):
                top_gutter 10
                bottom_gutter 10
                base_bar im.Scale(utils.scrollbar(), 10, 298)
                thumb utils.scrollbar_thumb()
        button:

            xpos 260
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

        # button:

        #     xpos 530
        #     yalign 1.0
        #     xsize 157
        #     ysize 57
        #     action Function(ZombieWorldActivateEvent(world.player, event, world).run), Hide('sc_zombieworld_event')
        #     background utils.button_1()
        #     hover_background utils.button_1_hover()
        #     text 'Start':
        #         style 'zw_button_text'
        #         xalign 0.5
        #         yalign 0.5

screen sc_item_icon_frame(bg, img, x_size=50, y_size=50):
    frame:
        xsize x_size
        ysize y_size
        background bg
        image img:
            xalign 0.5
            yalign 0.5

screen sc_resource_count_frame(utils, amount, x_size=97, y_size=27, y_align=0.5):
    frame:
        xsize x_size
        ysize y_size
        yalign y_align
        background utils.resource_text_bg()
        text '%s' % amount:
            xalign 0.5
            yalign 0.5
        transclude
screen sc_zombieworld_location(world):
    $ x_size = 1280
    $ location = world.current_location
    $ events = world.current_location.events()
    $ utils = ZombieWorldUtilities
    $ player = world.player

    window:
        yfill True
        ysize 720
        xsize x_size
        xalign 0.0
        background location.image()
        image utils.main_screen()

        frame:
            background utils.main_screen_turns_counter()
            text 'Days: %s' % world.turn:
                xpos 12
                ypos 5

        frame:
            background utils.main_screen_left_block()
            xpos 15
            ypos 445
            xsize 190
            image utils.equip_icon_bg():
                xpos 12
                ypos 10

            image utils.equip_icon_bg():
                xpos 95
                ypos 10

            image utils.equip_icon_bg():
                xalign 0.5
                ypos 90
            hbox:
                ypos 182
                xpos 8
                for i in range(1, player.vitality + 1):
                    if i <= player.filth:
                        image utils.cursed_heart_image()
                    else:
                        image utils.normal_heart_image()

        viewport:
            scrollbars 'horizontal'
            draggable True
            mousewheel "horizontal"
            ypos 150
            xmaximum 825
            xpos 190
            hbox:
                spacing 10
                for event in events:
                    frame:
                        background '#00000000'
                        image event.card_image():
                            xalign 0.5
                            yalign 0.5
                        xsize 190
                        ysize 260
                        imagebutton:
                            xalign 0.5
                            yalign 0.5
                            idle utils.event_card_border()
                            hover utils.event_card_border_hover()
                            hovered SetField(location, 'selected_event', event)
                            unhovered SetField(location, 'selected_event', None)
                            action Function(ZombieWorldShowEvent(world.player, event, world).run)

        if location.venchile is not None:
            image location.venchile.image():
                xpos 1085
                ypos 295
        frame:
            xpos 1065
            ypos 445
            background utils.main_screen_right_block()
            vbox:
                xpos 6
                ypos 6
                spacing 2
                hbox:
                    use sc_item_icon_frame(utils.resource_bg(), utils.food_icon())
                    use sc_resource_count_frame(utils, player.food)
                hbox:
                    use sc_item_icon_frame(utils.resource_bg(), utils.drugs_icon())
                    use sc_resource_count_frame(utils, player.drugs)
                hbox:
                    use sc_item_icon_frame(utils.resource_bg(), utils.ammo_icon())
                    use sc_resource_count_frame(utils, player.ammo)
                hbox:
                    use sc_item_icon_frame(utils.resource_bg(), utils.fuel_icon())
                    use sc_resource_count_frame(utils, player.fuel)

        frame:
            ypos 450
            xmaximum 825
            xpos 190
            background utils.main_screen_text_bg()
            if location.selected_event is not None:
                text location.selected_event.description():
                    ypos 20
                    xpos 25
                    color '#000000'
            else:
                text location.description():
                    ypos 20
                    xpos 25
                    color '#000000'
                
                
            
