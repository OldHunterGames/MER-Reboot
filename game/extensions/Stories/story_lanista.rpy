init python:
    tabernintro = False
    lupaintro = False
    colintro = False

label lbl_storylanista_start:
    $ player.set_avatar('images/avatar/special/player.png')
    $ player.firstname = 'Хозяин'
    $ SerPri = PersonCreator.gen_person()
    $ SerPri.set_avatar('images/avatar/special/princeps_serpis.png')
    $ SerPri.firstname = 'Принцепс дома Серпис'
    $ phoenix = PersonCreator.gen_person()
    $ phoenix.set_avatar('images/avatar/special/phoenix.png')
    $ phoenix.firstname = '???'
    $ barmaid = PersonCreator.gen_person()
    $ barmaid.set_avatar('images/avatar/special/barmaid.png')
    $ barmaid.firstname = 'Официантка'
    $ lanista = PersonCreator.gen_person()
    $ lanista.set_avatar('images/avatar/special/lanista.png')
    $ lanista.firstname = 'Ланиста Ликурий'
    $ glad1 = PersonCreator.gen_person()
    $ glad1.set_avatar('images/avatar/special/glad1.png')
    $ glad1.firstname = 'Пьяный гладиатор'
    $ glad2 = PersonCreator.gen_person()
    $ glad2.set_avatar('images/avatar/special/glad2.png')
    $ glad2.firstname = 'Чемпион Ярус'
    $ redsonya = PersonCreator.gen_person()
    $ redsonya.set_avatar('images/avatar/special/redsonya.png')
    $ redsonya.firstname = 'Рыжая Соня'
    $ barman = PersonCreator.gen_person()
    $ barman.set_avatar('images/avatar/special/bartender.png')
    $ barman.firstname = 'Хозяин Таверны'
    $ slaver = PersonCreator.gen_person()
    $ slaver.set_avatar('images/avatar/special/slaver.png')
    $ slaver.firstname = 'Работорговец'
    $ bmaman = PersonCreator.gen_person()
    $ bmaman.set_avatar('images/avatar/special/bmaman.png')
    $ bmaman.firstname = 'Мадам'

    show expression "images/bg/serpis_temple.jpg" as bg
    menu:
        'Начать пролог':
            pass
        'Пропустить пролог':
            $ phoenix.firstname = 'Ангел'
            return

    SerPri "Данной мне властью, возжигаю эту инсигнию в твоей душе и связую её с магистрами Дома."
    SerPri "Поднимись, пэр Дома Серпис и отыне не склоняй колен ни пред кем."
    'Я встал и отошел прочь, чтобы дать место следующему участнику ритуала. После кризиса черной седьмицы, в Доме Серпис сгорело много инсигний и сейчас либертины у которых было за душой хотя бы немного Искр спешили воспользоваться шансом чтобы получить полноценное гражданство.'
    'Всего минуту назад я был одним из таких либертинов. Благодаря критическому положению Дома, мне удалось не только оплатить стоимость начертания инсигнии но и сохранить для себя сотню Искр, для начала новой жизни.'

    player "Черт, жжётся"

    'У вас когда-нибудь горела душа? Это очень странное чувство и слова которые я использую чтобы его описать конечно не точны. Но я чувствую знак Дома Серпис на своей душе как узор из огня и Искры как маленькие шекочущие мурашки.'
    'Раньше мне приходилось хранить их в кристалле, но с инсигнией я могу впитать Искры прямо в свою душу. Могу чувстовать её. Говорят дискомфорт скоро пройдёт и я привыкну.'
    'Мне больше нечего делать в соборе. Я пошел прочь к дверям.'

    scene expression 'images/bg/vatican.png'

    phoenix "..."

    'Прямо за мной, на неприлично близком расстоянии идёт блондинка в длинных белых одеждах.'

    menu:
        "Спросить":
            player "Привет. Мы знакомы?"
            phoenix "Эээээй! Вот сейчас было обидно... Я же твой ангел-хранитель. Я тебя ещё вот такусеньким знала"
            'Девушка показывает пальцами крохотный промежуток'
            $ phoenix.firstname = 'Ангел'
            player "Эмбрионом чтоли?!"
            phoenix "Тада! Конечно. Душа появляется в теле в момент зачатия."
            player "Но я то тебя никогда не видел"
            phoenix "Ага-ага. Я же была тенью. Люди обычно не видят нас. Да и слышат плоховато. Ты например ЧАААААСТО вёл себя плохо и не слушал меня."
            player "Да как я мог тебя слушать?"
            phoenix "Это то чувство в душе когда ты знаешь что что-то не так. И голос совести..."
            player "А теперь ты будешь всё это мне кричать прямо в ухо? Ещё чего не хватало."
            phoenix "Когда ты получил инсигнию, я стала фениксом! Но видеть и слышать меня это твой выбор, меня всегда можно игнорировать. Все постоянно нас игнорируют..."
            player "О! Надо попробовать."
            phoenix "Стой-стой-стой! Я тебе пригожусь."
            player "Это как?"
            phoenix "Я связана со всеми фениксами Дома, поэтому смогу давать тебе важную информацию о происходящем."
            phoenix "И ещё я могу видеть невидимое"
            phoenix "А главное я всегда знаю что хорошо и что плохо и буду наставлять тебя на пути праведности! ТАДА ^_^"
            player "Вот это меня как раз и смущает..."
            player "Но я дам тебе шанс. Дай мне мудрый совет. У меня есть 100 искр и я не хочу пахать как серф, на дядю. Чем мне заняться?"
            phoenix "Первым делом сними жильё! На первое время тебе хватит. И что бы ты не далал, надо будт добыть рабов - без рабов своего бизнеса не поднимешь."
            phoenix "Пяти искр в день хватит на себя и ещё по пять придётся отдать за содержание каждого раба. Так что будь внимателен, не прогори."
            phoenix "А вот что именно тебе делать чтобы заработать искры... даже не знаю. Что ты умеешь?"
            player "Я умею веселиться! "
            phoenix 'Пфф...'
            player 'Знаю! Надо пойти в таверну обмыть моё гражданство. Там и разберёмся. Как говорится In vina veritas!'
            phoenix "Ой, барашек, ну разве стоит начинать новую жизнь поддаваясь таким низменным страстям? Femina in vino non curator vagina."
            player "Как ты меня только что назвала?!"
            phoenix "Барашек. Хехе... это потому что я твой пастырь! Дошло? ^_^"
            player "Сгинь, пречистая!"
            phoenix "*ПУФ!*"
            "Феникс исчезает, хотя я всё ещё чувствую её присутствие. Можно будет позвать её, но сейчас мне не охота выслушивать ни бодрые нравоучения ни глупые шутки."
        "Игнорировать":
            'Это должно быть феникс. Мой ангел-хранитель, получивший статус феникса и видимый теперь мне. Но другие то её не видят, а значит если я буду с ней общаться на людях это будет похоже на шизофрению...'
    'Хмммм... я вижу таверну прямо напротив. Вход в подвал, место наверное не самое дорогое, но с другой стороны и мне пока сорить Искрами рано.'
    'На вывеске гладиатор в характерном шлеме держит в руках огромную кружку пива с карикатурно пышной пенной шапкой.'
    'Бред. Порошковое пиво никогда не даёт такой пены, а настоящее в Вечный Рим почти не возят - слишком дорого выходит для такого непритязательного напитка.'
    'Но вот гладиаторы это интересно. Может мне открыть свою школу гладиаторов? Как там называется тренер на местном жаргоне? По-моему "Ланиста"'
    menu:
        'Пойти выпить':
            call lbl_storylanista_meetlanista
        'Заняться делом':
            player "Вообще то феникс права - у меня слишком мало Искр и слишком много дел."
            call lbl_storylanista_marketintro

    return

