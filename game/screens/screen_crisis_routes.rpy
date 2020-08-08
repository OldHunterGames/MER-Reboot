screen sc_crisis_routes(player, person):
    modal True
    zorder 10
    tag crisis
    window:
        style 'char_info_window'
        textbutton 'Leave' action Hide('sc_crisis_routes')
        frame:
            hbox:
                for crisis in MerCrisisSystem(person).get_active_crisises():
                    vbox:
                        text crisis.trigger
                        for route in MerCrisisRoute.get_by_crisis(crisis):
                            textbutton route.name action Function(route.go_to_route, player, person)