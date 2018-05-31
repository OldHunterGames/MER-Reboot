label lbl_ais_glue(info):
    call screen sc_ais(info)
    return

init python:
    class AngelInfoScreen(object):

        def __init__(self, angel, show_world_btn=False):
            self.angel = angel
            self.show_world_btn = show_world_btn

        def show(self):
            return renpy.show_screen('sc_ais', self)

screen sc_ais(info):
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
            text 'Income: %s' % angel.produce_sparks()
            if angel.world is not None and player in angel.get_witnesses(Hierarchy) and info.show_world_btn:
                textbutton 'Visit world':
                    action Function(MistTravel(angel.world, player, core).run)
            if angel.can_be_apostol(player) and angel.level() > 2:
                textbutton 'Become apostol(%s sparks)' % angel.apostol_cost():
                    action Function(SetAngelApostol(angel, player).run)
                    sensitive (player.sparks >= angel.apostol_cost())
            textbutton "Leave" action Hide('sc_ais')

        vbox:
            xalign 0.5
            if angel.level() > 2 and len(angel.ensemble) > 0:
                text 'Ensemble'
                for i in angel.ensemble:
                    textbutton i.name:
                        text_color value_color(i.level())
                        text_hover_color '#EFF0D1'
                        action Function(AngelInfoScreen(i, show_world_btn=True).show)
                if angel.apostol == player:
                    textbutton 'Extend ensemble':
                        action Function(EnsembleMaker(angel.apostol, angel).show)
        if apostol is not None:
            vbox:
                xalign 1.0
                imagebutton:
                    idle im.Scale(apostol.avatar, 200, 200)
                    action Function(CharacterInfoScreen(apostol).show)
                text apostol.firstname
