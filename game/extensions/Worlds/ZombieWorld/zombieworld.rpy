init python:
    sys.path.append(renpy.loader.transfn("extensions/Worlds/ZombieWorld"))

init 1 python:
    from zombieworld import *

    class ZombieWorld(World):
        DAYS_TO_SURVIVE = 30
        _VISITS = 0

        def __init__(self, *args, **kwargs):
            super(ZombieWorld, self).__init__(*args, **kwargs)
            self.current_location = None
            self.turn = 1
            self.locations = dict()

        def set_location(self, location):
            self.current_location = location

        def add_available_location(self, id, location):
            self.locations[id] = location

        def get_available_location(self, id):
            return self.locations.get(id)

        def sleep(self):
            result = renpy.call_in_new_context('lbl_zombieword_sleep', world=self)
            if result:
                self.skip_turn()

        @Observable
        def skip_turn(self):
            self.turn += 1

        def entry_label(self):
            if ZombieWorld._VISITS > 1:
                return 'lbl_zombieworld'
            else:
                return 'lbl_zombieworld_tutorial'

        @classmethod
        def get_path(cls):
            return 'ZombieWorld/'

        def on_visit(self, person):
            ZombieWorld._VISITS += 1
            if getattr(ZombieWorld, 'PLAYER', None) is None:
                self.player = ZombieWorldPersonMaker.make_person(person)
                ZombieWorld.PLAYER = self.player
                self.player.add_eventlistener('vitality_changed', self.vitality_change_callback)
            else:
                self.player = ZombieWorld.PLAYER

        def vitality_change_callback(self, vitality):
            if vitality <= 0:
                renpy.call_in_new_context('lbl_zombieworld_loose', world=self, person=person)

    class ZombieWorldUtilities(object):
        _world = ZombieWorld

        @classmethod
        def normal_heart_image(self):
            return self._world.path('resources/icons/heart_normal_intext.png')

        @classmethod
        def cursed_heart_image(self):
            return self._world.path('resources/icons/heart_cursed_intext.png')

        @classmethod
        def food_icon(self):
            return self._world.path('resources/icons/food_icon.png')

        @classmethod
        def drugs_icon(self):
            return self._world.path('resources/icons/drugs_icon.png')

        @classmethod
        def fuel_icon(self):
            return self._world.path('resources/icons/fuel_icon.png')

        @classmethod
        def ammo_icon(self):
            return self._world.path('resources/icons/ammo_icon.png')

        @classmethod
        def small_skull_icon(self):
            return self._world.path('resources/icons/death-skull_small.png')

        @classmethod
        def scrollbar_top(self):
            return self._world.path('resources/interface/sliders/slider_arrow_top.png')

        @classmethod
        def scrollbar_bottom(self):
            return self._world.path('resources/interface/sliders/slider_arrow_bottom.png')

        @classmethod
        def scrollbar(self):
            return self._world.path('resources/interface/sliders/slider_bg_v_merged.png')

        @classmethod
        def scrollbar_thumb(self):
            return self._world.path('resources/interface/sliders/slider_slider_v.png')

        @classmethod
        def main_screen(self):
            return self._world.path('resources/interface/interface_base.png')

        @classmethod
        def main_screen_text_bg(self):
            return self._world.path('resources/interface/text_field.png')

        @classmethod
        def main_screen_right_block(self):
            return self._world.path('resources/interface/resources_window.png')

        @classmethod
        def main_screen_left_block(self):
            return self._world.path('resources/interface/character_window.png')

        @classmethod
        def main_screen_turns_counter(self):
            return self._world.path('resources/interface/turns_counter.png')

        @classmethod
        def event_screen(self):
            return self._world.path('resources/interface/Eventscreen_1.png')

        @classmethod
        def button_1(self):
            return self._world.path('resources/interface/buttons/button_1.png')

        @classmethod
        def button_1_hover(self):
            return self._world.path('resources/interface/buttons/button_1_hover.png')

        @classmethod
        def equip_icon_bg(self):
            return self._world.path('resources/icons/equip_icon_background.png')

        @classmethod
        def resource_bg(self):
            return self._world.path('resources/icons/resource_icon_background.png')

        @classmethod
        def resource_text_bg(self):
            return self._world.path('resources/icons/resource_counter_background.png')

        @classmethod
        def event_card_border(self):
            return self._world.path('resources/events/event_card_border.png')

        @classmethod
        def event_card_border_hover(self):
            return self._world.path('resources/events/event_card_border_hover.png')

        @classmethod
        def event_empty_image(self):
            return self._world.path('resources/events/event_empty.png')

        @classmethod
        def card_empty_image(self):
            return self._world.path('resources/events/card_empty.png')


label lbl_zombieworld(world):
    'Zombieworld'
    return


label lbl_zombieworld_loose(world, person):
    'You lost all your vitality. GG'
    $ renpy.quit()
    return

label lbl_zombieword_sleep(world):
    menu:
        "Eat" if world.player.food > 0:
            python:
                ZombieWorldChangeVitality(world.player, 1).run()
                world.player.food -= 1
            if world.player.vitality < world.player.max_vitality:
                menu:
                    'Use drugs' if world.player.drugs > 0:
                        python:
                            ZombieWorldChangeVitality(world.player, 1).run()
                            world.player.drugs -= 1
                    'Go to sleep':
                        $ pass
        "Hungry sleep":
            $ ZombieWorldChangeVitality(world.player, -1).run()
        "I must go":
            return False
    'You sleep'
    python:
        if world.player.gender != 'female':
            ZombieWorldChangeFilth(world.player, 1).run()
    return True


label lbl_zombieworld_combat(combat, world):
    $ normal_heart = ZombieWorldUtilities.normal_heart_image()
    $ black_heart = ZombieWorldUtilities.cursed_heart_image()
    $ skull = ZombieWorldUtilities.small_skull_icon()
    while combat.active:
        python:
            icon = normal_heart if combat.player.vitality > combat.player.filth else black_heart
            if combat.player.vitality < 1:
                icon = skull
            power = combat.player_power()
            ghouls = combat.ghoul_power
            ammo_cons = combat.ammo_consumption()
        menu:
            'Ghouls: [ghouls]'
            'Fight ([power], {image=[icon]})':
                $ combat.fight()
            'Shoot the ghoul ([ammo_cons])' if combat.can_shoot():
                $ combat.shoot()
