init python:
    
    core_duel_suits_data = {
        'sword': {
            'name': __("Sword"),
            'action': 'drop_card',
            'beats': ['axe', 'heart'],
        },
        'axe': {
            'name': __("Axe"),
            'action': 'drop_card',
            'beats': ['shield', 'heart'],
        },
        'heart': {
            'name': __("Heart"),
            'action': 'get_card',
            'beats': ['shield', 'leg'],
        },
        'leg': {
            'name': __("Leg"),
            'action': 'get_card',
            'beats': ['axe', 'sword'],
        },
        'shield': {
            'name': __("Shield"),
            'action': 'get_card',
            'beats': ['sword', 'leg'],
        },
    }
