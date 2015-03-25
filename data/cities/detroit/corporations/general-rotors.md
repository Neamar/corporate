name: General Rotors
markets:
    armement: 3
    alimentaire: 3
    sécurité: 3
    magie: 3
datasteal: 10
sabotage: 30
extraction: 10
detection: 30
on_first:
    update(ladder[-1], 1)
    update(ladder[-2], 1)
on_last:
    update(ladder[0], -1)
    update(ladder[1], -1)
on_crash:
    # TBD

Description General Rotors
