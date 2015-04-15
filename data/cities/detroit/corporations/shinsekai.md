name: Shinsekai
markets:
    magie: 3
    immobilier: 3
    nanotechnologie: 2
    armement: 3
datasteal: 10
sabotage: 20
extraction: 10
detection: 60
on_first:
    update('horizon', -1)
    update(ladder[-1], -1)
on_last:
    update('horizon', 2)
on_crash:
    # TBD

Description Shinsekai
