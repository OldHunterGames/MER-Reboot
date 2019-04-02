init python:
    
    def plate_armor_calc(context):
        attack_type = context.get('suit', None)
        if attack_type == 'spades' or attack_type == 'clubs':
            return 1
        elif attack_Type == 'diamonds':
            return -1
        return 0

    mer_armor = {
        'nude': {
            'name': __('Nude'),
            'calc_bonus': lambda x: -1
        },
        'casual_clothes': {
            'name': __('Casual clothes'),
            'calc_bonus': lambda x: -1 if x.get('standoff_type', None) == 'combat' else 0
        },
        'combat_armor': {
            'name': __('Combat armor'),
            'calc_bonus': lambda x: -1 if x.get('standoff_type', None) == 'social' else 0
        },
        'plate_armor': {
            'name': __('Plate armor'),
            'calc_bonus': plate_armor_calc
        },
    }