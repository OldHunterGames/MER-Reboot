label lbl_zombieworld_tutorial(world):
    show expression world.path('resources/forest01.png') as bg
    python:
        location_forest = ZombieWorldLocation(
            'forest',
            zombieworld_tutorial_locations['forest']
        )
        rape_event = ZombieWorldEvent('rape', zombieworld_tutorial_events['rape'])
        location_forest.add_event(rape_event)
        world.set_location(location_forest)
    call screen sc_zombieworld_location(world)
    return