label lbl_storylanista_meetlanista:
    scene expression 'images/bg/g_tavern.png'
    'Да тут дым коромыслом!'
    barmaid 'Добро пожаловать в "Гладиаторскую кружку", господин!'
    'Ко мне бодро подскочила улыбчивая служанка, с кувшином наперевес. А сиськи у неё знатные однако'
    barmaid 'Сегодня в честь победы нового чемпиона арены Яруса Быка, его хозяин Ликурий Меликенский угощает всех сангритой!'
    'Сангрита, значит... ну хоть бы не порошковое пиво. Его так и не научились делать похожим на настоящее.'
    'А сангрита это напиток призванный заменить вино - немного настоящего креплёного, разбавляется водой и сдабривается сахаром и специями'
    'Неплохая штука на мой вкус, хотя ценители тонких вин во внешних мирах такое разве что в унитаз выльют. В общем Вечный Рим не лучшее место для алоко-энтузисатов'
    barmaid 'Только у нас кончились кубки, предсталяете? Так много народу набежало...'
    'Зато женщины тут что надо - ведь некрасивых рабынь держать просто не рентабельно, слишком уж дорого стоит проживание в центре всех миров.'
    'Я засмотрелся на шикарную грудь официантки, прикрытую лишь одним слоем тонкой белой ткани над узким корсетом. Похоже она заметила что я гляжу ей не в лицо...'
    barmaid 'Ой, а ведь точно, господин. Я могу налить вина между грудей! Вы такой умница! ^_^'
    'Ничуть не смущаясь, девушка стянула вниз ткань лифа и обнажила свои роскошные дойки'
    'Подняв их одной рукой так чтобы образовалась изрядная треугольная ложбинка в середине, второй она вылила туда немного сангриты из кувшина.'
    barmaid 'Прошу, господин. Не побрезгуйте'
    player 'Такими сиськами брезговать грех. Твоё здоровье, красавица'
    'Придерживая её сиськи ладонями, я зарылся лицом в ложбинку между ними и начал всасывать сладкую красную сангриту'
    'Девушка взвизгнула, то ли не ожидая такого энтузиазма, то ли просто так'
    'Выпив жидкость я тщательно вылизал остающиеся ароматные капли напитка с её гладких сочных сисек'
    barmaid 'Хихи... щекотно же, господин. Вы такой проказник! ^_^'
    'Я притянул девушку к себе чтобы поцеловать и она резво повернула голову так чтобы подставить щёку'
    'Видимо настоящего поцелуя мне просто так не светит...'
    glad2 'Хей, мужик! Отлипни от Хлои и подойди ка сюда'
    'Грубый мужской голос прервал мои поползновения в сторону сисястой официантки'
    'За самым большим столом сидит компания крепких, покрытых шрамами мужчин в окружении хихикающих и таких же пьяных красоток'
    'Тот что окликнул меня, самый здоровенный среди них. Страшного вида мужик честно говоря. Учитывая его центральное положение это наверное и есть новоиспечённый чемпион'
    glad2 'Да не стой ты столбом, приятель. Двигай сюда'
    'Пожалуй лучше не игнорировать такое настойчивое предложение, хоть тон мне и не нравится'
    glad2 'Так то лучше. Я - Ярус, прозванный Быком, лучший секутор школы Ликурия Меликенского и чемпион Колизея!'
    glad2 'А вот тебя я прежде тут не встречал. Кто таков?'
    player 'Я мало выходил из Башни Змеи и не до кабаков мне было'
    player 'Но с этого дня я гражданин Дома Серпис. Без титулов, зато могу и прикупить себе гладиатора если пожелаю!'
    glad1 'Да он нахал, Ярус!'
    lanista 'Тебе бы самому язык прикусить, Жакоб. Сколько тебе Искр надо чтобы выкупиться? Двести четырнадцать, если я верно помню. Не говоря уже о гражданстве.'
    lanista 'Я Ликурий, хозяин всего этого сброда. Рад привествовать нового гражданина в нашем славном Доме'
    player 'Благодарю за угощение'
    glad2 'Выходит у нас у обоих сегодня праздник! Ну так выпей с нами, гражданин'
    'Ярус пнул ногой мужика спавшего облоктившись на стол по правую руку от него. Пьянчуга свалился с лавки но даже не проснулся'
    glad2 'Вот тебе место. Да и кубок похоже освободился'
    glad2 'Хлоя, хватит сиськами трясти! Иди сюда и наполни кубок моего нового приятеля!'
    'Мы подняли тост. Сначала за меня, потом, очередной, за чемепиона'
    'Джакоб красочно рассказал как Ярус бился в турнире. Сам чемпион быстро переключил внимание на девиц, а вот его хозяин присматривается ко мне черезчур вниммательно'
    'Не удивлюсь если это он приказал гладиатору позвать меня за стол. Что ему надо?'
    lanista 'Могу я узнать, каково твоё ремесло?'
    player 'Ну, попав сюда я сначала выживал на границе, а потом сумел завербоваться в сервиторы, в Змеиную Башню.'
    lanista 'Клерк, стало быть?'
    player 'Да. Перекладывал бумажки, пока не смог выкупить свободу. Потом стал начальником отдела и скопил Искр на гражданство.'
    player 'Только я не собираюсь больше этим заниматься. Надоело хуже холеры'
    lanista 'Это верно, работа клерка не достойна гражданина Великого Дома. И чем же ты тогда займёшься?'
    player 'Не знаю. У меня есть пара Искр для начала, надо решить. Может стать ланистой, как ты?'
    lanista 'Гладиаторов всегда не хватает, так что тут все дороги открыты. Многие думают что мы соперничаем и грызём друг другу глотки...'
    lanista 'Но на самом деле всё сложнее. В отличие от работоровцев наш хлеб не продажа воспитанников, а зрелищные бои'
    lanista 'Тут мало просто всех победить. Хороший бой может быть только с достойным противником.'
    lanista 'Чтобы поставить на арену хорошую пару, которая не разочарует зрителей надо внимательно подбирать соперников'
    lanista 'Если уж тебя взяли в Змеиную Башню, ты верно умный парень. Так что смог бы стать ланистой, если бы захотел'
    lanista 'Лицензия на школу бесплатная, спонсируется Великими Домами. "Хлеба и зрелищ" как говорится'
    lanista 'Но вот рабов придётся купить самому и получить с боёв хороший доход, не так то просто.'
    player 'Поможешь мне разобраться?'
    lanista 'Почему бы и нет. Спрашивай.'
    call lbl_storylanista_lanistaquestions

    return

