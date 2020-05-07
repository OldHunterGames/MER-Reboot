init python:
    mer_background_data = {

    # БЕСПОЛЕЗНЫЕ
        'beggar': {
            'male': {
                'name': __('попрошайка'),
                'description': __('Проведший большую часть жизни в лишениях и скитаниях, этот доходяга едва ли способен на физический труд.'),
            },
            'female': {
                'name': __('попрошайка'),
                'description': __('Отверженная замарашка, она скиталась по миру, спала в грязи и выживала как могла.'),
            },
            'tier': 0,
            'type': 'useless',
        },

        'moron': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('раздолбай'),
            'prerequisites': [],
            'tier': 0,
            'type': 'useless',
            'description': __('Из за своей граничащей со слабоумием тупости, не имеет практически никаких полезных умений.'),
        },

        'commoner': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('обыватель'),
            'prerequisites': [],
            'tier': 1,
            'type': 'useless',
            'description': __('Ничем не примечательный обыватель.'),
        },

    # MARTIAL

        'troglodyte': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('троглодит'),
            'prerequisites': [],
            'tier': 1,
            'type': 'matrial',
            'description': __('Ничем не прмечательный представитель дикого племени'),
        },

        'brute': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('дикарь'),
            'prerequisites': [],
            'tier': 2,
            'type': 'matrial',
            'description': __('Сильный и ловкий первобытный охотник, настоящее воплощение брутальной дикости.'),
        },

        'soldier': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('солдат'),
            'prerequisites': [],
            'tier': 2,
            'type': 'martial',
            'description': __('Оцените эти мускулы! Отличное пушечное мясо для массовой армии своего мира, но и в рабы сгодится лучше некуда.'),
        },

        'atlete': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('атлет'),
            'prerequisites': ['male'],
            'tier': 2,
            'type': 'martial',
            'description': __('Спортсмен посветивший всю свою жизнь соврешенствованию собственного тела.'),
        },

        'ranger': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('следопыт'),
            'prerequisites': [],
            'tier': 3,
            'type': 'matrial',
            'description': __('Опытный следопыт, способный выследить и завалить любую дичь будь то зверь, человек или чудовище.'),
        },

        'fitgirl': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('фитнесс инструктор'),
            'prerequisites': ['female'],
            'tier': 3,
            'type': 'martial',
            'description': __('Она была успешным инструктором по карсоте и здоровью, и сама выделяется этими качествами.'),
        },

        'commander': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('боевой командир'),
            'prerequisites': [],
            'tier': 3,
            'type': 'martial',
            'description': __('Ветеран войны, дослужившийся до звания офицера. Крепок телом, отличный тактик, способен вдохновляь людей. Разве что грубоват.'),
        },

        'vigilante': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('мститель в маске'),
            'prerequisites': ['male'],
            'tier': 4,
            'type': 'martial',
            'description': __('Этот ночной герой, сильный, ловкий и умный, хранил покой родного города не ожидая ни славы ни награды.'),
        },

        'hero': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('герой'),
            'prerequisites': [],
            'tier': 5,
            'type': 'matrial',
            'description': __('Легендарный воитель покрывший себя вечной славной на поле брани.'),
        },

        'warlord': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('атаман'),
            'prerequisites': [],
            'tier': 4,
            'type': 'matrial',
            'description': __('Отважный воин заправлявший целым отрядом лихих бойцов.'),
        },

    # SETVICE
        'gatherer': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('собиратель'),
            'prerequisites': [],
            'tier': 1,
            'type': 'service',
            'description': __('Умеет собирает ядгоды, насекомых, коренья и фркты, искать воду, чинить одежду, готовить на костре.'),
        },

        'worker': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('работяга'),
            'tier': 1,
            'type': 'service',
            'description': __('Обычный работяга с завода, сильный но черезчур грубый и прямолинейный.'),
        },

        'hearthkeeper': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('хранитель очага'),
            'prerequisites': [],
            'tier': 2,
            'type': 'service',
            'description': __('Отличается внимательностью и усидчивостью. Племя доверило ему поддерживать и охранять огонь.'),
        },

        'herbalist': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('травник'),
            'prerequisites': [],
            'tier': 3,
            'type': 'service',
            'description': __('Знает множество ценных съедобных и целебных трав что растут в диких местах.'),
        },

        'artisan': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('умелец'),
            'prerequisites': [],
            'tier': 3,
            'type': 'service',
            'description': __('Обладает большим опытом в ремесле и руоделии. Золотые руки.'),
        },

        'master': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('мастер'),
            'prerequisites': [],
            'tier': 3,
            'type': 'service',
            'description': __('Из под руки этого мастера выходят не просто ремесленные поделки а настоящие произведения искусства.'),
        },

    # MANAGING

        'hermit': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('отшельник'),
            'prerequisites': [],
            'tier': 1,
            'type': 'managing',
            'description': __('Долгое проживание вдали от общества даёт время на раздумия.'),
        },

        'nerd': {
            'name': __('задрот'),
            'prerequisites': [],
            'tier': 1,
            'type': 'managing',
            'description': __('Конечно он хиловат, но мозги варят что надо! Гик? Нерд? Как там называются яйцеголовые?'),
        },

        'storyteller': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('сказитель'),
            'prerequisites': [],
            'tier': 2,
            'type': 'managing',
            'description': __('В племенах не имеющих письменности, сказителей уважают за крепкую память.'),
        },

        'shaman': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('шаман'),
            'prerequisites': [],
            'tier': 3,
            'type': 'managing',
            'description': __('Шаманом племени может стать лишь самый умный в племени дикарей.'),
        },

        'mentor': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('наставник'),
            'prerequisites': [],
            'tier': 4,
            'type': 'managing',
            'description': __('Отличается редкой интеллектуальной одаренностью.'),
        },

        'philosopher': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('философ'),
            'prerequisites': [],
            'tier': 5,
            'type': 'managing',
            'description': __('Мыслитель опередивший своё время и прозревший многие тайны вселенной.'),
        },

    # SOCIAL

        'slut': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('распутник'),
            'prerequisites': [],
            'tier': 1,
            'type': 'social',
            'description': __('Сексуальна раскрепощённость позволяет выживать даже в тех сообществах где денег ещё или уже не существует.'),
        },

        'whore': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('шлюха'),
            'prerequisites': [],
            'tier': 1,
            'type': 'social',
            'description': __('Выживать за счёт своей сексуальной доступности - древнейшая стратегия. И она неплохо работает.'),
        },

        'muse': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('муза'),
            'prerequisites': ['female'],
            'tier': 1,
            'type': 'social',
            'description': __('Она так красива и в то же время так наивна и бесхитростна. Эта дама служила источником вдохновения для многих поэтов и художников.'),
        },

        'model': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('фотомодель'),
            'prerequisites': ['female'],
            'tier': 2,
            'type': 'social',
            'description': __('Это лицо так и просится на обложку журнала мод. Хоть кроме внешности она ничем не выделяется, но ей и этого хватит!'),
        },

        'jester': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('шут'),
            'prerequisites': [],
            'tier': 2,
            'type': 'social',
            'description': __('Даже если над тобой все смеются и пинают, со стола сильных мира сего всегда можно собрать лушчие объедки.'),
        },

        'wisperer': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('интриган'),
            'prerequisites': [],
            'tier': 3,
            'type': 'social',
            'description': __('Знать всё и обо всех, значит обладать большим влиянием.'),
        },

        'poet': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('поэт'),
            'prerequisites': ['male'],
            'tier': 3,
            'type': 'social',
            'description': __('Этот красивый и утончённый юноша не одно дамское сердце разбил своими стихами.'),
        },

        'cutey': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('очаровашка'),
            'prerequisites': [],
            'tier': 4,
            'type': 'social',
            'description': __('Имея приятную врешность и дружелюбную натуру можно неплохо жить за счёт доброты окружающих.'),
        },

        'opinion_leader': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('лидер мнений'),
            'prerequisites': [],
            'tier': 4,
            'type': 'social',
            'description': __('Уникальное сочетание красноречия, харизмы и знаний позволяли этой выдающейся личности достучаться до миллионов сердец в родном мире.'),
        },

        'idol': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('поп-идол'),
            'prerequisites': [],
            'tier': 4,
            'type': 'social',
            'description': __('Вы только поглядите на неё! Красивая, спортивная, артистичная. В совём мире она была настоящей звездой эстрады!'),
        },

        'chief': {
            'male': {
                'name': __(''),
                'description': __('.'),
            },
            'female': {
                'name': __(''),
                'description': __('.'),
            },
            'name': __('вождь племени'),
            'prerequisites': [],
            'tier': 5,
            'type': 'social',
            'description': __('Вождями становятся те кто лучше всех умеет решать внутренние конфликты и мотивировать людей.'),
        },

    }