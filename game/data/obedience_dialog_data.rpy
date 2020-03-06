init python:
    natures_phrases = {
        'choleric': [
            __('Choleric'),
        ],
        'sanguine': [
            __('Sanguine'),
        ],
        'phlegmatic': [
            __('Phlegmatic'),
        ],
        'melancholic': [
            __('Melancholic'),
        ]
    }

    natures_phrases_plus = {
        'choleric': [
            __('Choleric+'),
        ],
        'sanguine': [
            __('Sanguine+'),
        ],
        'phlegmatic': [
            __('Phlegmatic+'),
        ],
        'melancholic': [
            __('Melancholic+'),
        ]
    }

    natures_good_reactions = {
        'choleric': [
            __('Choleric good'),
        ],
        'sanguine': [
            __('Sanguine good'),
        ],
        'phlegmatic': [
            __('Phlegmatic good'),
        ],
        'melancholic': [
            __('Melancholic good'),
        ]
    }

    # In this dictionary first key is person's nature, inner keys for selected action
    natures_bad_reactions = {
        'choleric': [
            {
                'sanguine': [
                    __('Choleric person-sanguine choice: bad'),
                ],
                'phlegmatic': [
                    __('Choleric person-phlegmatic choice: bad'),
                ],
                'melancholic': [
                    __('Choleric person-melancholic choice: bad'),
                ]
            }
        ],
        'sanguine': {
                'choleric': [
                    __('Sanguine person-choleric choice: bad'),
                ],
                'phlegmatic': [
                    __('Sanguine person-phlegmatic choice: bad'),
                ],
                'melancholic': [
                    __('Sanguine person-melancholic choice: bad'),
                ]
        },
        'phlegmatic': {
                'choleric': [
                    __('Phlegmatic person-choleric choice: bad'),
                ],
                'sanguine': [
                    __('Phlegmatic person-sanguine choice: bad'),
                ],
                'melancholic': [
                    __('Phlegmatic person-melancholic choice: bad'),
                ]
        },
        'melancholic': {
                'choleric': [
                    __('Melancholic person-choleric choice: bad'),
                ],
                'sanguine': [
                    __('Melancholic person-sanguine choice: bad'),
                ],
                'phlegmatic': [
                    __('Melancholic person-phlegmatic choice: bad'),
                ]
        }
    }

    control_strategy_phrases = {
        'chantage': [
            __('chantage'),
        ],
        'bribe': [
            __('bribe'),
        ],
        'seduction': [
            __('seduction'),
        ],
        'reason': [
            __('reason'),
        ],
        'torture': [
            __('torture'),
        ],
        'deprivation': [
            __('deprivation'),
        ],
        'humiliation': [
            __('humiliation'),
        ],
        'discipline': [
            __('discipline'),
        ],
    }

    obedience_starting_text_data = {
        'choleric': [
            __('Choleric'),
        ],
        'sanguine': [
            __('Sanguine'),
        ],
        'phlegmatic': [
            __('Phlegmatic'),
        ],
        'melancholic': [
            __('Melancholic')
        ]
    }