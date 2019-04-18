init python:
    def class_tier_bonus(user, context):
        return user.person_class.tier

    def best_attr_bonus(user, context):
        attr = max(user.attributes().keys(), key=lambda x: user.attribute(x))
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
            'attribute': best_attr_bonus,
        },
    }