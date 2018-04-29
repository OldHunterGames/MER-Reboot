# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

init -10 python:
    sys.path.append(renpy.loader.transfn("scripts"))
    # sys.path.append(renpy.loader.transfn("scripts/person"))
    # sys.path.append(renpy.loader.transfn("core"))
    from mer_person import *
    from mer_angel import *
    from mer_utilities import *
    from mer_core import *

# The game starts here.

label start:
    $ player = CorePerson('ADAM', 'male')
    $ core = MERCore()
    $ core.player = player
    call _main

    return

label _main:
    while True:
        call lbl_main
    return

label lbl_main:
    menu:
        'Me':
            call screen sc_cis(player)
        'Others':
            call screen sc_contacts()
        'Travel to outer worlds':
            'You visited and synchronised outer world'
            python:
                angel = CoreAngel('Placeholder', grade=CoreAngel.DOMINATION_GRADE)
                player.add_angel(angel)

    return

label lbl_make_patricians():
    python:
        for i in xrange(16):
            angel = CoreAngel('Placeholder', grade=CoreAngel.DOMINATION_GRADE)
            person = CorePerson('Placeholder1' + str(i))
            person.add_angel(angle)
            core.add_character(person)
