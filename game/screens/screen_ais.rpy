label lbl_ais_glue(info):
    call screen sc_ais(info)
    return

init python:
    class AngelInfoScreen(object):

        def __init__(self, angel):
            self.angel = angel

        def show(self):
            return renpy.show_screen('sc_ais', self)

screen sc_ais(info, controlled=False, relations=None):
    $ angel = info.angel
    $ apostol = angel.apostol
    tag info
    modal True
    zorder 10
    window:
        style 'char_info_window'
        vbox:
            image angel.avatar
            text angel.name
            if angel.world is not None and player in angel.get_witnesses(Hierarchy):
                textbutton 'Visit world':
                    action Function(angel.world.visit, player)
            if angel.can_be_apostol(player) and angel.level() > 2:
                textbutton 'Become apostol':
                    action Function(SetAngelApostol(angel, player).run)
            textbutton "Leave" action Hide('sc_ais')
        if apostol is not None:
            vbox:
                xalign 1.0
                image apostol.avatar
                text apostol.firstname