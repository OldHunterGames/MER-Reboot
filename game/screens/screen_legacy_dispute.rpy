label lbl_legacy_dispute(dispute):
    call screen sc_legacy_dispute(dispute)
    return

screen sc_legacy_dispute(dispute):
    frame:
        xsize 400
        xalign 0.5
        ysize 300

        if dispute.winner is None:
            vbox:
                textbutton 'Accept price(npc takes angel':
                    sensitive (dispute.can_accept_person())
                    action Function(dispute.money_accept)
                textbutton 'Double price(you take angel)':
                    sensitive (dispute.can_raize_player())
                    action Function(dispute.money_raise)
                textbutton 'Random':
                    action Function(dispute.dice_decision)
                textbutton 'Fight':
                    action Function(dispute.fight)
                textbutton 'Sex':
                    sensitive (dispute.can_sex())
                    action Function(dispute.sex)
        else:
            text 'Dispute winner is %s' % dispute.winner.name:
                xalign 0.5
                yalign 0.5
            textbutton 'Leave' action Return():
                xalign 0.5
                yalign 1.0