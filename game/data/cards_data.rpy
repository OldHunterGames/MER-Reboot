init python:
    def context_or_empty(context):
        return {} if context is None else context

    def class_tier_bonus(user, context):
        context = context_or_empty(context)
        return user.person_class.tier

    def soul_level_bonus(user, context):
        context = context_or_empty(context)
        return user.soul_level

    def best_attr_bonus(user, context):
        context = context_or_empty(context)
        attr = max(user.attributes().values())
        return attr

    def best_attr_suit(user, context):
        context = context_or_empty(context)
        attr = max(user.attributes().keys(), key=lambda x: user.attribute(x))
        suit = Suits.attribute_as_suit(attr)
        return suit
    
    def joker_power(user, context):
        context = context_or_empty(context)
        return 1 if context.get('isEnemy', False) else 5

    person_cards_data = {

        'betrayal': {
            'name': __("Предательство"),
            'suit': 'hearts',
            'custom': soul_level_bonus,
            'type': 'sabotage',
            'case': 'universal',
        },        
        'bravado': {
            'name': __("Дружба"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'tag': 'fellowship',
            'type': 'support',
            'case': 'universal',
        },        
        'cestus': {
            'name': __("Cestus"),
            'suit': 'spades',
            'attribute': 'might',
            'type': 'equipment',
            'case': 'combat',
        },
        'combat_expirience': {
            'name': __("Combat expirience"),
            'suit': 'spades',
            'custom': class_tier_bonus,
            'type': 'skill',
            'case': 'combat',
        },
        'deception': {
            'name': __("Обман"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'type': 'grove',
        },        
        'distracting_nudity': {
            'name': __("Distracting nudity"),
            'suit': 'spades',
            'attribute': 'charisma',
            'type': 'skill',
            'case': 'universal',
        },        
        'dual_strike': {
            'name': __("Dual strike"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'type': 'equipment',
            'case': 'combat',
        },        
        'evasive': {
            'name': __("Evasive"),
            'suit': 'spades',
            'value': 1,
            'type': 'skill',
            'case': 'combat',
        },     
        'exotic_weapon': {
            'name': __("Exotic weapon"),
            'suit': best_attr_suit,
            'custom': best_attr_bonus,
            'type': 'equipment',
            'case': 'combat',
        },        
        'far_reach': {
            'name': __("Far reach"),
            'suit': 'clubs',
            'attribute': 'subtlety',
            'type': 'equipment',
            'case': 'combat',
        },
        'half_armored': {
            'name': __("Half-armored"),
            'suit': 'diamonds',
            'value': 3,
            'type': 'equipment',
            'case': 'combat',
        },        
        'hide_cloth': {
            'name': __("Накидка из шкур"),
            'suit': 'diamonds',
            'value': 1,
            'type': 'equipment',
        },          
        'imposing_fear': {
            'name': __("Imposing fear"),
            'suit': 'hearts',
            'attribute': 'charisma',
            'type': 'skill',
            'case': 'combat',
        },        
        'champion': {
            'name': __("Champion"),
            'suit': 'joker',
            'custom': joker_power,
            'type': 'skill',
            'case': 'combat',
        },        
        'common_sense': {
            'name': __("Common sense"),
            'suit': 'skull',
            'attribute': 'knowledge',
            'type': 'skill',
        },        
        'knife': {
            'name': __("Knife"),
            'suit': 'spades',
            'value': 1,
            'type': 'equipment',
            'case': 'combat',
        },            
        'light_armor': {
            'name': __("Легкая броня"),
            'suit': 'diamonds',
            'value': 2,
            'type': 'equipment',
            'case': 'combat',
        },        
        'living_legend': {
            'name': __("Living legend"),
            'suit': 'joker',
            'custom': joker_power,
            'type': 'skill',
        },        
        'lucky': {
            'name': __("Хрень!"),
            'suit': 'diamonds',
            'custom': soul_level_bonus,
            'type': 'skill',
        },        
        'mobile_offence': {
            'name': __("Mobile offence"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'type': 'skill',
            'case': 'combat',
        },        
        'natural_charm': {
            'name': __("Natural charm"),
            'suit': 'skull',
            'attribute': 'charisma',
            'type': 'skill',
        },        
        'net': {
            'name': __("Net"),
            'suit': 'hearts',
            'attribute': 'subtlety',
            'type': 'equipment',
            'case': 'combat',
        },        
        'padded_armor': {
            'name': __("Padded armor"),
            'suit': 'diamonds',
            'attribute': 'might',
            'type': 'equipment',
        },        
        'pain_resilience': {
            'name': __("Pain resilience"),
            'suit': 'diamonds',
            'value': 1,
            'type': 'skill',
            'case': 'combat'
        },
        'public_approval': {
            'name': __("Public approval"),
            'suit': 'hearts',
            'attribute': 'charisma',
            'type': 'skill',
        },        
        'punch': {
            'name': __("Punch"),
            'suit': 'skull',
            'attribute': 'might',
            'type': 'skill',
        },
        'pyramid_helm': {
            'name': __("Pyramid helm"),
            'suit': 'clubs',
            'value': 3,
            'type': 'equipment',
            'case': 'combat',
        },         
        'satisfaction': {
            'name': __("Любовь"),
            'suit': 'hearts',
            'attribute': 'charisma',
            'type': 'skill',
        },
        'shared_wisdom': {
            'name': __("Shared wisdom"),
            'suit': 'clubs',
            'attribute': 'knowledge',
            'type': 'skill',
        },             
        'shield': {
            'name': __("Shield"),
            'suit': 'clubs',
            'attribute': 'might',
            'type': 'equipment',
            'case': 'combat',
        },        
        'sociable': {
            'name': __("Общительность"),
            'suit': 'hearts',
            'custom': class_tier_bonus,
            'type': 'skill',
        },        
        'slippery_skin': {
            'name': __("Slippery skin"),
            'suit': 'hearts',
            'value': 1,
            'type': 'skill',
            'case': 'combat',
        },
        'slippery_words': {
            'name': __("Slippery words"),
            'suit': 'skull',
            'attribute': 'subtlety',
            'type': 'skill',
        },        
        'smart_tactics': {
            'name': __("Умная тактика"),
            'suit': 'diamonds',
            'attribute': 'knowledge',
            'case': 'combat',
        },        
        'spear': {
            'name': __("Копьё"),
            'suit': 'clubs',
            'attribute': 'might',
            'type': 'equipment',
        },        
        'steel_whip': {
            'name': __("Steel whip"),
            'suit': 'spades',
            'attribute': 'subtlety',
            'type': 'equipment',
            'case': 'combat',
        },        
        'stone_knife': {
            'name': __("Каменный нож"),
            'suit': 'spades',
            'value': 1,
            'type': 'equipment',
            'case': 'combat',
        },        
        'struggle': {
            'name': __("Struggle"),
            'suit': 'skull',
            'attribute': 'might',
            'type': 'skill',
        },        
        'stubborn': {
            'name': __("Stubborn"),
            'suit': 'skull',
            'attribute': 'might',
            'type': 'skill',
        },        
        'subdual_weapon': {
            'name': __("Subdual weapon"),
            'suit': 'skull',
            'value': 5,
            'type': 'equipment',
            'case': 'combat',
        },        
        'sword': {
            'name': __("Sword"),
            'suit': 'spades',
            'attribute': 'might',
            'type': 'equipment',
            'case': 'combat',
        },        
        'tactical_advice': {
            'name': __("Умная тактика"),
            'suit': 'clubs',
            'custom': class_tier_bonus,
            'type': 'support',
            'case': 'combat',
        },        
        'trident': {
            'name': __("Trident"),
            'suit': 'clubs',
            'attribute': 'might',
            'type': 'equipment',
            'case': 'combat',
        },
        'two_handed_sword': {
            'name': __("Two-handed sword"),
            'suit': 'hearts',
            'attribute': 'might',
            'type': 'equipment',
            'case': 'combat',
        },        
        'wisdom_of_many_lives': {
            'name': __("Wisdom of many lives"),
            'suit': 'diamonds',
            'custom': soul_level_bonus,
            'type': 'skill',
        },        
        'wrestling': {
            'name': __("Wrestling"),
            'suit': 'skull',
            'attribute': 'might',
            'type': 'skill',
            'case': 'combat',
        },
        'whip_lash': {
            'name': __("Whip lash"),
            'suit': 'spades',
            'value': 1,
            'type': 'equipment',
        },

    }