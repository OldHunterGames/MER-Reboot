init python:
    quirks_data = {
        'caring': {
            'name': __('Caring'),
            'good_strategy': ControlStrategy.chantage,
            'bad_strategy': ControlStrategy.bribe,
        },
        'sadistic': {
            'name': __('Sadistic'),
            'good_strategy': ControlStrategy.bribe,
            'bad_strategy': ControlStrategy.chantage,
        },
        'lewd': {
            'name': __('Lewd'),
            'good_strategy': ControlStrategy.seduction,
            'bad_strategy': ControlStrategy.reason,
        },
        'passionate': {
            'name': __('Passionate'),
            'good_strategy': ControlStrategy.reason,
            'bad_strategy': ControlStrategy.seduction,
        },
        'delicate': {
            'name': __('Delicate'),
            'good_strategy': ControlStrategy.torture,
            'bad_strategy': ControlStrategy.deprivation,
        },
        'masochistic': {
            'name': __('Masochistic'),
            'good_strategy': ControlStrategy.deprivation,
            'bad_strategy': ControlStrategy.torture,
        },
        'narcissistic': {
            'name': __('Narcissistic'),
            'good_strategy': ControlStrategy.humiliation,
            'bad_strategy': ControlStrategy.discipline,
        },
        'submissive': {
            'name': __('Submissive'),
            'good_strategy': ControlStrategy.discipline,
            'bad_strategy': ControlStrategy.humiliation,
        },

    }