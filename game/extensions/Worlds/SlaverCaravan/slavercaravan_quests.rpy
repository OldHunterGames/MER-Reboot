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
    show expression world.path('bg/quest_priest.png') as bg
    define bishop = Character('Bishop', color="#c8ffc8")
    "There is a prominent cathedral in this town. Maybe someone there can pray for you, to please archon [world.archon.name]."
    bishop "For a small donation of 50 food, our church will pray for attonement of your sins indefinetely, my child."
    "{color=#0000ffff}(food > 0){/color} I have much less, but take this please. I'll get more someday." if world.food > 0:
        "You donated small ammout of food to church."
        $ world.food -= 1
    "{color=#0000ffff}(food => 50){/color} I'll humbly donate this food to a church" if world.food > 49:
        "Priest will mention you in all the prayers from now on. {color=#00ff00}Archon is pleased{/color}"
        $ world.food -= 50
        $ world.quests_completed += 1
        $ world.current_location.quest = None
    "I'm starving myself. Please give me a food, father!":
        bishop "Here you are. {i}Pax vobiscum{/i}."
        "You gou a cup of watery cabbage stew. But priest will not listen you anymore."
        $ world.food += 1
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
