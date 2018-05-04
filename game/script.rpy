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
    call lbl_make_initial_characters()
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

label lbl_make_initial_characters():
    python:
        patricians = [renpy.call_in_new_context('lbl_make_patrician') for i in range(12)]
        free_patricians = [renpy.call_in_new_context('lbl_make_patrician') for i in range(4)]
        senators = [renpy.call_in_new_context('lbl_make_senator') for i in range(6)]
        free_senators =[renpy.call_in_new_context('lbl_make_senator') for i in range(2)]
        nobles = [renpy.call_in_new_context('lbl_make_noble') for i in range(2)]
        free_nobles = [renpy.call_in_new_context('lbl_make_noble') for i in range(2)]
        princeps = renpy.call_in_new_context('lbl_make_princeps', 'serpis')
        for i in senators + free_senators:
            Hierarchy(i).add_clientela(patricians.pop())
        Hierarchy(random.choice(senators)).add_clientela(patricians.pop())
        Hierarchy(random.choice(free_senators)).add_clientela(patricians.pop())
        for i in nobles + free_nobles:
            Hierarchy(i).add_clientela(senators.pop())
        Hierarchy(random.choice(nobles)).add_clientela(senators.pop())
        Hierarchy(random.choice(free_nobles)).add_clientela(senators.pop())
        for i in nobles:
            Hierarchy(princeps).add_clientela(i)
    return 

label lbl_make_patrician():
    python:
        angel = AngelMaker.gen_archon()
        person = PersonCreator.gen_person()
        person.add_angel(angel)
        core.add_character(person)
    return person

label lbl_make_senator():
    python:
        senator = PersonCreator.gen_person()
        angel = AngelMaker.gen_ellochim()
        for i in range(2):
            a = AngelMaker.gen_archon()
            angel.add_angel(a)
            senator.add_angel(a)
        senator.add_angel(angel)
        core.add_character(senator)
    return senator

label lbl_make_noble():
    python:
        noble = PersonCreator.gen_person()
        cherub = AngelMaker.gen_cherub()
        ellohims = [AngelMaker.gen_ellochim() for i in range(2)]
        archons = [AngelMaker.gen_archon() for i in range(4)]
        for i in ellohims:
            cherub.add_angel(i)
            noble.add_angel(i)
        for i in range(2):
            ellohim = ellohims[i]
            for n in archons[i*2: i*2+2]:
                ellohim.add_angel(n)
            noble.add_angel(ellohim)
        noble.add_angel(cherub)
        core.add_character(noble)
    return noble

label lbl_make_princeps(house):
    python:
        princeps = PersonCreator.gen_person()
        seraph = AngelMaker.gen_seraph(house)
        cherubs = [AngelMaker.gen_cherub() for i in range(2)]
        ellohims = [AngelMaker.gen_ellochim() for i in range(4)]
        archons = [AngelMaker.gen_archon() for i in range(8)]
        core.add_character(princeps)
        for i in cherubs:
            princeps.add_angel(i)
            seraph.add_angel(i)
        for i in range(2):
            cherub = cherubs[i]
            for n in ellohims[i*2: i*2+2]:
                cherub.add_angel(n)
                princeps.add_angel(n)
        for i in range(4):
            ellohim = ellohims[i]
            for n in archons[i*2: i*2+2]:
                ellohim.add_angel(n)
                princeps.add_angel(n)
        princeps.add_angel(seraph)
    return princeps
