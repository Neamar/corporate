name: CityGroup
markets:
    communication: 2
    immobilier: 3
    magie: 3
    sécurité: 2
datasteal: 10
sabotage: 10
extraction: 10
detection: 90
on_first:
    update(ladder[-1], -2)
on_last:
    update('aztechnology', 1)
    update(ladder[0], -1)
on_crash:
    # TBD

Description CityGroup
