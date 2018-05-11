init python:
    wildworld_attributes = {
        'might': {'name': __('Might'), 'low': __('Weak'), 'high': __('Hardy')},
        'subtlety': {'name': __('Subtlety'), 'low': __('Naive'), 'high': __('Subtle')},
        'charisma': {'name': __('Charisma'), 'low': __('Boring'), 'high': __('Charming')},
        'knowledge': {'name': __('Knowledge'), 'low': __('Incompetent'), 'high': __('Competent')},
    }

    wildworld_features = {
        'male': {'slot': 'gender', 'name': __('Male'), 'might': 1, 'subtlety': -1},
        'female': {'slot': 'gender', 'name': __('Female'), 'subtlety': 1, 'might': -1},
    }

    wildworld_cities = {
        'market_city': {
            'description': __("City with market"), 'label': 'lbl_wildworld_market_city',
        },
        'brothel_city': {
            'description': __("City with brothel"), 'label': 'lbl_wildworld_brothel_city',
        }
    }

    wildworld_locations = {
        'road': {
            'name': __('Road'), 'description': __("Road"), 'label': 'lbl_wildworld_road'
        },
        'wildness': {
            'name': __("Wildness"), 'description': __("Wildness"), 'label': 'lbl_wildworld_wildness'
        }
    }

    wildworld_city_names = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Name6', 'Name7']

    wildworld_items = {
        'sturdy_rope': {
            'description': __("For a one unit of food you can buy five pieces of sturdy rope. It's a basic way to restrain a slave, not overly secure, but cheap. You can buy rope anywhere."),
            'name': __("Sturdy rope"),
            'price': 0.2,
            'tags': ['enslave'],
        },
        'leather_restraints': {
            'name': __("Lether restraints"),
            'description': __("Specially arranged leather restraints is a better way to hold a slave, cutting chances to escape a half."),
            'price': 1,
            'escape_chance': lambda x: x//2,
            'tags': ['enslave'],
        },
        'wooden_pads': {
            'name': __("Wooden pads"),
            'description': __(""),
            'price': 2,
            'escape_chance': lambda x: 0,
            'food_consumption': lambda x: x*2,
            'tags': ['enslave'],
        },
        'iron_shackles': {
            'name': __("Iron shackles"),
            'description': __("You can buy shackles only in advanced town."),
            'price': 10,
            'escape_chance': lambda x: 0,
            'tags': ['enslave'],
        }
    }