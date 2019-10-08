init python:
    new_sex_cards = {
        # positions
        'sit': {
            'name': __("Sit"),
            'description': __("Sit"),
            'conditions': [],
            'type': 'pose',
        },
        'stand_mirror': {
            'name': __("Stand infront of mirror"),
            'description': __("Stand infront of mirror"),
            'conditions': ['toys'],
            'type': 'pose',
        },
        'sit_mirror': {
            'name': __("Sit infront of mirror"),
            'description': __("Sit infront of mirror"),
            'conditions': ['toys'],
            'type': 'pose',
        },
        'lie_bed': {
            'name': __("Lie on a bed"),
            'description': __("Lie on a bed"),
            'conditions': [],
            'type': 'pose',
        },
        'on_knees': {
            'name': __("On knees"),
            'description': __("On knees"),
            'conditions': [],
            'type': 'pose',
        },
        'doggy_style': {
            'name': __("Doggy pose"),
            'description': __("Doggy pose"),
            'conditions': [],
            'type': 'pose',
        },
        # behaviors
        'sadly': {
            'name': __("Sadly"),
            'description': __("Sadly"),
            'conditions': [],
            'type': 'behavior',
        },
        'bashfully': {
            'name': __("Bashfully"),
            'description': __("Bashfully"),
            'conditions': [],
            'type': 'behavior',
        },
        'gently': {
            'name': __("Gently"),
            'description': __("Gently"),
            'conditions': [],
            'type': 'behavior',
        },
        # actions
        'undress': {
            'name': __("Undress"),
            'description': __("Undress"),
            'target_conditions': ['cloth'],
            'permanent_conditions': {
                'remove': ['cloth'],
                'add': [],
            },
            'type': 'action',
        },
        'speak': {
            'name': __("Speak"),
            'description': __("Speak"),
            'conditions': ['free_mouth'],
            'temporary_conditions': {
                'remove': ['free_mouth'],
                'add': [],
            },
            'type': 'action',
        },
        'blowjob': {
            'name': __("Blowjob"),
            'description': __("Blowjob"),
            'conditions': ['free_mouth'],
            'target_conditions': ['has_dick'],
            'temporary_conditions': {
                'remove': ['free_mouth'],
                'add': [],
            },
            'type': 'action',
        },

    }

    # example of multikey descriptions
    actions_descriptions = {
        frozenset(('blowjob', 'sadly', 'sit')): 'Suck while passively sitting',
        frozenset(('speak', 'sadly', 'sit')): 'Speak while sadly sitting',
    }