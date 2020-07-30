screen sc_crisis_routes(player, person):
    modal True
    zorder 10
    tag info
    window:
        style 'char_info_window'
        frame:
            hbox:
                for crisis in MerCrisisSystem(person).get_active_crisises():
                    vbox:
                        text crisis.trigger
                        for route in MerCrisisRoute.get_by_crisis(crisis):
                            textbutton route.name action Function(route.go_to_route, player, person)