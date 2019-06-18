from mer_class import PersonClass, PriceCalculator, MerArenaMaker
from mer_person import PersonCreator
import random

def make_gladiator(allowed_classes=None, person_generator_params=None, min_tier=0, max_tier=5):
        if person_generator_params is None:
            person_generator_params = {}
        while True:
            gladiator = PersonCreator.gen_person(genus='human', **person_generator_params)
            if allowed_classes is not None:
                classes = allowed_classes
            else:
                classes = PersonClass.pipe_filters(PersonClass.class_filter, PersonClass.gender_filter)(
                   gladiator, PersonClass.get_by_tag('gladiator'))
                classes = [i for i in classes if i.tier >= min_tier and i.tier <= max_tier]
            classes_to_give = []
            for i in classes:
                if gladiator.attribute(i.key_attributes[0]) >= i.tier:
                    classes_to_give.append(i)
            if len(classes_to_give) < 1:
                continue
            gladiator.person_class = random.choice(classes_to_give)

            return gladiator

        return gladiator
    
def make_mudfight_gladiator():
    return make_gladiator(PersonClass.get_by_ids(['lucator']), {'gender': 'female'})

def make_whipfight_gladiator():
    return make_gladiator(PersonClass.get_by_ids(['andabant']), {'gender': 'female'})

def make_pitfight_gladiator():
    return make_gladiator(PersonClass.get_by_ids(['pugilist']), {'gender': 'male'})

def make_gladiator_fit_raiting(low, high, calculator, max_tier=5):
    min_tier = 0
    def inner():
        while True:
            if low >= 30:
                min_tier = 2
            if low >= 100:
                min_tier = 3
            glad = make_gladiator(min_tier=min_tier, max_tier=max_tier)
            price = calculator(glad).training_price()
            if price >= low and price <= high:
                return glad
    return inner

def make_champion():
    return make_gladiator(PersonClass.get_by_tag('gladiator', PersonClass.get_by_tier(5)))

def default_arena_prize(arena):
    sparks = arena.enemy.person_class.tier * 5
    if arena.fight.is_player_win():
        sparks *= 2
    return sparks

def lupanarium_prize(arena):
    if arena.fight.is_player_win():
        prize = 15
    else:
        value = arena.fight.player_combatant.attribute('charisma')
        if value < 0:
            prize = 1
        else:
            prize = 5 + 5 * value
    if arena.fight.player_combatant.person_class == PersonClass.get_by_id('lucator'):
        prize += 5
    return prize

def whipfight_prize(arena):
    return PriceCalculator(arena.enemy).training_price()

def filter_equipment(card):
    return card.type != 'equipment'

pitfight_classes = PersonClass.get_by_ids(['lucator', 'pugilist', 'menial_slave'])
heat_up_classes = list(set(PersonClass.get_by_tag('gladiator'))
    .difference(set(PersonClass.get_by_tier(4)))
    .difference(set(PersonClass.get_by_tier(5)))
)
enemies = list(set(heat_up_classes).intersection(set(PersonClass.get_by_tier(3))))
grand_fight_classes = PersonClass.get_by_tag('gladiator')
available_arenas = {
    'mudfight': MerArenaMaker(
        make_mudfight_gladiator, lambda person: person.gender == 'female', lupanarium_prize, die_after_fight=False, cards_filter=filter_equipment, arena_bg='brothel', selection_bg='images/bg/brothel.png'
    ),
    'whip_fight': MerArenaMaker(
        make_whipfight_gladiator, lambda person: person.gender == 'female', lupanarium_prize, min_player_level=3, die_after_fight=False, arena_bg='brothel', selection_bg='images/bg/brothel.png'
    ),
    'pitfight': MerArenaMaker(
        make_pitfight_gladiator,
        lambda person: person.gender == 'male',
        default_arena_prize,
        die_after_fight=False,
        cards_filter=filter_equipment,
        arena_bg='pit',
        selection_bg='images/bg/tavern_empty.png',
    ),
    'chaotic_fights': MerArenaMaker(
        make_gladiator,
        lambda person: True,
        lambda _: 0,
        die_after_fight=False,
        gain_prestige=False,
        can_skip_enemy=True,
        arena_bg='arena',
        selection_bg='images/bg/arena.png',
    ),
    'common_fight': MerArenaMaker(
        make_gladiator_fit_raiting(30, 100, PriceCalculator, max_tier=3),
        lambda person: True,
        default_arena_prize,
        min_player_level=2,
        arena_bg='arena',
        selection_bg='images/bg/arena.png',
    ),
    'premium_fights': MerArenaMaker(
        make_gladiator_fit_raiting(100, 150, PriceCalculator),
        lambda person: True,
        default_arena_prize,
        min_player_level=3,
        arena_bg='arena',
        selection_bg='images/bg/arena.png',
    ),
    'tournament': MerArenaMaker(
        make_gladiator,
        lambda person: True,
        default_arena_prize,
        min_player_level=4,
        arena_bg='arena',
        selection_bg='images/bg/arena.png',
    )
}

def make_starter_slave():
    slave = PersonCreator.gen_person(genus='human')
    slave.person_class = PersonClass.random_by_tag('starter')
    return slave

def setup_arenas(core):
    for arena in available_arenas.values():
        core.skip_turn.add_callback(arena.set_gladiator)