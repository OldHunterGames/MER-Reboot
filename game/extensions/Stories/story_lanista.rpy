label lbl_storylanista_start:
    $ player.set_avatar('images/avatar/special/player.png')
    $ player.firstname = 'Me'
    $ SerPri = PersonCreator.gen_person()
    $ SerPri.set_avatar('images/avatar/special/princeps_serpis.png')
    $ SerPri.firstname = 'Принцепс дома Серпис'
    $ phoenix = PersonCreator.gen_person()
    $ phoenix.set_avatar('images/avatar/special/phoenix.png')
    $ phoenix.firstname = '???'
    $ barmaid = PersonCreator.gen_person()
    $ barmaid.set_avatar('images/avatar/special/barmaid.png')
    $ barmaid.firstname = 'Официанта'
    $ lanista = PersonCreator.gen_person()
    $ lanista.set_avatar('images/avatar/special/lanista.png')
    $ lanista.firstname = 'Ланиста'
    $ glad1 = PersonCreator.gen_person()
    $ glad1.set_avatar('images/avatar/special/glad1.png')
    $ glad1.firstname = 'Гладиатор'
    $ glad2 = PersonCreator.gen_person()
    $ glad2.set_avatar('images/avatar/special/glad2.png')
    $ glad2.firstname = 'Чемпион'

    show expression "images/bg/serpis_temple.jpg" as bg
    menu:
        'Начать эпилог':
            pass
        'Пропустить эпилог':
            return

    SerPri "Данной мне властью, возжигаю эту инсигнию в твоей душе и связую её с владыками Дома."
    SerPri "Поднимись, пэр Дома Серпис и отыне не склоняй колен ни пред кем."
    'Я встал и отошел прочь, чтобы дать место следующему участнику ритуала. После кризиса черной седьмицы, в Доме Серпис сгорело много инсигний и сейчас либертины у которых было за душой хотя бы немного искр спешили воспользоваться шансом чтобы получить полноценное гражданство.'
    'Всего минуту назад я был одним из таких либертинов. Благодаря критическому положению дома, мне удалось не только оплатить стоимость начертания инсигнии но и сохранить для себя сотню Искр, для начала новой жизни.'

    player "Черт, жжётся"

    'У вас когда-нибудь горела душа? Это очень странное чувство и слова которые я использую чтобы его писать конечно не точны. Но я чувствую знак Дома Серпис на своей душе как узор из огня и Искры как маленькие шекочущие мурашки.'
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
            phoenix "Стой-стой-стой!. Я тебе пригожусь."
            player "Это как?"

        "Игнорировать":
            'Это должно быть феникс. Мой ангел-хранитель, получивший статус феникса и видимый теперь мне. Но другие то её не видят, а значит если я буду с ней общаться на людях это будет похоже на шизофрению...'

    return