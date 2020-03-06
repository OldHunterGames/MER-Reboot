init python:
    quirks_data = {
        'caring': {
            'name': __('Caring'),
            'good_strategy': ControlStrategy.chantage,
            'bad_strategy': ControlStrategy.bribe,
            'good_reactions': [__('Good caring reaction')],
            'bad_reactions': [__('Bad caring reaction')],
        },
        'sadistic': {
            'name': __('Sadistic'),
            'good_strategy': ControlStrategy.bribe,
            'bad_strategy': ControlStrategy.chantage,
            'good_reactions': [__('Good sadistic reaction')],
            'bad_reactions': [__('Bad sadistic reaction')],
        },
        'lewd': {
            'name': __('Lewd'),
            'good_strategy': ControlStrategy.seduction,
            'bad_strategy': ControlStrategy.reason,
            'good_reactions': [__('Good lewd reaction')],
            'bad_reactions': [__('Bad lewd reaction')],
        },
        'passionate': {
            'name': __('Passionate'),
            'good_strategy': ControlStrategy.reason,
            'bad_strategy': ControlStrategy.seduction,
            'good_reactions': [__('Good passionate reaction')],
            'bad_reactions': [__('Bad passionate reaction')],
        },
        'delicate': {
            'name': __('Delicate'),
            'good_strategy': ControlStrategy.torture,
            'bad_strategy': ControlStrategy.deprivation,
            'good_reactions': [__('Good delicate reaction')],
            'bad_reactions': [__('Bad delicate reaction')],
        },
        'masochistic': {
            'name': __('Masochistic'),
            'good_strategy': ControlStrategy.deprivation,
            'bad_strategy': ControlStrategy.torture,
            'good_reactions': [__('Good masochistic reaction')],
            'bad_reactions': [__('Bad masochistic reaction')],
        },
        'narcissistic': {
            'name': __('Narcissistic'),
            'good_strategy': ControlStrategy.humiliation,
            'bad_strategy': ControlStrategy.discipline,
            'good_reactions': [__('Good narcissistic reaction')],
            'bad_reactions': [__('Bad narcissistic reaction')],
        },
        'submissive': {
            'name': __('Submissive'),
            'good_strategy': ControlStrategy.discipline,
            'bad_strategy': ControlStrategy.humiliation,
            'good_reactions': [__('Good submissive reaction')],
            'bad_reactions': [__('Bad submissive reaction')],
        },

    }