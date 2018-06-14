init python:
    
    core_duel_suits_data = {
        'sword': {
            'name': __("Sword"),
            'action': 'drop_card',
            'beats': ['axe', 'heart'],
            'attribute': 'subtlety',
        },
        'axe': {
            'name': __("Axe"),
            'action': 'drop_card',
            'beats': ['shield', 'heart'],
            'attribute': 'might',
        },
        'heart': {
            'name': __("Heart"),
            'action': 'get_card',
            'beats': ['shield', 'leg'],
            'attribute': 'charisma',
        },
        'leg': {
            'name': __("Leg"),
            'action': 'get_card',
            'beats': ['axe', 'sword'],
            'attribute': 'competence',
        },
        'shield': {
            'name': __("Shield"),
            'action': 'get_card',
            'beats': ['sword', 'leg'],
            'attribute': 'might',
        },

        'skull': {
            'name': __("Skull"),
            'action': 'no_action',
            'beats': [],
            'attribute': None,
        },
    }