label lbl_storylanista_lanistaquestions:
    menu:
        'К чему мне вообще стремиться?':
            lanista 'К богатству и славе, разумеется.'
            lanista 'Давай начистоту. Сейчас у тебя опыта ноль. Это значит что ты не сможешь подготовить полноценного гладиатора по вем правилам.'
            lanista 'Но это не самое главное. Ты можешь начинать не с колизея, а с частных боёв где правила не строгие.'
            lanista 'Главное другое. Каких бы крутых и правильных бойцов ты ни готовил, это нихера не значит без народной любви.'
            lanista 'Толпа должна знать тебя и хотеть твоих бойцов. А для этого им надо быть зрелищными, а не сильными.'
            lanista 'Добивайся красивых побед на разных аренах и для тебя будут открываться новые варианты.'
            lanista 'И когда тебя будет знать каждая собака, ты сможешь сделать то что я сделал сегодня - выставить свою команду на туринр Колизея.'
            lanista 'Вот там уже всё годится для победы. Потому что если ты подгтотовил чемпиона, это значит только одно - ты теперь среди лучших.'
        'С чего мне начать?':
            lanista 'Да хоть бы с этого кабака!'
            lanista 'Раз в декаду тут проходят кулачные бои. Никаких особых правил допуска, единственное что запрещено - снаряжение.'
            lanista 'Выставить можно любого раба, даже без подготовки. И его не убьют, а значит ты не потеряешь свои вложения.'
            lanista 'Только бери мужика. Для любителей смотреть как девчёнки друг друга мутузят есть лупанарий'
            lanista 'Кстати тоже хороше место для начала, если купишь сперва девку.'
            lanista 'И не гонись за сильными бойцами сначала. Если ты выставишь амбала который вышибет дух из случайного бойца, то ты конечно получишь награду.'
            lanista 'Но на что тут смотреть? Публика любит неожиданные повороты!'
            lanista 'Вот если твой парень будет на вид неказист, но сумеет забороть сильного противника, покажет напряжённый бой, это да.'
            lanista 'Тут публика будет твоя. И кто-нибудь обязательно замолвит словечко за тебя в Колизее.'
            lanista 'А ты тем временем разберёшься как натаскивать бойцов, поймёшь какие есть формальные типы.'
            lanista 'Потренироваться можно в хаотичных боях, но я бы туда особо лезть не советовал. Там нет ни денег ни славы, просто бой без ограничений.'
            lanista 'Стремиться надо к победе в основных схватках. И опять же - ищи неожиданной победы.'
            lanista 'Если покажешь крутой бой, тебя пригласят выставить гладиатора в элитные матчи. И тут снова то же правило - дай неожиданную победу, чтобы впечатлить публику.'
            lanista 'Когда толпа будет от тебя в восторге, тебя позовут в турнир. Там всё сложне, я сейчас даже начинать не стану.'
            lanista 'Если доберёшься до этого момента, разберёшься. Пока и так путь не близкий.'
        'Это же бизнес. Что там по деньгам?':
            lanista 'Тут ты прав. Об Искрах надо помнить всегда.'
            lanista 'Если тебе нечем будет питать инсигнию, она сгорит и ты окажешься снова либертином без прав.'
            lanista 'Всегда следи за тем чтобы оставался запас Искр на декаду.'
            lanista 'И помни что тебе надо содержать не только себя, но и гладиаторов - чем больше рабов, тем больше Искр ты на них тратишь каждую декаду.'
            lanista 'Никто не должен сидеть без дела, иначе ты разоришься.'
            lanista 'В крайнем случае гладиатора всегда можно продать, но особой выгоды тут не ищи - боец принесёт тебе больше денег на арене чем на рынке.'
            lanista 'На кажой площадке свои правила, но по большому счёту ты получаешь деньги за бой и при проишрыше и при выигрыше.'
            lanista 'Только вот если проиграешь в Колизее, твой раб скорее всего умрёт, а он стоит денег.'
            lanista 'Много сражайся. Выигрывай бои. И деньги потекут сами.'
        'Как мне побеждать?':
            lanista 'Про сами правила боя лучше поспрашивай у Рыжей Сони, на арене. Она расскажет лучше.'
            lanista 'Но главное что ты должен понять - нельзя просто пускать бойцов в тяжелые бои раз за разом и надеяться на победы.'
            lanista 'Победа требует подготовки, но не только. Гладиатору нужен кураж, нужна моральная поддержка.'
            lanista 'Ты можешь сам подготовить для него план боя, чтобы он знал какие слабые стороны есть у его противника.'
            lanista 'Ты можешь подсунуть ему девку из своих рабынь, чтобы он был доволен и уверен в себе.'
            lanista 'Или устроить попойку - как я сейчас. Только обязательно с друзьями. Можешь сам участвовать можешь отпустить братанов порезвиться.'
            lanista 'Друзья поддерживают друг-друга, делятся опытом, болеют за братана на арене. Всё это реально улучшает шансы на победу в бою.'
            lanista 'Одной только силы и подготовки мало, нужен моральный дух, воля к победе, уверенность в своих силах.'
            lanista 'Но будь осторожен. Люди любят внимание, но страсти часто доводят до беды. Могут быть и ссоры.'
            lanista 'Особенно если ты подложишь чужую девку не тому или отправишь раба пить с кем-то оставив его лучшего друга под замком.'
            lanista 'Сразу возникнут конфликты и интриги. А занчит твоего бойца подставят.'
            lanista 'Ты не поверишь какой-только херни не придумают ревнивые друзья и любовники.'
            lanista 'Если по ходу боя выяснится что твоего чемпиона предали, это может смешать все карты!'
            lanista 'Ну а кроме того, смотри с кем дерёшься. Просчитай шансы заранее и посмотри сможешь ли победить.'
            lanista 'Если враг тебе не по зубам, лучше откажись от боя. Если ввяжешься в проигрышную драку - загубишь гладиатора.'
        'Поздно уже. Я пойду':
            'Я поблагодарил новых друзей за угощение и слегка пошатываясь от принятого на грудь пошёл на поиски дорстойного жилья'
            call lbl_storylanista_marketintro
            return
    call lbl_storylanista_lanistaquestions
    return

