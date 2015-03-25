name: Impulse
markets:
    santé: 1
    transport: 3
    communication: 2
    armement: 2
datasteal: 20
sabotage: 10
extraction: 10
detection: 60
on_first:
    update(ladder[1], -2)
on_last:
    update('saeder-krupp', 2)
on_crash:
    # TBD

Description Impulse
