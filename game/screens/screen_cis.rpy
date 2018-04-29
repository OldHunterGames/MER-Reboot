
style char_info_window is window:
    background Color((0, 0, 0, 255))
    xfill True
    yfill True
    xsize 1280
    ysize 720

label lbl_cis_glue(person, controlled=False, relations=None):
    call screen sc_cis(person, controlled, relations)
    return


label lbl_new_meeting(person):
    $ new_person = core.person_creator.gen_random_person()
    $ person.relations(new_person)
    $ core.faction.add_member(new_person)
    return

screen sc_cis(person, controlled=False, relations=None):

    window:
        style 'char_info_window'
        hbox:
            vbox:
                image im.Scale(person.avatar, 200, 200)
                text person.firstname:
                    xalign 0.5
                textbutton "Leave" action Return()
            vbox:
                for i in sorted(person.get_host(), key=lambda x: x.level()):
                    text encolor_text(i.name, i.level())
                
