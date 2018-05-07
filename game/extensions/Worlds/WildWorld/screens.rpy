screen sc_wildworld_stats(world):
    
    window:
        background Color((0, 0, 0, 100))
        xfill True
        yfill True
        ysize 720
        xsize 192
        xpos 1168

        vbox:
            spacing 10
            xalign 0.5
            xsize 180
            image im.Scale(world.player.avatar, 180, 180):
                xalign 0.5
            vbox:
                for value in world.player.show_attributes().values():
                    text value
                


