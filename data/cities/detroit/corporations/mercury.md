name: Mercury
markets:
    alimentaire: 3
    immobilier: 3
    transport: 3
    cyberware: 2
datasteal: 10
sabotage: 10
extraction: 20
detection: 60
on_first:
    update('renraku', 1)
    update('shiawase', 1)
on_last:
    update(ladder[-2], -2)
on_crash:
    # TBD

Descirption Mercury
