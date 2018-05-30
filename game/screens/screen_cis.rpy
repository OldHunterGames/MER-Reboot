
style char_info_window is window:
    background '#C0FDFB'
    color '#1C1E15'
    xfill True
    yfill True
    xsize 1280
    ysize 720

style mer_bg:
    background '#C0FDFB'

style mer_text:
    color '#1C1E15'
    hover_color '#001E05'

style mer_border:
    background '#64B6AC'

label lbl_cis_glue(info, controlled=False, relations=None):
    call screen sc_cis(info, controlled, relations)
    return

init python:
    class CharacterInfoScreen(object):

        def __init__(self, person, controlled=False):
            self.person = person
            self.controlled = controlled

        def show(self):
            return renpy.show_screen('sc_cis', self)

screen sc_cis(info, relations=None):
    $ person = info.person
    $ controlled = info.controlled
    python:
        if person == player:
            controlled = True
    modal True
    zorder 10
    tag info
    window:
        style 'char_info_window'
        vbox:
            image im.Scale(person.avatar, 200, 200)
            text person.firstname:
                xalign 0.5
            text 'Sparks: %s' % person.sparks:
                xalign 0.5
            text 'Income: %s' % core.calc_income(person):
                xalign 0.5
            if Hierarchy(person).get_patron() is not None:
                textbutton 'Patron: %s' % Hierarchy(person).get_patron().firstname:
                    action Function(CharacterInfoScreen(Hierarchy(person).get_patron()).show)
            if len(Hierarchy(person).get_clientelas()) > 0:
                textbutton 'Clientelas':
                    action Function(ContactsInfo(Hierarchy(person).get_clientelas()).show)
            if person.heir() is not None:
                textbutton 'Heir: %s' % person.heir().firstname:
                    action Function(ContactsInfo(person.successors()).show)
            if not controlled:
                if not person.is_successor(player) and not player.is_successor(person):
                    textbutton 'Challenge' action Function(SuccessorChallenge(person, player).run)
            if controlled:
                textbutton 'Ensembles':
                    action Function(EnsembleMaker(person).show)
            textbutton "Leave" action Hide('sc_cis')
        vbox:
            xpos 205
            text 'Angels'
            viewport:
                scrollbars 'vertical'
                draggable True
                mousewheel True
                xsize 200
                ysize 200
                vbox:
                    for i in reversed(sorted(person.get_host(), key=lambda x: x.level())):
                        textbutton i.name:
                            text_color value_color(i.level())
                            text_hover_color '#EFF0D1'
                            action Function(AngelInfoScreen(i).show)
        vbox:
            xpos 410
            text 'Sonm'
            viewport:
                scrollbars 'vertical'
                draggable True
                mousewheel True
                xsize 200
                ysize 200
                vbox:
                    for i in reversed(sorted(Hierarchy(person).assembly(exclude_self=True), key=lambda x: x.level())):
                        textbutton i.name:
                            text_color value_color(i.level())
                            text_hover_color '#EFF0D1'
                            action Function(AngelInfoScreen(i).show)
                    
