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