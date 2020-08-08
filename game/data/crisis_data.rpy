init python:
    from mer_crisis import *
    crisis = MerCrisis(
        'make_pain',
        '',
        lambda p1, p2: True,
    )
    route = MerCrisisRoute(crisis, 'Be good', 'lbl_resolve_1')
    MerCrisis.register_crisis(crisis)
    MerCrisisRoute.register_route(route)

    train_crisis = MerCrisis(
        'train',
        '',
        lambda p1, p2: ClassData(p2).get_class_type() == 'useless',
    )
    humiliate_route = MerCrisisRoute(train_crisis, 'Humiliate', 'lbl_resolve_humiliate')
    spank_route = MerCrisisRoute(train_crisis, 'Spank', 'lbl_resolve_spank')
    MerCrisis.register_crisis(train_crisis)
    MerCrisisRoute.register_route(spank_route)
    MerCrisisRoute.register_route(humiliate_route)

label lbl_resolve_humiliate(player, person, crisis):
    "[person.name] подчиняется, кризис решён. Побочных эффектов нет"
    python:
        MerCrisisSystem(person).fulfill_crisis(crisis)
    return

label lbl_resolve_spank(player, person, crisis):
    python:
        text = 'Этого не достаточно для подчинения'
        result = False
        nature_data = NatureData(person)
        nature = nature_data.get_nature()
        if nature == 'melancholic':
            text = 'Шлепки эффективный благодаря чувствительности раба'
            result = True
        if nature == 'phlegmatic':
            text = 'Бесполезно. Упертый характер'
        if nature == 'choleric':
            text = 'Бесполезно. Буйный характер. Спровоцированна ненависть'
    python:
        if result:
            MerCrisisSystem(person).fulfill_crisis(crisis)
    '[text]'
    return

label lbl_resolve_1(player, person, crisis):
    python:
        print(crisis.trigger)
        MerCrisisSystem(person).fulfill_crisis(crisis)
    'Kekukek'
    return