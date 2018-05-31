## Slaver's caravan quest

init python:
    slavercaravan_quests = ['beggar', 'donation', 'virgin', 'bunch', 'perfect']

label lbl_slavercaravan_quest_beggar(world):
    menu:
        "Beggar asks for food"
        "Give some" if world.food > 0:
            $ world.food -= 1
        "Give all you have" if world.food > 5:
            $ world.food = 0
            $ world.quests_completed += 1
            $ world.current_location.quest = None
        "No way":
            $ world.current_location.quest = None

    return

label lbl_slavercaravan_quest_donation(world):
    "Donation quest done"
    $ world.quests_completed += 1
    $ world.current_location.quest = None

    return

label lbl_slavercaravan_quest_virgin(world):
    "Virgin quest done"
    $ world.quests_completed += 1
    $ world.current_location.quest = None

    return

label lbl_slavercaravan_quest_bunch(world):
    "Bunch quest done"
    $ world.quests_completed += 1
    $ world.current_location.quest = None

    return

label lbl_slavercaravan_quest_perfect(world):
    "Perfect quest done"
    $ world.quests_completed += 1
    $ world.current_location.quest = None
    
    return
