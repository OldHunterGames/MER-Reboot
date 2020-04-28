init python:
    mer_background_data = {
        'beggar': {
            'male': {
                'name': __('чумичка'),
                'description': __('Отверженная замарашка, она скиталась по миру, спала в грязи и выживала как могла.'),
            },
            'female': {
                'name': __('чумичка'),
                'description': __('Отверженная замарашка, она скиталась по миру, спала в грязи и выживала как могла.'),
            },
            'tier': 0,
            'type': 'useless',
        },

        'vargant': {
            'name': __('доходяга'),
            'prerequisites': [],
            'tier': 0,
            'type': 'useless',
            'description': __('Проведший большую часть жизни в лишениях и скитаниях, этот доходяга едва ли способен на физический труд.'),
        },

        'moron': {
            'name': __('раздолбай'),
            'prerequisites': [],
            'tier': 0,
            'type': 'useless',
            'description': __('Из за своей граничащей со слабоумием тупости, не имеет практически никаких полезных умений.'),
        },

        'commoner': {
            'name': __('обыватель'),
            'prerequisites': [],
            'tier': 1,
            'type': 'useless',
            'description': __('Ничем не примечательный обыватель.'),
        },

        'troglodyte': {
            'name': __('троглодит'),
            'prerequisites': [],
            'tier': 1,
            'type': 'matrial',
            'description': __('Ничем не прмечательный представитель дикого племени'),
        },

        'gatherer': {
            'name': __('собиратель'),
            'prerequisites': [],
            'tier': 1,
            'type': 'service',
            'description': __('Умеет собирает ядгоды, насекомых, коренья и фркты, искать воду, чинить одежду, готовить на костре.'),
        },

        'hearthkeeper': {
            'name': __('хранитель очага'),
            'prerequisites': [],
            'tier': 2,
            'type': 'service',
            'description': __('Отличается внимательностью и усидчивостью. Племя доверило ему поддерживать и охранять огонь.'),
        },

        'herbalist': {
            'name': __('травник'),
            'prerequisites': [],
            'tier': 3,
            'type': 'service',
            'description': __('Знает множество ценных съедобных и целебных трав что растут в диких местах.'),
        },

        'artisan': {
            'name': __('умелец'),
            'prerequisites': [],
            'tier': 3,
            'type': 'service',
            'description': __('Обладает большим опытом в ремесле и руоделии. Золотые руки.'),
        },

        'master': {
            'name': __('мастер'),
            'prerequisites': [],
            'tier': 3,
            'type': 'service',
            'description': __('Из под руки этого мастера выходят не просто ремесленные поделки а настоящие произведения искусства.'),
        },

        'brute': {
            'name': __('дикарь'),
            'prerequisites': [],
            'tier': 2,
            'type': 'matrial',
            'description': __('Сильный и ловкий первобытный охотник, настоящее воплощение брутальной дикости.'),
        },

        'ranger': {
            'name': __('следопыт'),
            'prerequisites': [],
            'tier': 3,
            'type': 'matrial',
            'description': __('Опытный следопыт, способный выследить и завалить любую дичь будь то зверь, человек или чудовище.'),
        },

        'warlord': {
            'name': __('атаман'),
            'prerequisites': [],
            'tier': 4,
            'type': 'matrial',
            'description': __('Отважный воин заправлявший целым отрядом лихих бойцов.'),
        },

        'hermit': {
            'name': __('отшельник'),
            'prerequisites': [],
            'tier': 1,
            'type': 'managing',
            'description': __('Долгое проживание вдали от общества даёт время на раздумия.'),
        },

        'storyteller': {
            'name': __('сказитель'),
            'prerequisites': [],
            'tier': 2,
            'type': 'managing',
            'description': __('В племенах не имеющих письменности, сказителей уважают за крепкую память.'),
        },

        'shaman': {
            'name': __('шаман'),
            'prerequisites': [],
            'tier': 3,
            'type': 'managing',
            'description': __('Шаманом племени может стать лишь самый умный в племени дикарей.'),
        },

        'mentor': {
            'name': __('наставник'),
            'prerequisites': [],
            'tier': 4,
            'type': 'managing',
            'description': __('Отличается редкой интеллектуальной одаренностью.'),
        },

        'philosopher': {
            'name': __('философ'),
            'prerequisites': [],
            'tier': 5,
            'type': 'managing',
            'description': __('Мыслитель опередивший своё время и прозревший многие тайны вселенной.'),
        },

        'slut': {
            'name': __('распутник'),
            'prerequisites': [],
            'tier': 1,
            'type': 'social',
            'description': __('Сексуальна раскрепощённость позволяет выживать даже в тех сообществах где денег ещё или уже не существует.'),
        },

        'whore': {
            'name': __('шлюха'),
            'prerequisites': [],
            'tier': 1,
            'type': 'social',
            'description': __('Выживать за счёт своей сексуальной доступности - древнейшая стратегия. И она неплохо работает.'),
        },

        'jester': {
            'name': __('шут'),
            'prerequisites': [],
            'tier': 2,
            'type': 'social',
            'description': __('Даже если над тобой все смеются и пинают, со стола сильных мира сего всегда можно собрать лушчие объедки.'),
        },

        'wisperer': {
            'name': __('интриган'),
            'prerequisites': [],
            'tier': 3,
            'type': 'social',
            'description': __('Знать всё и обо всех, значит обладать большим влиянием.'),
        },

        'cutey': {
            'name': __('очаровашка'),
            'prerequisites': [],
            'tier': 4,
            'type': 'social',
            'description': __('Имея приятную врешность и дружелюбную натуру можно неплохо жить за счёт доброты окружающих.'),
        },

        'chief': {
            'name': __('вождь племени'),
            'prerequisites': [],
            'tier': 5,
            'type': 'social',
            'description': __('Вождями становятся те кто лучше всех умеет решать внутренние конфликты и мотивировать людей.'),
        },

        'worker': {
            'name': __('работяга'),
            'tier': 1,
            'type': 'service',
            'description': __('Обычный работяга с завода, сильный но черезчур грубый и прямолинейный.'),
        },

        'soldier': {
            'name': __('солдат'),
            'prerequisites': [],
            'tier': 2,
            'type': 'martial',
            'description': __('Оцените эти мускулы! Отличное пушечное мясо для массовой армии своего мира, но и в рабы сгодится лучше некуда.'),
        },

        'commander': {
            'name': __('боевой командир'),
            'prerequisites': [],
            'tier': 3,
            'type': 'martial',
            'description': __('Ветеран войны, дослужившийся до звания офицера. Крепок телом, отличный тактик, способен вдохновляь людей. Разве что грубоват.'),
        },

        'hero': {
            'name': __('герой'),
            'prerequisites': [],
            'tier': 5,
            'type': 'matrial',
            'description': __('Легендарный воитель покрывший себя вечной славной на поле брани.'),
        },

        'idol': {
            'name': __('поп-идол'),
            'prerequisites': [],
            'tier': 4,
            'type': 'social',
            'description': __('Вы только поглядите на неё! Красивая, спортивная, артистичная. В совём мире она была настоящей звездой эстрады!'),
        },

        'nerd': {
            'name': __('задрот'),
            'prerequisites': [],
            'tier': 1,
            'type': 'managing',
            'description': __('Конечно он хиловат, но мозги варят что надо! Гик? Нерд? Как там называются яйцеголовые?'),
        },

        'muse': {
            'name': __('муза'),
            'prerequisites': ['female'],
            'tier': 1,
            'type': 'social',
            'description': __('Она так красива и в то же время так наивна и бесхитростна. Эта дама служила источником вдохновения для многих поэтов и художников.'),
        },

        'model': {
            'name': __('фотомодель'),
            'prerequisites': ['female'],
            'tier': 2,
            'type': 'social',
            'description': __('Это лицо так и просится на обложку журнала мод. Хоть кроме внешности она ничем не выделяется, но ей и этого хватит!'),
        },

        'atlete': {
            'name': __('атлет'),
            'prerequisites': ['male'],
            'tier': 2,
            'type': 'martial',
            'description': __('Спортсмен посветивший всю свою жизнь соврешенствованию собственного тела.'),
        },

        'fitgirl': {
            'name': __('фитнесс инструктор'),
            'prerequisites': ['female'],
            'tier': 3,
            'type': 'martial',
            'description': __('Она была успешным инструктором по карсоте и здоровью, и сама выделяется этими качествами.'),
        },

        'poet': {
            'name': __('поэт'),
            'prerequisites': ['male'],
            'tier': 3,
            'type': 'social',
            'description': __('Этот красивый и утончённый юноша не одно дамское сердце разбил своими стихами.'),
        },

        'vigilante': {
            'name': __('мститель в маске'),
            'prerequisites': ['male'],
            'tier': 4,
            'type': 'martial',
            'description': __('Этот ночной герой, сильный, ловкий и умный, хранил покой родного города не ожидая ни славы ни награды.'),
        },

        'opinion_leader': {
            'name': __('лидер мнений'),
            'prerequisites': [],
            'tier': 4,
            'type': 'social',
            'description': __('Уникальное сочетание красноречия, харизмы и знаний позволяли этой выдающейся личности достучаться до миллионов сердец в родном мире.'),
        },

    }