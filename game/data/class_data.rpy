init python:
    mer_class_data = {
        'omega': {
            'name': __('Omega'),
            'description': __('A pity to watch... useless.'),
            'available_garments': ['cloth'],
            'type': 'slave',
            'tier': 0,
        },
        'lucator': {
            'name': __('Lucator'),
            'tier': 2,
            'key_attributes': ['charisma'],
            'prerequisites': {
                'type': 'slave'
            },
            'type': 'slave',
            'description': __('This specific type of gladiator is supposed to wrestle in mud, jelly or oil for a spectators fun. This wrestling is not particularly dangerous, so a beauty is more important than a physical fitness.'),
            'available_garments': ['cloth'],
            'tag': 'gladiator'
        },
        'andabant': {
            'name': __('Andabant'),
            'tier': 3,
            'key_attributes': ['charisma'],
            'prerequisites': {
                'class': ['pugilist', 'lucator']
            },
            'type': 'slave',
            'description': __('This specific type of gladiator is supposed to wrestle in mud, jelly or oil for a spectators fun. This wrestling is not particularly dangerous, so a beauty is more important than a physical fitness.'),
            'available_garments': ['cloth'],
            'attack_suits': ['hearts'],
            'attack_types': ['melee'],
            'tag': 'gladiator'
        },
        'myrmidon': {
            'name': __('Myrmidon'),
            'tier': 3,
            'key_attributes': ['might'],
            'prerequisites': {
                'class': ['pegniarius']
            },
            'type': 'slave',
            'description': __('Classic sword & shield wielding, lightly armored gladiator.'),
            'available_garments': ['armor'],
            'attack_suits': ['spades'],
            'attack_types': ['melee'],
            'tag': 'gladiator'
        },
        # 'pugilist': {
        #     'name': __('Pugilist'),
        #     'key_attributes': ['might'],
        #     'type': 'slave',
        #     'prerequisites': {
        #         'type': 'slave'
        #     },
        #     'description': __("This gladiator is trained for non lethal unarmed combat. Often it's just a first step to become a more brutal cestus gladiator."),
        #     'available_garments': ['cloth'],
        #     'attack_suits': ['stubborn'],
        #     'tag': 'gladiator'
        # },
        # 'cestus': {
        #     'name': __('Cestus'),
        #     'key_attributes': ['might'],
        #     'type': 'slave',
        #     'prerequisites': {
        #         'class': 'pugilist'
        #     }
        #     'description': __("This gladiator is trained for non lethal unarmed combat. Often it's just a first step to become a more brutal cestus gladiator."),
        #     'available_garments': ['cloth'],
        #     'attack_suits': ['stubborn'],
        #     'tag': 'gladiator'
        # },
    }