label lbl_storylanista_tabernintro:
    scene expression 'images/bg/tavern_empty.png'
    barman 'Gaudete. Чем могу помочь?'
    player 'Я слышал у вас тут проходят кулачные бои без правил?'
    barman 'Это верно. Желаете сделать ставочку?'
    player 'Не совсем. Я хочу выставить своего бойца. За деньги.'
    barman 'А, так вы ланиста? Ну если подберёте хорошую пару тем бойцам которые у нас есть, для зрелищного боя, то я готв заплатить.'
    barman 'Больше если твой боец победит, меньше если проиграет. Но в любом случае не много - бой не смертельный, рисков считай никаких.'
    player 'А какие ограничения на выставляемых бойцов?'
    barman 'Мне всё равно какого он будет класса, хоть чемпиона приводи лишь бы мужика. Но помни - никакого снаряжения, только навыки! Карт брони и оружия в кулачном бою у твоего гладиатора не будет.'
    player 'Понял. По рукам!'

    return

label lbl_storylanista_lupaintro:
    scene expression 'images/bg/brothel.png'
    bmaman 'Gaudete. Добро пожаловать в наш дом удовольствий! Кого сегодня желает благородный патриций?'
    player 'К чему эта лесть? Я обычный плебей.'
    bmaman 'Нет-нет, мой дорогой. Запомните, в нашем доме каждый клиент - патриций!'
    player 'А я не клиент. Я ланиста. Слышал что у вас тут проходят бои.'
    bmaman 'Вот как? Ну "бои" это громко сказано. Мы тут не фанаты крови и трупов, просто иногда посетителям хочется немного адреналина перед сексом.'
    bmaman 'Мы проводим женские драки в масле и поединки на кнутах, тоже только для девушек.'
    player 'И если моя рабыня победит, я получу награду?'
    bmaman 'Ох, милый. Мужчины только и могут думать что о победах. Но у нас тут не арена и не поле боя, и ценится у нас другое.'
    player 'Это что-же?'
    bmaman 'Красота! Я дам надбавку если вы выставите девушку специально подготовленную для сексуальной борьбы. "Луктаторы" так они называются.'
    bmaman 'И конечно нам нужны яростные схватки, поэтому за победу вашей девочки я заплачу. Но вот если она проиграет...'
    player 'Что тогда?'
    bmaman 'У нас есть правило: проигравшая девушка достаётся посетителям. За одну искру с члена, они могут иметь её до самого утра любым способом по кругу и одновременно.'
    player 'Вряд ли это хорошо для здоровья моей гладиаторши...'
    bmaman 'О, поверьте, женский организм способен пережить такое. Зато я заплачу вам половину дохода. Чем больше членов соблазнится на красоту вашей рабыни, тем больше вы получите.'
    player 'Тоесть я могу бросить на ринг красивую девку и получить даже больше если она проиграет?'
    bmaman 'Если она будет красивой то да. Конечно она от этого не получит опыта, а вы славы. Но заработок может быть хороший.'
    bmaman 'К тому же бонус за особую подготовку луктатора, я дам независимо от результата боя. Борьба в грязи это искусство!'
    player 'Шикарно! А что там с дуэлями на кнутах?'
    bmaman 'Бойцы с кнутами называются андабандами. Это куда болезненней валяния в масле, но не так популярно.'
    bmaman 'Я заплачу за это как за обычный бой. То что надо для наших гостей которых боль возбуждает сильнее сисек и писек.'
    player 'А что по ограничениям на выставляемых рабов?'
    bmaman 'Только женщины. Для битв в грязи годится любой класс, но никаких карт снаряжения, только навыки. На кнутах бьются только андабанды с родным снаряжением.'
    player 'Хорошо. По рукам!'

    return

