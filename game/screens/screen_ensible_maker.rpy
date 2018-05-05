init python:
    
    class EnsembleMaker(object):

        def __init__(self, owner):
            self.picked = list()
            self.owner = owner

        @property
        def angels(self):
            return [i for i in self.owner.get_host() if i.kanonarch is None and angel.level() < 4]

        def select(self, angel):
            self.picked.append(angel)

        def unselect(self, angel):
            self.picked.remove(angel)

        def available(self):
            if len(self.picked) < 1:
                return self.angels
            else:
                return [i for i in self.angels if i.grade == self.picked[0].grade]

        def show(self):
            return renpy.show_screen('sc_make_ensemble', self)

        def make(self):
            CreateAngelEnsemble(AngelMaker, self.owner, *self.picked).run()
            self.picked = list()


screen sc_make_ensemble(maker):
    modal True
    zorder 10
    tag info
    window:
        vbox:
            textbutton 'Make':
                sensitive len(maker.picked) > 1
                action Function(maker.make)
            textbutton 'Leave':
                action Hide('sc_make_ensemble')
        style 'char_info_window'
        viewport:
            scrollbars 'vertical'
            draggable True
            mousewheel True
            xsize 200
            ysize 200
            xalign 0.5
            vbox:
                for i in maker.available():
                    textbutton i.name:
                        text_color value_color(i.level())
                        text_hover_color '#000000'
                        action If(i in maker.picked, Function(maker.unselect, i), Function(maker.select, i))
                        selected i in maker.picked
                        text_selected_idle_color '#000000'
                        text_selected_hover_color '#ffffff'