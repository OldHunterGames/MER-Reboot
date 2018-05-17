init python:
    slavercaravan_attributes = {
        'might': {'name': __('Might'), 'low': __('Weak'), 'high': __('Hardy')},
        'subtlety': {'name': __('Subtlety'), 'low': __('Naive'), 'high': __('Subtle')},
        'charisma': {'name': __('Charisma'), 'low': __('Boring'), 'high': __('Charming')},
        'knowledge': {'name': __('Knowledge'), 'low': __('Incompetent'), 'high': __('Competent')},
    }

    slavercaravan_features = {
        'male': {'slot': 'gender', 'name': __('Male'), 'might': 1, 'subtlety': -1},
        'female': {'slot': 'gender', 'name': __('Female'), 'subtlety': 1, 'might': -1},
    }

    slavercaravan_physical_features = {
        'tall': {'slot': 'height', 'name': __('Tall'), 'might': 1, 'subtlety': -1},
        'small': {'slot': 'height', 'name': __('Small'), 'might': -1, 'subtlety': 1},
        'subtle': {'slot': 'constitution', 'name': __('Subtle'), 'might': -1, 'subtlety': 1},
        'brawny': {'slot': 'constitution', 'name': __('Brawny'), 'might': 1, 'subtlety': -1},
        'husky_voice': {'slot': 'voice', 'name': __('Husky voice'), 'might': 1, 'charisma': -1},
        'clear_voice': {'slot': 'voice', 'name': __('Clear voice'), 'might': -1, 'charisma': 1},
        'seductive_smile': {'slot': 'smile', 'name': __('Seductive smile'), 'subtlety': 1, 'might': -1},
        'coarse_grin': {'slot': 'smile', 'name': __('Coarse grin'), 'might': 1, 'charisma': -1},
        'giggly': {'slot': 'smile', 'name': __('Giggly'), 'charisma': 1, 'knowledge': -1},
        'inexpressive_face': {'slot': 'smile', 'name': __('Inexpressive face'), 'charisma': -1, 'knowledge': 1},
        'thick_skin': {'slot': 'skin', 'name': __('Thick skin'), 'might': 1, 'charisma': -1},
        'smooth_skin': {'slot': 'skin', 'name': __('Smooth skin'), 'might': -1, 'charisma': 1},
        'leery_eyes': {'slot': 'eyes', 'name': __('Leery eyes'), 'subtlety': 1},
        'firm_gaze': {'slot': 'eyes', 'name': __('Firm gaze'), 'might': 1},
        'bright_eyes': {'slot': 'eyes', 'name': __('Bright eyes'), 'charisma': 1},
        'enigmatic_gaze': {'slot': 'eyes', 'name': __('Enigmatic gaze'), 'knowledge': 1},
    }

    slavercaravan_alignment_features = {
        'gluttonous': {'slot': 'nutrition', 'name': __('Gluttonous'), 'charisma': 1},
        'temperate': {'slot': 'nutrition', 'name': __('Temperate'), 'knowledge': 1},
        'proud': {'slot': 'authority', 'name': __('Proud'), 'might': 1},
        'humble': {'slot': 'authority', 'name': __('Humble'), 'knowledge': 1},
        'slothful': {'slot': 'comfort', 'name': __('Slothful'), 'knowledge': 1},
        'diligent': {'slot': 'comfort', 'name': __('Diligent'), 'might': 1},
        'cruel': {'slot': 'communication', 'name': __('Cruel'), 'might': 1},
        'merciful': {'slot': 'communication', 'name': __('Merciful'), 'charisma': 1},
        'lustful': {'slot': 'eros', 'name': __('Lustful'), 'subtlety': 1},
        'chaste': {'slot': 'eros', 'name': __('Chaste'), 'knowledge': 1},
        'envious': {'slot': 'ambition', 'name': __('Envious'), 'subtlety': 1},
        'kind': {'slot': 'ambition', 'name': __('Kind'), 'charisma': 1},
        'greedy': {'slot': 'prosperity', 'name': __('Greedy'), 'knowledge': 1},
        'charitable': {'slot': 'prosperity', 'name': __('Charitable'), 'charisma': 1},
        'coward': {'slot': 'safety', 'name': __('Coward'), 'subtlety': 1},
        'zealous': {'slot': 'safety', 'name': __('Zealous'), 'might': 1},
    }

    slavercaravan_cities = {
        'market_city': {
            'description': __("City with market"), 'label': 'lbl_slavercaravan_market_city',
        },
        'brothel_city': {
            'description': __("City with brothel"), 'label': 'lbl_slavercaravan_brothel_city',
        },
        'amazon_village': {
            'description': __("Amazon village"), 'label': 'lbl_slavercaravan_amazon_village',
        },
        'sawmill_city':{
            'description': __("City with sawmill"), 'label': 'lbl_slavercaravan_sawmill_city',
        },
        'artisan_city': {
            'description': __("Artisans city"), 'label': 'lbl_slavercaravan_artisan_city', 
        },
        'rich_city': {
            'description': __("Rich city"), 'label': 'lbl_slavercaravan_rich_city',
        },
    }

    slavercaravan_locations = {
        'road': {
            'name': __('Road'), 'description': __("Road"), 'label': 'lbl_slavercaravan_road'
        },
        'wildness': {
            'name': __("Wildness"), 'description': __("Wildness"), 'label': 'lbl_slavercaravan_wildness'
        }
    }

    slavercaravan_city_names = ['Name1', 'Name2', 'Name3', 'Name4', 'Name5', 'Name6', 'Name7']

    slavercaravan_items = {
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