label lbl_storylanista_colintro:
    scene expression 'images/bg/arena.png'
    'Вы находите Рыжую Соню - легендарную гладиаторшу, которая являетя сейчас распорядительницей Колизея.'
    redsonya 'Ещё один ланиста? То что любой может этим заняться, не значит что любой может добиться успеха!'
    player 'Я уже выбрал пусть, теперь у меня нет выхода кроме как преуспеть.'
    redsonya 'Ха! Ну как пожелаешь. Только учти одну вещь:'
    redsonya 'Никто не пустит твоих бойцов на арену, пока ты не докажешь что способен организовывать достойные зрелища.'
    player 'И как же мне это доказать, если меня не пустят на арену?'
    redsonya 'Ты можешь начать с не смертельных боёв в лупанариях и тавернах. Если твои бойцы покажут класс, то у тебя мгновенно появятся рекомендации.'
    player 'И тогда мой боец сможет стать чемпионом арены?'
    redsonya 'Воу, придержи коней, "ланиста". Сначала я допущу тебя до схваток на разогреве. Если покажешь себя там, то дам шанс в главных боях.'
    redsonya 'И вот когда тебя будет в Риме знать каждая собака, тогда я позволю тебе собрать команду для турнира. Это большое дело, знаешь ли.'
    redsonya 'Не надейся что взлетишь по этой ленстнице быстро и просто. Придётся поработать.'
    player 'Хочется конечно попроще, но так и быть. Поработаю. Только ради тебя. ^_^'
    redsonya '*презрительно ухмыляется*'
    player 'Можешь прояснить для меня кое-какие моменты?'

    call lbl_storylanista_colquestions

    return

