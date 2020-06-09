label lbl_new_slave_event(slave):
    menu:
        'Ignore':
            python:
                if NatureData(slave).get_nature() == 'sanguine':
                    emotion = get_basic_emotion('curiosity')
                else:
                    emotion = get_basic_emotion('curiosity')
                PersonEmotions(slave).add_emotion(emotion)
    '[slave.name] got emotion: [emotion.name]'