init python:
    new_sex_cards = {
        # positions
        'sit': {
            'name': __("Sit"),
            'description': __("Sit"),
            'childs': ['face_fuck'],
        },
        'face_fuck': {
            'name': __("Face fuck"),
            'suit': 'diamonds',
            'description': __("Face fuck"),
        },
    }

    # example of multikey descriptions
    sex_descriptions = {
        frozenset(('blowjob', 'sadly', 'sit')): 'Suck while passively sitting',
        frozenset(('speak', 'sadly', 'sit')): 'Speak while sadly sitting',
    }