label lbl_storylanista_colquestions:
    menu:
        'Как работает боевая система?':
            redsonya 'Представь себе, что каждая особенность бойца это игральная карта.'
            redsonya 'Его оружие, броня, особые навыки, хитрые приёмы и боевой дух - на каждую особенность есть карта.'
            redsonya 'Часть карт определяются классом бойца - к ним у твоего гладиатора будет доступ всегда.'
            redsonya 'Но есть карты которые можно набрать до боя и они больше зависят от того что твой боец делал: веселился с друзьями, трахал девку или отрабатывал с тобой тактику боя'
            redsonya 'Всё это отразится на его ассортименте боевых карт, но только на ближайший бой.'
            redsonya 'К серьёзному бою можно готовиться несколько декад к ряду. А вот выпускать своего бойца на арену без дополнительной накачки, декада за декадой это рисковано.'
            redsonya 'У твоего врага тоже есть карты. Считай что они все зависят от его боевого класса, никаких дополнений.'
            redsonya 'Но засада в том, что тебе надо побить КАЖДУЮ его карту чтобы победить.'
            redsonya 'Что толку если ты во всём переиграл врага, если скажем не смог пробить его броню? Или не смог попасть? Нужно найти ответ на каждый его козырь.'
            redsonya 'Представь себе что это раунд игры в дурака - противник кидает тебе одну за другой карты, а ты должен отбиться от каждой или проиграть.'
            player 'А если моя карта будет слабее его?'
            redsonya 'Она сгорит и потрятится зря, а ты продолжишь отбиваться пока у кого-то из вас не кончатся карты.'
            player 'И что если они кончатся у меня?'
            redsonya 'Тогда ты проиграл.'
            player 'А как же понять какая карта сильнее а какая слабее?'
            redsonya 'Это ключевой момент! Именно в том и заключается мастерство чтобы набрать нужные для победы карты до боя и потом правильно их разыграть.'
            redsonya 'У боевых карт есть достоинство, по взрастанию старшинства это:\n красный < фиолетовый < циан < синий < зелёный < золотой.'
            player 'И откуда берётся это достоинство?'
            redsonya 'Как правило зависит от атрибутов твоих гладиаторов. Например чтобы нанести удар мечём нужна сила. Значит достоинство твоей карты "меч" будет равно силе гладиатора.'
            player 'И если у него золотая сила...'
            redsonya 'То и карта меча будет золотой! Верно. Хотя бывают карты и похитрее. У некоторых значение фиксированное, другие зависят от боевого духа или уровня класса. Надо смотреть на каждую отдельно.'
            player 'Значит я просто набираю карты посильнее и закидываю ими более слабые?'
            redsonya 'Да, но нет. Запомни - масть важнее достоинства.'
            player 'Вот это что за АУЕ такое, только что было? Мусорам по пасти, пацанам по масти?'
            redsonya 'Понятия не имею о чем ты там лопочешь. Масти важны! Очень важны. Запомни как они взаимодействуют и будешь побеждать.'
            redsonya 'Самая слабая масть - черепа. Карта любой другой масти побьёт череп, какое бы достоинство он не имел.'
            player 'Даже красная бубна может побить золотой череп?!'
            redsonya 'Да. Именно так. Черепа отстой. Используй их только против других черепов с достоинством помладше. Это всё на что они годятся.'
            redsonya 'Есть четыре основных масти: бубны, трефы, черви и пики. Они как бы равны, но на самом деле всё хитрее, так что слушай внимательно:'
            redsonya 'С бубнами всё просто. У них нет сил или слабостей - старшая бубна бьёт любую младшую карту другой масти и бьётся старшей картой любой же масти.'
            redsonya 'Три остальные масти работают как "камень-ножницы-бумага". Каждая масть сильна против одной и слаба против другой.'
            redsonya 'Червы сильнее треф, трефы сильнее пик, а пики сильнее червей.'
            redsonya 'Можешь запомнить так: черви это любовь, пики - предательство, а трефы - мудрость.'
            redsonya 'Любовь страдает от предательства, предательство раскрывается мудростью, а мудрость склоняется перед любовью.'
            player 'Какое это отношение имеет к бою?'
            redsonya 'Это условности. Просто так легче запомнить:\n Черви > Трефы > Пики > Черви.\n Любовь > Мудрость > Предательство > Любовь.'
            player 'Ух. Постараюсь запомнить...'
            redsonya 'Постарайся. Это самое важное.'
            redsonya 'Теоретически (не думаю что тебе пригодится) есть ещё джокеры. Они бывают только красные и золотые. Твой всегда золотой, у врага всегда красный.'
            redsonya 'Джокер бьёт карту любой масти. Но золотой джокер бьёт красного. Твой джокер всегда золотой, а у врага всегда красный.'
            player 'Удобно'
            redsonya 'Ну, иначе ты бы никогда не победил против золотого джокера.'
            player 'Это всё?'
            redsonya 'Да. Просто помни про старшинство мастей и выбирай подходящие карты чтобы побеждать карты врага. Если масти равны по силе, то ориентируйся на цвет карты - её достоинство.'
            redsonya 'Я напомню тебе если будет нужно. Столько раз сколько будет нужно.'
            call lbl_storylanista_colquestions

        'Я проигрываю даже если мы равны!':
            redsonya 'Да. Для победы тебе нужно побить каждую карту врага. И если у тебя меньше карт или хотя бы одну карту врага нечем крыть - ты обречен.'
            redsonya 'Но это не беда, так как в отличие от врага ты можешь добыть для своих гладиаторов дополнительные карты на один бой.'
            player 'Откуда их взять?'
            redsonya 'Работай со своими гладиаторами. И давай им развлекаться, тогда у них поднимется боевой дух.'
            redsonya 'Ты можешь продумать тактику следующего боя. Или послать своего бойца развлекаться в таверне и лупанарии, но только в паре с кем-то.'
            redsonya 'Если братаны или сеструхи пойдут вместе, они вместе получат бонус братства и подружатся. Если отправишь мужчину и женщину, не удивляйся что они станут любовниками.'
            redsonya 'Оба любовника так же получат бонусы. И достоинство карты будет зависеть от привлекательности любовника. Чем больше харизма партнёра, тем старше будет карта удовлетворения.'
            redsonya 'Ну и с тусовкой та же история, только там в дело идёт не харизма, а коварство. Чем лучше подвешен язык у "второго пилота" тем больше будет успех в их делишках.'
            redsonya 'Совместные развлечения выматывают обоих участников и стоят Искр. Но с другой стороны помимо поддержки после развлчения оба получат ещё и кураж.'
            player 'Что за кураж?'
            redsonya 'Ощущение удачливости. Насколько сильно оно повлияет зависит от силы характера самого гладиатора.'
            redsonya 'Ну а годность твоей тактики, придуманной для бойца, зависит только от твоего опыта ланисты. И разрабатывая тактику ты потратишь только свои силы а не его.'
            player 'А я могу набрать побольше этих карт куража, тактики и поддержки?'
            redsonya 'Нет. Один человек может одновременно иметь лишь по одной карте каждого вида, но тебе хватит если разыгрывтаь их с умом.'
            player 'Значит слишком много вечеринок на пользу не пойдёт...'
            redsonya 'Да. Причём во многих смыслах. Видишь ли - люди ревнивы. Особенно бесправные рабы которым так ценна возможность иметь друга.'
            redsonya 'Конечно сам ты можешь спать или тусить с кем угодно без последствий, но вот если дать рабам повод для ссоры...'
            redsonya 'Например отправить парня развлекаться не с той девчёнкой или разбить сложившуюся пару побратимов. Тот что останется не у дел может затаить на "предателя" зуб'
            redsonya 'И напакостить ему как нибудь. Можно было бы и не обращать внимания на эти разборки, но они могут подвести твоего бойца в самый важный момент'
            player 'Это как?'
            redsonya 'В битве у врага ВНЕЗАПНО появится карта "предательства". И тебе придётся побить ещё и её ко всему в предачу.'
            redsonya 'А так как ты на это не рассчитывал, сюрприз может оказаться фатальным.'
            redsonya 'Следи за отношениями своих подопечных и не давай им поводов для ссор.'
            call lbl_storylanista_colquestions

        'Как мне развивать моих гладиаторов?':
            redsonya 'Ну сначала их и гладиаторами называть не стоит. На рынке ты купишь едва обученных подчиняться рабов.'
            redsonya 'И чтобы чему-то их научить, тебе сначала надо самому набраться опыта и разобраться что к чему.'
            redsonya 'Запомни главное - тебе нужна достойная победа. Одолев слабого врага ты ничему не научишься, да и любви толпы не стяжаешь.'
            redsonya 'Старайся побеждать слабыми бойцами сильных, а не наоборот! По крайней мере для опыта.'
            redsonya 'Чем больше будет твоё признание, тем более престижных бойцов ты сможешь готовить. Но и самим рабам нужен будет бовой опыт, прежде чем они будут готовы к продвижению.'
            redsonya 'Веди их от победы к победе, обучай и вскоре будешь иметь отряд элитных гладиаторов.'
            redsonya 'Только помни, что каждого надо содержать и кормить, так что пусть не сидят без дела иначе они очень быстро тебя разорят!'
            call lbl_storylanista_colquestions

        'Напомни мне про старшинство карт.':
            redsonya 'Золотой > Зелёный > Синий > Циан > Фиолетовый > Красный. Это достоинство карты, но оно не так важно как масть.'
            redsonya 'Черепа слабее всех, любая другая масть побьёт их независимо от достоинства.'
            redsonya 'У бубен смотри толко на достоинство, они равны всем другим обычным мастям (и конечно силнее черепов)'
            redsonya 'Черви сильнее чем крести, но боятся пик. Пика пронзает сердце!'
            redsonya 'Крести сильнее пик, но слабее червей. Кресты золочёные тупят пики точёные!'
            redsonya 'Пики сильнее червей, но слабее крестей. Пронзают сердца, но тупятся о кресты.'
            redsonya 'Ну и если вдруг увидишь у врага джокера, то его можно перебить только своим джокером. А твой джокер побьёт любую карту вообще.'
            call lbl_storylanista_colquestions

        'Пока что это всё':
            pass

    return

