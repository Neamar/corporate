name: Invictus
markets:
    nanotechnologie: 2
    alimentaire: 2
    magie: 2
    communication: 2
datasteal: 10
sabotage: 10
extraction: 30
detection: 30
on_first:
    update('renraku', -1)
    update('sony', 1)
on_last:
    update('sony', -1)
    update(ladder[-2], -1)
on_crash:
    # TBD

Description Invictus
