name: Iris
markets:
    immobilier: 3
    alimentaire: 3
    cyberware: 1
    santé: 2
datasteal: 20
sabotage: 20
extraction: 10
detection: 30
on_first:
    update('prometheus', 1)
    update(ladder[1], 1)
on_last:
    update(ladder[0], 2)
on_crash:
    # TBD

Description Iris
