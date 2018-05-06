style contacts_button:
    color '#10ff10'
    hover_color 'c0ffc0'
    selected_idle_color 'c0ffc0'
    selected_hover_color 'c0ffc0'

init python:

    class ContactsInfo(object):

        def __init__(self, persons):
            self.persons = persons
            self.selected = None

        def show(self):
            return renpy.call_in_new_context('_sc_contacts', info=self)

        def select(self, person):
            self.selected = person

label _sc_contacts(info):
    call screen sc_contacts(info)

screen sc_contacts(info):
    $ persons = info.persons
    window:
        style 'char_info_window'
        frame:
            background '#F0F8FF'
            xalign 0
            yalign 0
            xsize 360
            yfill True
            ysize 720
            frame:
                background im.Scale('gui/contacts_bg.jpg', 350, 720)
                viewport:
                    scrollbars 'vertical'
                    draggable True
                    mousewheel True
                    xmaximum 350
                    
                    vbox:
                        spacing 10
                        for i in persons:
                            hbox:
                                spacing 5
                                xmaximum 350
                                image im.Scale(i.avatar, 32, 32)
                                textbutton i.firstname + " '%s'" % Hierarchy(i).status_str():
                                    action Function(info.select, i)
                                    selected info.selected == i
                                    text_style 'contacts_button'
        frame:
            background '#F0F8FF'
            xpos 365
            frame:
                style 'mer_bg'
                xsize 900
                yfill True
                textbutton "Leave" xalign 1.0 yalign 1.0 action Return()
                if info.selected is not None:
                    $ person = info.selected
                    vbox:
                        xalign 0.5
                        image im.Scale(person.avatar, 200, 200)
                        textbutton person.firstname:
                            xalign 0.5
                            action Function(CharacterInfoScreen(person).show)
                    python:
                        patron = Hierarchy(person).get_patron()

                    if patron is not None:
                        hbox:
                            text 'Patron: '
                            textbutton patron.firstname + " '%s'" % Hierarchy(patron).status_str():
                                action Function(CharacterInfoScreen(patron).show)

