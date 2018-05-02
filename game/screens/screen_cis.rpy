
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

label lbl_cis_glue(person, controlled=False, relations=None):
    call screen sc_cis(person, controlled, relations)
    return

screen sc_cis(person, controlled=False, relations=None):

    window:
        style 'char_info_window'
        vbox:
            image im.Scale(person.avatar, 200, 200)
            text person.firstname:
                xalign 0.5
            textbutton "Leave" action Return()
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
                    for i in sorted(person.get_host(), key=lambda x: x.level()):
                        textbutton encolor_text(i.name, i.level()):
                            text_style 'mer_text'
                            action Function(lambda: print('kek'))
                    
