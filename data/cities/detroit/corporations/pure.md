name: Pure
markets:
    cyberware: 2
    transport: 3
    communication: 2
    armement: 3
datasteal: 30
sabotage: 10
extraction: 10
detection: 30
on_first:
    update('spinrad', -1)
    update(ladder[1], -1)
on_last:
    update('neonet', 1)
    update('renraku', 1)
on_crash:
    # TBD

Description Pure
