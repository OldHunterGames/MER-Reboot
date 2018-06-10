init python:

    class SexDeckInfo(object):

        PAGE_CARDS = 5

        def __init__(self, deck):
            self.deck = deck
            self.page = 0

        def get_page(self):
            return sorted(
                self.deck.get_cards(),
                key=lambda card: card.id
            )[self.page*self.PAGE_CARDS:(self.page+1)*self.PAGE_CARDS]

        def hand(self):
            return self.deck.get_hand()

        def free_slots(self):
            return self.deck.max_hand_length() - len(self.hand())

        def show(self):
            return renpy.show_screen('sc_sex_deck', info=self)

        def has_next_page(self):
            return (self.page + 1) * self.PAGE_CARDS < len(self.deck.get_cards())

        def has_prev_page(self):
            return self.page > 0


screen sc_sex_deck(info):

    modal True
    zorder 10
    window:
        style 'char_info_window'

        frame:
            xalign 0.5
            yalign 0.0
            ysize 300
            xsize 1080
            hbox:
                spacing 10
                xalign 0.5
                for i in info.get_page():
                    frame:
                        xsize 200
                        ysize 250
                        vbox:
                            text i.id
                            text i.type()
                            text i.activity()
            textbutton 'Previous':
                xalign 0.0
                yalign 1.0
                action SetField(info, 'page', info.page -1)
                sensitive (info.has_prev_page())

            textbutton 'Next':
                xalign 1.0
                yalign 1.0
                action SetField(info, 'page', info.page +1)
                sensitive (info.has_next_page())

        frame:
            xalign 0.5
            ypos 305
            ysize 300
            xsize 1080
            hbox:
                spacing 10
                xalign 0.5
                for i in info.deck.get_hand():
                    frame:
                        xsize 200
                        ysize 250
                        vbox:
                            text i.id
                            text i.type()
                            text i.activity()
                for i in range(info.free_slots()):
                    image im.Scale(card_back(), 200, 250)

        textbutton "Leave":
            action Hide('sc_sex_deck')
