init python:
    mer_class_data = {
        'omega': {
            'name': __('Omega'),
            'description': __('A pity to watch... useless.'),
            'available_garments': ['cloth'],
            'type': 'slave',
            'tier': 0,
        },
        'sex_slave': {
            'name': __('Sex slave'),
            'tier': 1,
            'type': 'slave',
            'description': __('Slave with a very basic training, suited for plain sexual relief and uncomplicated chores'),
            'available_garments': ['cloth'],
            'tag': 'starter'
        },
        'menial_slave': {
            'name': __('Menial slave'),
            'tier': 1,
            'type': 'slave',
            'description': __('Generic slave trained for uncomplicated physical labor'),
            'available_garments': ['cloth'],
            'tag': 'starter'
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
            'tag': 'gladiator',
            'cost': 0
        },
        'andabant': {
            'name': __('Andabant'),
            'tier': 3,
            'key_attributes': ['charisma'],
            'prerequisites': {
                'class': ['pugilist', 'lucator']
            },
            'type': 'slave',
            'description': __('Andabants are fighting for most spectacular show, using brutal metal whips and blindfolded helmets protecting only their faces but nothing more. Gruesome yet not lethal combat. Andabant bodies are covered in multiple scars, but faces are cute - some weirdos find this attractive. Traditional punishment for the looser is rape - either by a winner or by the public.'),
            'available_garments': ['cloth'],
            'attack_suits': ['hearts'],
            'attack_types': ['melee'],
            'tag': 'gladiator',
            'cost': 5,
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
            'tag': 'gladiator',
            'cost': 10,
        },
        'pugilist': {
            'name': __('Pugilist'),
            'key_attributes': ['might'],
            'tier': 2,
            'type': 'slave',
            'prerequisites': {
                'type': 'slave'
            },
            'description': __("This gladiator is trained for non lethal unarmed combat. Often it's just a first step to become a more brutal cestus gladiator."),
            'available_garments': ['cloth'],
            'tag': 'gladiator',
            'cost': 0,
        },
        'cestus': {
            'name': __('Cestus'),
            'key_attributes': ['might'],
            'tier': 3,
            'type': 'slave',
            'prerequisites': {
                'class': ['pugilist']
            },
            'description': __("Despite fighting with no actual weapon, cestus is a true martial fighter utilizing a metal plated gauntlets or knuckles adorned wit a menacing spikes, serated blades etc"),
            'available_garments': ['cloth'],
            'attack_suits': ['spades'],
            'tag': 'gladiator',
            'cost': 5,
        },
        'pegniarius': {
            'name': __('Pegniarius'),
            'key_attributes': ['might'],
            'tier': 2,
            'type': 'slave',
            'prerequisites': {
                'type': 'slave'
            },
            'description': __("This gladiator in training have some potential but not ready for a mortal combat yet. Pegniarii can spar with a blunt weapons in between a real matches on the arena, to heathen up the public."),
            'available_garments': ['armor'],
            'attack_suits': ['hearts'],
            'tag': 'gladiator',
            'cost': 5
        },
        'dimacheros': {
            'name': __('Dimacheros'),
            'key_attributes': ['might'],
            'tier': 4,
            'type': 'slave',
            'prerequisites': {
                'class': ['myrmidon']
            },
            'description': __("Dual wielding, lightly armored gladiator."),
            'available_garments': ['armor'],
            'attack_suits': ['spades'],
            'tag': 'gladiator',
            'cost': 10
        },
        'retiarius': {
            'name': __('Retiarius'),
            'key_attributes': ['might'],
            'tier': 3,
            'type': 'slave',
            'prerequisites': {
                'class': ['pegniarius']
            },
            'description': __("Fast moving unarmored gladiator, armed with a net, trident and a knife."),
            'available_garments': ['cloth'],
            'attack_suits': ['spades', 'clubs'],
            'tag': 'gladiator',
            'cost': 10,
        },
        'secutor': {
            'name': __('Secutor'),
            'key_attributes': ['might'],
            'tier': 4,
            'type': 'slave',
            'prerequisites': {
                    'class': ['myrmidon'],
                    'gender': 'male'
            },
            'description': __("This menacing pyramid-helmed man with a heavy two-handed sword is beloved by public and feared by peers."),
            'available_garments': ['cloth'],
            'attack_suits': ['diamonds'],
            'tag': 'gladiator',
            'cost': 20,
        },
            
        'goplynia': {
            'name': __('Goplynia'),
            'key_attributes': ['might'],
            'tier': 4,
            'type': 'slave',
            'prerequisites': {
                'class': ['myrmidon', 'andabant'],
                'gender': 'not male'
            },
            'description': __("This gladiatrix have heavy armored arms and legs but bare torso to please audience and make combat dangerous. Armed with a metal whips they are ready to trash anyone."),
            'available_garments': ['heavy_armor'],
            'attack_suits': ['hearts'],
            'tag': 'gladiator',
            'cost': 20
        },
        'cenobite': {
            'name': __('Cenobite'),
            'key_attributes': ['might'],
            'tier': 4,
            'type': 'slave',
            'prerequisites': {
                'class': ['retiarius', 'andabant'],
            },
            'description': __("Cenobites are most cruel sado-mazo gladiators of Eternal Rome. They trading protective armor for explicit and self-harmful piercing, tattoos, scarification and BDSM iron or leather wearings. They use any type of weapon given it have a most menacing and scary appearance."),
            'available_garments': ['cloth'],
            'attack_suits': ['hearts', 'spades', 'clubs'],
            'tag': 'gladiator',
            'cost': 15
        },

        'infamous_lanista': {
            'name': __('Infamous lanista'),
            'key_attributes': ['knowledge'],
            'tier': 1,
            'type': 'civil',
            'description': __(""),
            'available_garments': ['attire'],
            'attack_suits': ['diamonds',],
            'attack_types': ['magitech'],
            'tag': 'lanista'
        },

        'marginal_lanista': {
            'name': __('Marginal lanista'),
            'key_attributes': ['knowledge'],
            'tier': 2,
            'type': 'civil',
            'prerequisites': {
                'class': ['infamous_lanista'],
            },
            'description': __(""),
            'available_garments': ['attire'],
            'attack_suits': ['diamonds',],
            'attack_types': ['magitech'],
            'tag': 'lanista'
        },

        'mediocre_lanista': {
            'name': __('Mediocre lanista'),
            'key_attributes': ['knowledge'],
            'tier': 3,
            'type': 'civil',
            'prerequisites': {
                'class': ['marginal_lanista'],
            },
            'description': __(""),
            'available_garments': ['attire'],
            'attack_suits': ['diamonds',],
            'attack_types': ['magitech'],
            'tag': 'lanista'
        },

        'popular_lanista': {
            'name': __('Popular lanista'),
            'key_attributes': ['knowledge'],
            'tier': 4,
            'prerequisites': {
                'class': ['mediocre_lanista'],
            },
            'type': 'civil',
            'description': __(""),
            'available_garments': ['attire'],
            'attack_suits': ['diamonds',],
            'attack_types': ['magitech'],
            'tag': 'lanista'
        },

        'famous_lanista': {
            'name': __('Famous lanista'),
            'key_attributes': ['knowledge'],
            'tier': 5,
            'prerequisites': {
                'class': ['popular_lanista'],
            },
            'type': 'civil',
            'description': __(""),
            'available_garments': ['attire'],
            'attack_suits': ['diamonds',],
            'attack_types': ['magitech'],
            'tag': 'lanista'
        },
    }