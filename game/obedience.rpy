label lbl_raise_obedience(slave, show_initial=True):
    if not core.can_interact(slave):
        return
    python:
        import random
        slave_suggestions = QuirksSuggestions(slave).get_suggestions()
        slave_quirk_data = QuirkData(slave)
        slave_nature_data = NatureData(slave)
        start_text = random.choice(obedience_starting_text_data[slave_nature_data.get_nature()])
    if show_initial:
        '[start_text]'
    python:
        print('phase1 starts')
        phase1_state = None
        loop_counter = 0
        while True:
            phrases_to_use = natures_phrases if loop_counter == 0 else natures_phrases_plus
            if Slave(slave).approachability() < 1 or core.player_approachability < 1:
                break
            first_phase_variants = NatureData.shuffled_natures()
            phrases = []
            for phrase_type in first_phase_variants:
                if phrase_type in slave_suggestions:
                    phrases.append(
                        (
                            "{{color=#00ff00}}{0}{{/color}}".format(
                                random.choice(phrases_to_use[phrase_type])
                            ),
                            phrase_type
                        )
                    )
                else:
                    phrases.append(
                        (
                            random.choice(phrases_to_use[phrase_type]),
                            phrase_type
                        )
                    )
            choisen_type = renpy.display_menu(phrases)
            slave_nature = slave_nature_data.get_nature()
            if choisen_type == slave_nature:
                phase1_state = 'true_choise'
                renpy.say(None, random.choice(natures_good_reactions[slave_nature]))
                break
            else:
                Slave(slave).decrease_approachability()
                phase1_state = 'false_choise'
                renpy.say(None, random.choice(natures_bad_reactions[slave_nature][choisen_type]))
            loop_counter += 1
    if phase1_state != 'true_choise':
        return

    python:
        while True:
            phase2_state = None
            if not core.can_interact(slave):
                break
            second_phase_variants = []
            second_phase_variants.append(random.choice(slave_quirk_data.good_strategy()))
            strategies = ControlStrategy.get_strategies()
            strategies.remove(second_phase_variants[0])
            random.shuffle(strategies)
            second_phase_variants.extend(strategies[0:3])
            phrases = []
            for phrase_type in second_phase_variants:
                if phrase_type in QuirksSuggestions(slave).get_control_strategy_suggestions():
                    phrases.append(
                        (
                            "{{color=#00ff00}}{0}{{/color}}".format(
                                random.choice(control_strategy_phrases[phrase_type])
                            ),
                            phrase_type
                        )
                    )
                else:
                    phrases.append(
                        (
                            random.choice(control_strategy_phrases[phrase_type]),
                            phrase_type
                        )
                    )
            choisen_type = renpy.display_menu(phrases)
            print(choisen_type)
            print(slave_quirk_data.good_strategy())
            if choisen_type in slave_quirk_data.good_strategy():
                phase2_state = 'good_choise'
                quirk_for_phrase = Quirk.quirk_by_good_strategy(choisen_type)
                renpy.say(None, random.choice(quirk_for_phrase.good_reactions))
                Slave(slave).increase_obedience()
                break
            if choisen_type in slave_quirk_data.bad_strategy():
                phase2_state = 'bad_choise'
                quirk_for_phrase = Quirk.quirk_by_good_strategy(choisen_type)
                renpy.say(None, random.choice(quirk_for_phrase.bad_reactions))
                Slave(slave).decrease_approachability()
                break
            renpy.say(None, random.choice(control_strategy_phrases[choisen_type]))
            phase2_state = 'neutral_choise'
            Slave(slave).decrease_approachability()
    if phase2_state == 'bad_choise':
        call lbl_raise_obedience(slave, False)
    return