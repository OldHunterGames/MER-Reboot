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

label lbl_resolve_1(player, person, crisis):
    python:
        print(crisis.trigger)
        MerCrisisSystem(person).fulfill_crisis(crisis)
    'Kekukek'
    return