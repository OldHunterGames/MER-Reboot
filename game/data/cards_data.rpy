init python:
    def context_or_empty(context):
        return {} if context is None else context

    def class_tier_bonus(user, context):
        context = context_or_empty(context)
        return user.person_class.tier

    def soul_level_bonus(user, context):
        context = context_or_empty(context)
        return user.soul_level

    def best_attr_bonus(user, context):
        context = context_or_empty(context)
        attr = max(user.attributes().values())
        return attr

    def best_attr_suit(user, context):
        context = context_or_empty(context)
        attr = max(user.attributes().keys(), key=lambda x: user.attribute(x))
        suit = Suits.attribute_as_suit(attr)
        return suit
    
    def joker_power(user, context):
        context = context_or_empty(context)
        return 1 if context.get('isEnemy', False) else 5

    person_cards_data = {
        'wrestling': {
            'name': __("Wrestling"),
            'suit': 'skull',
            'attribute': 'might',
            'type': 'skill',
        },
        'slippery_skin': {
            'name': __("Slippery skin"),
            'suit': 'skull',
            'attribute': 'subtlety',
            'type': 'skill',
        },
        'whip_lash': {
            'name': __("Whip lash"),
            'suit': 'spades',
            'value': 1,
            'type': 'equipment',
        },
        'far_reach': {
            'name': __("Far reach"),
            'suit': 'skull',
            'attribute': 'subtlety',
            'type': 'equipment',
        },
        'pain_resilience': {
            'name': __("Pain resilience"),
            'suit': 'skull',
            'attribute': 'soul',
            'type': 'skill',
        },
        'punch': {
            'name': __("Punch"),
            'suit': 'skull',
            'attribute': 'might',
            'type': 'skill',
        },
        'evasive': {
            'name': __("Evasive"),
            'suit': 'skull',
            'attribute': 'subtlety',
            'type': 'skill',
        },
        'cestus': {
            'name': __("Cestus"),
            'suit': 'spades',
            'attribute': 'might',
            'type': 'equipment',
        },
        'combat_expirience': {
            'name': __("Combat expirience"),
            'suit': 'spades',
            'custom': class_tier_bonus,
            'type': 'skill',
        },
        'blunt_weapon': {
            'name': __("Blunt weapon"),
            'suit': 'skull',
            'value': 5,
            'type': 'equipment',
        },
        'padded_armor': {
            'name': __("Padded armor"),
            'suit': 'diamonds',
            'value': 1,
            'type': 'equipment',
        },
        'sword': {
            'name': __("Sword"),
            'suit': 'spades',
            'attribute': 'might',
            'type': 'equipment',
        },
        'shield': {
            'name': __("Shield"),
            'suit': 'clubs',
            'attribute': 'might',
            'type': 'equipment',
        },
        'dual_strike': {
            'name': __("Dual strike"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'type': 'skill',
        },
        'trident': {
            'name': __("Trident"),
            'suit': 'clubs',
            'attribute': 'might',
            'type': 'equipment',
        },
        'net': {
            'name': __("Net"),
            'suit': 'hearts',
            'attribute': 'subtlety',
            'type': 'equipment',
        },
        'knife': {
            'name': __("Sword"),
            'suit': 'spades',
            'value': 1,
            'type': 'equipment',
        },
        'two_handed_sword': {
            'name': __("Two-handed sword"),
            'suit': 'hearts',
            'attribute': 'might',
            'type': 'equipment',
        },
        'imposing_fear': {
            'name': __("Imposing fear"),
            'suit': 'hearts',
            'attribute': 'charisma',
            'type': 'skill',
        },
        'pyramid_helm': {
            'name': __("Pyramid helm"),
            'suit': 'clubs',
            'value': 3,
            'type': 'equipment',
        },
        'steel_whip': {
            'name': __("Steel whip"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'type': 'equipment',
        },
        'distracting_nudity': {
            'name': __("Distracting nudity"),
            'suit': 'spades',
            'attribute': 'charisma',
            'type': 'skill',
        },
        'half_armored': {
            'name': __("Half-armored"),
            'suit': 'diamonds',
            'value': 3,
            'type': 'equipment',
        },
        'exotic_weapon': {
            'name': __("Exotic weapon"),
            'suit': best_attr_suit,
            'custom': best_attr_bonus,
            'type': 'equipment',
        },
        'lucky': {
            'name': __("Lucky"),
            'suit': 'diamonds',
            'custom': soul_level_bonus,
            'type': 'skill',
        },
        'shared_wisdom': {
            'name': __("Shared wisdom"),
            'suit': 'clubs',
            'attribute': 'knowledge',
            'type': 'skill',
        },
        'satisfaction': {
            'name': __("Satisfaction"),
            'suit': 'hearts',
            'attribute': 'charisma',
            'type': 'skill',
        },
        'betrayal': {
            'name': __("Betrayal"),
            'suit': 'hearts',
            'custom': soul_level_bonus,
            'type': 'skill',
        },
        'smart_tactics': {
            'name': __("Smart tactics"),
            'suit': 'diamonds',
            'attribute': 'knowledge',
            'case': 'combat',
        },
        'tactical_advice': {
            'name': __("Tactical advice"),
            'suit': 'clubs',
            'custom': class_tier_bonus,
            'type': 'support',
            'case': 'combat',
        },
        'deception': {
            'name': __("Deception"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'type': 'skill',
        },
        'public_approval': {
            'name': __("Public approval"),
            'suit': 'hearts',
            'attribute': 'charisma',
            'type': 'skill',
        },
        'living_legend': {
            'name': __("Living legend"),
            'suit': 'joker',
            'custom': joker_power,
            'type': 'skill',
        },
        'wisdom_of_many_lives': {
            'name': __("Wisdom of many lives"),
            'suit': 'diamonds',
            'custom': soul_level_bonus,
            'type': 'skill',
        },
        'slippery_words': {
            'name': __("Slippery words"),
            'suit': 'skull',
            'attribute': 'subtlety',
            'type': 'skill',
        },
        'stubborn': {
            'name': __("Stubborn"),
            'suit': 'skull',
            'attribute': 'might',
            'type': 'skill',
        },
        'struggle': {
            'name': __("Struggle"),
            'suit': 'skull',
            'attribute': 'might',
            'type': 'skill',
        },
        'common_sense': {
            'name': __("Common sense"),
            'suit': 'skull',
            'attribute': 'knowledge',
            'type': 'skill',
        },
        'natural_charm': {
            'name': __("Natural charm"),
            'suit': 'skull',
            'attribute': 'charisma',
            'type': 'skill',
        },
        'champion': {
            'name': __("Champion"),
            'suit': 'joker',
            'custom': joker_power,
            'type': 'skill'
        },
        'bravado': {
            'name': __("Bravado"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'tag': 'fellowship',
            'type': 'support',
        }
    }