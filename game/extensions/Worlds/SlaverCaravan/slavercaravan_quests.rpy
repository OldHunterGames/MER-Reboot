## Slaver's caravan quest

init python:
    slavercaravan_quests = ['beggar', 'donation', 'virgin', 'bunch', 'perfect']

label lbl_slavercaravan_quest_beggar(world):
    show expression world.path('bg/quest_beggar.png') as bg
    "You see a starving woman in a torn clothes sitting on the street. She is begging for some food but people ingnore her."
    menu:
        "You can take advantage or save her..."
        "{color=#0000ffff}(food > 0){/color} Give some food" if world.food > 0:
            $ world.food -= 1
        "{color=#0000ffff}(food => 10){/color} Give all you have" if world.food > 9:
            "Beggar will pray for you. {color=#00ff00}Archon is pleased{/color}"
            $ world.food = 0
            $ world.quests_completed += 1
            $ world.locations.current_location().quest = None
        "Just ignor her as all people do":
            "She'll probably die soon anyway... such a waste."
            $ world.locations.current_location().quest = None
        "Rape the beggar":
            "Your state is impoved, but beggars now hate you..."
            $ world.player.state += 1
            $ world.locations.current_location().quest = None

    return

label lbl_slavercaravan_quest_donation(world):
    show expression world.path('bg/quest_priest.png') as bg
    define bishop = Character('Bishop', color="#c8ffc8")
    "There is a prominent cathedral in this town. Maybe someone there can pray for you, to please archon [world.archon.name]."
    bishop "For a small donation of 50 food, our church will pray for attonement of your sins indefinetely, my child."
    menu:
        "{color=#0000ffff}(food > 0){/color} I have much less, but take this please. I'll get more someday." if world.food > 0:
            "You donated small ammout of food to church."
            $ world.food -= 1
        "{color=#0000ffff}(food => 50){/color} I'll humbly donate this food to a church" if world.food > 49:
            "Priest will mention you in all the prayers from now on.\n {color=#00ff00}Archon is pleased{/color}"
            $ world.food -= 50
            $ world.quests_completed += 1
            $ world.locations.current_location().quest = None
        "I'm starving myself. Please give me a food, father!":
            bishop "Here you are. {i}Pax vobiscum{/i}."
            "You gou a cup of watery cabbage stew. But priest will not listen you anymore."
            $ world.food += 1
            $ world.locations.current_location().quest = None

    return

label lbl_slavercaravan_quest_virgin(world):
    $ girls = SlaverCaravanFilter.filter_by_gender(world.characters, 'female')
    image listvennik = 'extensions/Worlds/SlaverCaravan/character/oleysha.png'
    image whore = 'extensions/Worlds/SlaverCaravan/character/oldwhore.png'
    define listvennik = Character('Skinny Boy', color="#c8f0c8")
    define whore = Character('Old Whore', color="#800000")
    "Passing by the street you hear an angry woman voice in a dark alley."
    show whore at left with dissolve
    whore "You are disgusting little brat. How dare you!"
    show listvennik at right with dissolve
    listvennik "S-sorry m'eam, b-but you are... um... the p-pr..."
    whore "Who am I?!"
    listvennik "Uh. I mean y-you do it... with a man... f-for a money"
    whore "WHAAAAT? You dare to call me a whore?!"
    whore "You are the miserable little bag of rotten semen. No woman in all the world will touch your wrinkled little snag! Not for all the money in the fucking world!!"
    listvennik "B-but I putt off all my school breakfast money for a year to get 10 g.p. for you"
    whore "You whant to defile such a noble whoman as me for a mere 10 g.p?! Pff! It's just so insulting."
    listvennik "B-but Yaroch-kun said you sucked him for a 1 g.p."
    whore "SHUT UP, YOU MOTHERFUCKER!!!"
    whore "Thats it. I'm calling a pimp and he will beat all the crap out of you!!"
    listvennik "N-no! P-please... m'eam I'd never mean to offend you... please"
    whore "Give me 5 g.p. and get the hell out of here."
    listvennik "Yes, yes. Here you are."
    whore "Now fuck off, you little weirdo!"
    hide listvennik with moveoutright
    "Whore stayed in the alley to count her ill gained gold, while a boy run off towards you..."
    hide whore with dissolve
    "This damn kid is running like crasy with a tears in his eyes. He is so distracted that he flew straight into you."
    show listvennik at center with moveinright
    show listvennik at center with vpunch
    listvennik "Whaaaa.... It hurts... ouch..."
    player "Mind you way!"
    listvennik "Oh... I'm so sorry"
    player "Hm. Just for lulz. What is your name?"
    listvennik "I'm Aleosha."
    player "So, Aleosha..."
    menu:
        "You can use this kid to your profit. He appears to used to be used anyway."
        "I'm a pimp. Give me all your money":
            listvennik "Oh now. Don't hurt me. This is all I have. 5 gold. Get it. Just don't hurt me, please!"
            $ world.food += 5
            "You got 5 food"
        "{color=#0000ffff}(have a slavegirl){/color} I'll give you a slavegirl to play with, kid.":
            $ slave = PickSlave(girls, world).call()
            $ world.remove_character(slave)
            listvennik "My own slavegirl? WOW! THANK YOU SO MUCH!!!"
            "He will pray for your soul till the end of his days. {color=#00ff00}Archon is pleased{/color}"
            $ world.quests_completed += 1
            $ world.locations.current_location().quest = None

    return

label lbl_slavercaravan_quest_bunch(world):
    "You a farm destroyed by the fire. Farmer lose all his family and workers and now have no means to attend his land."
    "He desperately need a bunch of ANY slaves. At least three of them in a bunch"
    menu:
        "I have a plenty of slaves. You need them more than me, good man." if len(world.characters) > 2:
            "You saved the farm and old man, so he will pray for you untill end of his days.\n {color=#00ff00}Archon is pleased{/color}"
            $ world.quests_completed += 1
            $ world.locations.current_location().quest = None
            $ world.slaves_escape()
        "I can't help righ now":
            $ pass

    return

label lbl_slavercaravan_quest_perfect(world):
    $ slaves = SlaverCaravanFilter.filter_by_attribute(world.characters, 5)
    "Local ruler seeks a mate. You can present a slave with a {color=#FFBF00}perect{/color} attribute to him."
    menu:
        "I'll present a slave to ruler" if slaves:
            $ slave = PickSlave(slaves, world).call()
            $ world.remove_character(slave)
            "Slave is grateful to become a rulers concubine and will pray for you.\n {color=#00ff00}Archon is pleased{/color}"
            $ world.quests_completed += 1
            $ world.locations.current_location().quest = None
        "Maybe later":
            $ pass

    return