label lbl_storylanista_marketintro:
    'Я разобрался с жильём и оформил лицензию на деятельность ланисты, благо это единственная бесплатная лицензия среди всех гильдий'
    'Теперь нужно позаботиться о своём главном капитале - приобрести рабов.'
    scene expression 'images/bg/slavemarket.png'
    'Я отправился на центральный невольничий рынок'
    slaver "Приветствую тебя, о Солнцеликий! Прошу сюда, погляди на мой товар!"

    return

label lbl_storylanista_luctatorbang:
    scene expression 'images/bg/brothel.png'
    show expression 'images/special/luctator_bang.png' as bang at top with dissolve
    'Плейсхолдер. Тут будет сцена секса с проигравшей луктаторшей.'
    show expression 'images/special/luctator_bang2.png'as bang at top with dissolve
    'Вот так!'
    hide bang

    return

label lbl_storylanista_wenchsex:
    scene expression 'images/special/wench_bang.png'
    'Плейсхолдер. Тут будет сцена секса с официанткой Хлоей из таверны.'

    return

label lbl_storylanista_brobang:
    scene expression 'images/special/brosex.png'
    'Плейсхолдер. Тут будет сцена двойного проникновения на пару с гладиатором.'
    return

label lbl_storylanista_slavesex:
    scene expression 'images/special/slavesex.png'
    'Плейсхолдер. Тут будет сцена любви со своей гладиаторшей.'
    return

