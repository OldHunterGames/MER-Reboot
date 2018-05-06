init python:
    
    class EnsembleMaker(object):

        def __init__(self, owner, kanonarch=None):
            self._picked = list()
            self.kanonarch = kanonarch
            self.owner = owner

        @property
        def permanent(self):
            if self.kanonarch is None:
                return list()
            else:
                return self.kanonarch.ensemble

        @property
        def picked(self):
            return self._picked + self.permanent

        @property
        def angels(self):
            return [i for i in self.owner.get_host() if i.kanonarch is None and angel.level() < 4] + self.permanent

        def select(self, angel):
            self._picked.append(angel)

        def unselect(self, angel):
            self._picked.remove(angel)

        def available(self):
            if len(self.picked) < 1:
                return self.angels
            else:
                return [i for i in self.angels if i.grade == self.picked[0].grade]

        def show(self):
            return renpy.show_screen('sc_make_ensemble', self)

        def make(self):
            self.owner.sparks -= self.cost()
            if self.kanonarch is not None:
                ExtendEnsemble(self.kanonarch, self._picked).run()
            else:
                CreateAngelEnsemble(AngelMaker, self.owner, *self.picked).run()
            self._picked = list()
            

        def cost(self):
            if len(self._picked) < 1:
                return 0
            else:
                cost = 0
                for i in range(len(self.permanent), len(self.picked)):
                    cost += ensemble_costs[i]
                return cost * ensemble_multipliers[self._picked[0].level()]


screen sc_make_ensemble(maker):
    modal True
    zorder 10
    tag info
    window:
        vbox:
            if len(maker.picked) < 8:
                textbutton 'Make(%s sparks)' % maker.cost():
                    if maker.owner.sparks < maker.cost():
                        text_color '#ff0000'
                    sensitive (len(maker.picked) > 1 and maker.owner.sparks >= maker.cost())
                    action Function(maker.make)
            else:
                text 'Maximum ensemble size'
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
                        action If(i in maker.permanent, NullAction(), If(i in maker.picked, Function(maker.unselect, i), Function(maker.select, i)))
                        selected i in maker.picked
                        text_selected_idle_color '#000000'
                        text_selected_hover_color '#ffffff'