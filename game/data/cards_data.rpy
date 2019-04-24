init python:
    def class_tier_bonus(user, context):
        return user.person_class.tier

    def soul_level_bonus(user, context):
        return user.soul_level

    def best_attr_bonus(user, context):
        attr = max(user.attributes().values())
        return attr

    def best_attr_suit(user, context):
        attr = max(user.attributes().keys(), key=lambda x: user.attribute(x))
        suit = Suits.attribute_as_suit(attr)
        return suit

    person_cards_data = {
        'wrestling': {
            'name': __("Wrestling"),
            'suit': 'skull',
            'attribute': 'might',
        },
        'slippery_skin': {
            'name': __("Slippery skin"),
            'suit': 'skull',
            'attribute': 'subtlety',
        },
        'whip_lash': {
            'name': __("Whip lash"),
            'suit': 'spades',
            'value': 1,
        },
        'far_reach': {
            'name': __("Far reach"),
            'suit': 'skull',
            'attribute': 'subtlety',
        },
        'pain_resilience': {
            'name': __("Pain resilience"),
            'suit': 'skull',
            'attribute': 'soul',
        },
        'punch': {
            'name': __("Punch"),
            'suit': 'skull',
            'attribute': 'might',
        },
        'evasive': {
            'name': __("Evasive"),
            'suit': 'skull',
            'attribute': 'subtlety',
        },
        'cestus': {
            'name': __("Cestus"),
            'suit': 'spades',
            'attribute': 'might',
        },
        'combat_expirience': {
            'name': __("Combat expirience"),
            'suit': 'spades',
            'custom': class_tier_bonus,
        },
        'blunt_weapon': {
            'name': __("Blunt weapon"),
            'suit': 'skull',
            'value': 5,
        },
        'padded_armor': {
            'name': __("Padded armor"),
            'suit': 'diamonds',
            'value': 1,
        },
        'sword': {
            'name': __("Sword"),
            'suit': 'spades',
            'attribute': 'might',
        },
        'shield': {
            'name': __("Shield"),
            'suit': 'clubs',
            'attribute': 'might',
        },
        'dual_strike': {
            'name': __("Dual strike"),
            'suit': 'spades',
            'attribute': 'subtlety',
        },
        'trident': {
            'name': __("Trident"),
            'suit': 'clubs',
            'attribute': 'might',
        },
        'net': {
            'name': __("Net"),
            'suit': 'hearts',
            'attribute': 'subtlety',
        },
        'knife': {
            'name': __("Sword"),
            'suit': 'spades',
            'value': 1,
        },
        'two_handed_sword': {
            'name': __("Two-handed sword"),
            'suit': 'hearts',
            'attribute': 'might',
        },
        'imposing_fear': {
            'name': __("Imposing fear"),
            'suit': 'hearts',
            'attribute': 'charisma',
        },
        'pyramid_helm': {
            'name': __("Pyramid helm"),
            'suit': 'clubs',
            'value': 3,
        },
        'steel_whip': {
            'name': __("Steel whip"),
            'suit': 'spades',
            'attribute': 'subtlety',
        },
        'distracting_nudity': {
            'name': __("Distracting nudity"),
            'suit': 'spades',
            'attribute': 'charisma',
        },
        'half_armored': {
            'name': __("Half-armored"),
            'suit': 'diamonds',
            'value': 3,
        },
        'exotic_weapon': {
            'name': __("Exotic weapon"),
            'suit': best_attr_suit,
            'custom': best_attr_bonus,
        },
        'lucky': {
            'name': __("Lucky"),
            'suit': 'diamonds',
            'custom': soul_level_bonus,
        },
        'shared_wisdom': {
            'name': __("Shared wisdom"),
            'suit': 'clubs',
            'attribute': 'knowledge',
            'type': 'combat_support',
        },
        'satisfaction': {
            'name': __("Satisfaction"),
            'suit': 'hearts',
            'attribute': 'charisma',
        },
        'betrayal': {
            'name': __("Betrayal"),
            'suit': 'hearts',
            'custom': soul_level_bonus,
        },
        'smart_tactics': {
            'name': __("Smart tactics"),
            'suit': 'diamonds',
            'attribute': 'knowledge',
        },
        'tactical_advice': {
            'name': __("Tactical advice"),
            'suit': 'diamonds',
            'custom': class_tier_bonus,
        },
        'deception': {
            'name': __("Deception"),
            'suit': 'spades',
            'attribute': 'subtlety',
        },
        'public_approval': {
            'name': __("Public approval"),
            'suit': 'hearts',
            'attribute': 'charisma',
        },
        'living_legend': {
            'name': __("Living legend"),
            'suit': 'joker',
            'value': 1,
        },
        'wisdom_of_many_lives': {
            'name': __("Wisdom of many lives"),
            'suit': 'diamonds',
            'custom': soul_level_bonus,
        },
        'slippery_words': {
            'name': __("Slippery words"),
            'suit': 'skull',
            'attribute': 'subtlety',
        },
        'stubborn': {
            'name': __("Stubborn"),
            'suit': 'skull',
            'attribute': 'might',
        },
        'struggle': {
            'name': __("Struggle"),
            'suit': 'skull',
            'attribute': 'might',
        },
        'common_sense': {
            'name': __("Common sense"),
            'suit': 'skull',
            'attribute': 'knowledge',
        },
        'natural_charm': {
            'name': __("Natural charm"),
            'suit': 'skull',
            'attribute': 'charisma',
        },
    }