label lbl_storylanista_sonyabang:
    scene expression 'images/bg/arena.png'
    show expression 'images/special/sonya_bang.png' as bang at top with dissolve
    'Плейсхолдер. Тут будет сцена секса с Рыжей Соней и гладиаторами-чемпионами.'
    show expression 'images/special/sonya_bang2.png'as bang at top with dissolve
    'Вот так!'
    hide bang

    return

label lbl_storylanista_coleventpunish:
    'Ты достиг нового уровня ланисты'

    return

label lbl_storylanista_endofstory:
    scene expression 'images/bg/arena.png'
    'Толпа на трибунах ликует. Это был действительно сильный турнир со множеством интересных схваток'
    'Мой гладиатор стоит посреди арены потрясая окровавленным оружием - сегодня родился новый чемпион!'
    'Ну а пробился на вершину славы которой способен достичь ланиста'
    redsonya 'Наслаждаешься моментом?'
    scene expression 'images/special/sonya_love.png'
    player 'Я ПОБЕДИЛ!'
    $ renpy.full_restart()
    return

label lbl_storylanista_actionanalys:
    phoenix 'Привет! Нужен совет как развивать своих гладитаоров? Я подскажу.'
    phoenix 'Самое большое усиление которое ты можешь дать гладиатору - это обучить и снарядить его по стандартам продвинутого боевого класса. Но есть некоторые условия.'
    phoenix 'Во-первых, обучение последовательное. Ты не можешь сразу воспитать гоплинию, например. Сначала рабыне придётся освоить класс луктатора, потом андабанда и уже дальше откроется потенциал для гоплинии.'
    phoenix 'Первый апгрейд требует только твоих навыков - если у тебя за плечами есть хотя бы одна хорошая победа, ты разберёшься как натаскивать рабов на базовый гладиаторский класс.'
    phoenix 'Но дальше гладиаторам понадобится личный боевой опыт и личные славные победы, чтобы стать достойными более высоких классов. Чтобы перейти к более сильному классу надо показать себя в более слабом.'
    phoenix 'У более сильных классов больше базовых карт снаряжения и навков. Кстати за гладитаоров со снаряжением тебе придётся раскошелиться на покупку этого снаряжения, так что рост некоторых классов требует Искр!'
    phoenix 'Чтобы тебе было проще ориентироваться, я помечу продвинутое обучение сердечком если гладитор готов!'
    phoenix 'Теперь про отработку тактики. Ты можешь применить собственный боевой опыт, чтобы подсказать своему гладиатору оптимальный способ действий в следующем бою. Он получит карту "тактики", масть крести, достоинство зависит от твоего уровня.'
    phoenix 'Главным преимуществом такой подготовки является то, что она затрачивает лишь твои силы, а гладитаор останется готовым к бою и его можно будет хоть сразу выставить на ринг.'
    phoenix 'Если ты понимаешь, что боевой дух твоих бойцов слабоват для выхода на арену...'
    player 'Стоп! Как я это должен понять то?'
    phoenix 'Ну, барашек, это же так просто - если у тебя слишком мало карт чтобы побить потенциального оппонента, значит тебе нужны дополнительные карты. А они как раз могут быть получены в виде боевого духа!'
    phoenix 'А чтобы поднять боевой дух, твоих ребят надо отправить развлекаться по тавернам и лупанариям в хорошей компании. Ты можешь сам присоединиться к гладиатору или поставить его в пару к другому своему рабу.'
    phoenix 'Если отправить на равзлечение однополую пару, то они будут укреплять дружбу, а если мужчину и женщину то они наверняка займутся любовью. Только будь осторожен - уже имеющимся любовникам и друзьям это может не понравиться.'
    phoenix 'В любом случае оба участника развлечений уйдут в недельный загул и будут ни на что не способны. Зато получат сразу по две карты: куража и дружбы либо любви.'
    phoenix 'Карта куража имеет бубновую масть и достоинство равное силе характера самого гладиатора.'
    phoenix 'Любовь конечно же имеет червовую масть и зависит по достоинству от харизмы партнёра. А дружба масть пик и зависит по достоинству от коварства друга.'
    phoenix 'Только помни, что в отличие от карт класса, карты боевого духа будут действенны только в следующем бою - потом они исчезнут, даже если ты не применишь их в бою.'
    phoenix 'Ну и конечно раба можно продать. Цена зависит как от базовых характеристик, так и от набора и качества его классовых карт и от списка достойных побед.'

    return