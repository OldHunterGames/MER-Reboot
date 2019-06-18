screen sc_select_fighter(selector):
    python:
        fighter1 = selector.current_fighter()
        fighter2 = selector.enemy
        entertainment = PriceCalculator(fighter2).entertainment_raiting_formula()
        evaluation = 'Опасный противник' if entertainment > PriceCalculator(fighter1).training_price() else 'Скучный противник'
    tag info
    modal True
    zorder 10
    window:
        background '#777777'
        image selector.arena_maker.selection_bg
        # image gui_image('arena/UI_overlay.png')
        style 'char_info_window'
        vbox:
            xalign 0.5
            yalign 0.5
            textbutton 'Отказаться от боя' action Function(selector.escape), Return()
            if len(selector.fighters) > 1:
                textbutton "Сменить бойца" action Function(selector.next)
            textbutton selector.start_text action Return()

        hbox:
            spacing 15
            yalign 0.05
            vbox:
                image im.Scale(fighter2.avatar, 200, 200)
                text fighter2.name xalign 0.5 color '#ffffff'
                text fighter2.person_class.colored_name() xalign 0.5
                text evaluation
                if selector.arena_maker.can_skip_enemy:
                    textbutton 'Skip this enemy' action Function(selector.arena_maker.set_gladiator)
            hbox:
                spacing 5
                for card in fighter2.get_cards('combat', special_filter=selector.arena_maker.cards_filter):
                    use fight_card_representation(card.suit(fighter2, {}), card.get_power(fighter2, {}), card.name, NullAction())

        hbox:
            spacing 15
            xalign 1.0
            yalign 0.95
            hbox:
                spacing 5
                yalign 1.0
                for card in fighter1.get_cards('combat', special_filter=selector.arena_maker.cards_filter):
                    use fight_card_representation(card.suit(fighter1, {}), card.get_power(fighter1, {}), card.name, NullAction())
            vbox:
                
                text fighter1.name xalign 0.5 color '#ffffff'
                text fighter1.person_class.colored_name() xalign 0.5
                image im.Scale(fighter1.avatar, 200, 200)
            

            
        

        if fighter1 == selector.player:
                text "You gonna fight personaly. If you lose it's a game over. Are you shure?":
                    color '#ff0000'
                    xalign 0.5
                    yalign 0.5
                    xmaximum 500
