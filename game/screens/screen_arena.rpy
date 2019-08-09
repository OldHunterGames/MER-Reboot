init python:
    glad_images = {
        'golplynia': 'hoplinie.png',
        'dimacheros': {
            'female': 'dimacher_f.png',
        },
        'pugilist': {
            'female': 'pugilist_f.png'
        },
        'secutor': 'Secutor.png'
    }

    def get_glad_image(person_class, gender):
        data = glad_images.get(person_class.id)

        if isinstance(data, dict):
            return data.get(gender)
        else:
            return data
    
    def get_card_suit_image(suit, power):
        return gui_image('arena/{0}_{1}.png'.format(suit, power))


screen sc_arena(arena):
    python:
        fighter1 = arena.fighter1
        fighter2 = arena.fighter2

    tag info
    modal True
    zorder 10
    window:
        style 'char_info_window'
        background '#777777'
        if arena.state == 'selection':
            # background gui_image('arena/Arena_BG.png')
            # image gui_image('arena/UI_overlay.png')

            hbox:
                yalign 0.05
                spacing 15
                vbox:
                    image im.Scale(fighter1.avatar, 200, 200)
                    vbox:
                        xalign 0.5
                        text fighter1.name color '#fff'
                        text fighter1.person_class.colored_name()
                        textbutton 'make a bet (%s sparks)' % arena.sparks action Function(arena.make_bet, fighter1) xmaximum 200
                hbox:
                    spacing 5
                    for card in fighter1.get_cards('combat'):
                        use fight_card_representation(card, card.suit(fighter1, {}), card.get_power(fighter1, {}), card.name, NullAction())
            
            vbox:
                xalign 0.5
                yalign 0.5
                text 'Next fight preview'
                textbutton 'Next fight' action Return('next'):
                    text_color '#fff'
                    text_hover_color '#00ff00'
                textbutton 'Leave' action Return('leave_arena'):
                    text_color '#fff'
                    text_hover_color '#ffff00'
            hbox:
                xalign 1.0
                yalign 0.95
                spacing 15
                hbox:
                    spacing 5
                    yalign 1.0
                    for card in fighter2.get_cards('combat'):
                        use fight_card_representation(card, card.suit(fighter2, {}), card.get_power(fighter2, {}), card.name, NullAction())

                
                vbox:
                    vbox:
                        xalign 0.5
                        textbutton 'make a bet (%s sparks)' % arena.sparks action Function(arena.make_bet, fighter2) xmaximum 200
                        text fighter2.name color '#fff'
                        text fighter2.person_class.colored_name()
                    image im.Scale(fighter2.avatar, 200, 200)

        if arena.state == 'prefight':
            $ standoff = arena.fight
            $ enemy_card = standoff.enemy_current_card
            $ back = 'images/bg/' + arena.background + '_fight.png' or 'images/arena/Arena_BG.png'

            image back
            vbox:
                xalign 0.5
                yalign 0.5
                if standoff.winner is None:
                    text 'Choose a strategy'
                
                else:
                    if standoff.is_player_win():
                        text 'Player won'
                    else:
                        text 'Player lost'
                    textbutton 'Leave' action Return()

            vbox:
                xalign 0.5
                yalign 0.6
                if standoff.message == 'success':
                    image 'images/special/strike_hit.png'
                    timer 2.0 action Function(standoff.clear_message), If(standoff.winner is not None, Return())
                elif standoff.message == 'fail':
                    image 'images/special/strike_fail.png'
                    timer 2.0 action Function(standoff.clear_message), If(standoff.winner is not None, Return())


            hbox:
                yalign 0.05
                spacing 15
                vbox:
                    image im.Scale(arena.enemy.avatar, 200, 200)
                    vbox:
                        xalign 0.5
                        text arena.enemy.name color '#fff'
                        text arena.enemy.person_class.colored_name()
                if enemy_card is not None:
                    use fight_card_representation(enemy_card, enemy_card.suit(arena.enemy, {}), enemy_card.get_power(arena.enemy, {}), enemy_card.name, NullAction())
            hbox:
                yalign 0.95
                xalign 1.0
                spacing 15
                hbox:
                    yalign 1.0
                    spacing 15
                    if standoff.winner is None:
                        for card in standoff.player_cards:
                            use fight_card_representation(card, card.suit(arena.ally, {}), card.get_power(arena.ally, {}), card.name, [Function(standoff.select_card, card), If(standoff.will_win(card), true=Play('sound', 'sound/cheer.mp3'), false=Play('sound', 'sound/boo.mp3'))])
                vbox:
                    vbox:
                        xalign 0.5
                        text arena.ally.name color '#fff'
                        text arena.ally.person_class.colored_name()
                    image im.Scale(arena.ally.avatar, 200, 200)


        # if arena.state == 'prefight':
        #     $ img = get_glad_image(arena.enemy.person_class, arena.enemy.gender)
        #     $ standoff = arena.fight
        #     $ enemy_card = standoff.enemy_current_card
        #     image gui_image('arena/Arena_BG.png')
        #     if img is not None:
        #         image gui_image('arena/{0}'.format(img)):
        #             xpos 465
        #             ypos 190
        #     image gui_image('arena/UI_overlay.png')
        #    
        #         else:
        #             if standoff.is_player_win():
        #                 text 'Player won'
        #             else:
        #                 text 'Player lost'
        #             textbutton 'Leave' action Return()

        #     vbox:
        #         xalign 0.5
        #         yalign 0.5
        #         if standoff.message == 'success':
        #             text standoff.message color '#00ff00'
        #             timer 1.0 action Function(standoff.clear_message)
        #         elif standoff.message == 'fail':
        #             text standoff.message color '#ff0000'
        #             timer 1.0 action Function(standoff.clear_message)

        #     vbox:
        #         xpos 10
        #         ypos 10
        #         spacing 15
        #         image im.Scale(arena.ally.avatar, 333, 346)
        #         vbox:
        #             xalign 0.5
        #             text arena.ally.name color '#fff'
        #             text arena.ally.person_class.colored_name()                    

        #     vbox:
        #         xpos 935
        #         ypos 10
        #         spacing 15
        #         image im.Scale(arena.enemy.avatar, 333, 346)
        #         vbox:
        #             xalign 0.5
        #             text arena.enemy.name color '#fff'
        #             text arena.enemy.person_class.colored_name()
        #             if enemy_card is not None:
        #                 use fight_card_representation(enemy_card.suit(arena.enemy, {}), enemy_card.get_power(arena.enemy, {}), enemy_card.name, NullAction())

screen fight_card_representation(card, suit, power, name, card_action):
    $ corners = [(0.0, 0), (0.0, 1.0), (1.0, 0), (1.0, 1.0)]
    python:
        if len(name) > 8:
            name_text = ''
            steps = len(name) // 8
            for i in range(steps+1):
                name_text += name[(i)*8:(i+1)*8] + ' '
        else:
            name_text = name
    frame:
        background im.Scale(card.image, 100, 150)
        xsize 100
        ysize 150
        for corner in corners:
            image get_card_suit_image(suit, power):
                xalign corner[0]
                yalign corner[1]
        textbutton name_text:
            text_color value_color(power)
            text_hover_color '#fff'
            action card_action, SensitiveIf(not isinstance(card_action, NullAction))
            xalign 0.5
            yalign 0.5
