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
    python:
        for i in range(40):
            core.add_character(PersonCreator.gen_person())
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
            $ ContactsInfo(core.characters).show()
        'Travel to outer worlds':
            'You visited and synchronised outer world'
            python:
                angel = AngelMaker.gen_archon()
                player.add_angel(angel)

    return

label lbl_make_patrician():
    python:
        angel = AngelMaker.gen_archon()
        person = PersonCreator.gen_person()
        person.add_angel(angel)
        core.add_character(person)
        patricians.append((person, angel))
    return person

label lbl_make_senator():
    python:
        senator = PersonCreator.gen_person()
        angel = AngelMaker.gen_ellohim()
        for i in range(2):
            a = AngelMaker.gen_archon()
            angel.add_angel(a)
            senator.add_angel(a)
        senator.add_angel(angel)
    return senator

label lbl_make_noble():
    python:
        noble = PersonCreator.gen_person()
        cherub = AngelMaker.gen_cherub()
        ellohims = [AngelMaker.gen_ellohim() for i in range(2)]
        archons = [AngelMaker.gen_archon() for i in range(4)]
        for i in ellohims:
            cherub.add_angel(i)
            noble.add_angel(i)
        for i in range(2):
            for n in archons[i*2, i*2+2]:
                i.add_angel(n)
                noble.add_angel(n)
        noble.add_angel(cherub)
    return noble




label lbl_make_princeps(house):
    python:
        angel = AngelMaker.gen_seraph(house)
        person = CorePerson('%s leader' % house.capitalize())
        person.add_angel(angel)
        core.add_character(person)
    return {'angel': angel, 'person': person}

label lbl_make_nobles():
    python:
        seraph, princeps = lbl_make_princeps('serpis')
        for i in range(2):
            angel = AngelMaker.gen_cherub()
            person = CorePerson('Noble person')
            person.add_angel(person)
            core.add_character(person)
            seraph.add_angel(angel)

