name: Appleseed
markets:
    transport: 3
    sécurité: 2
    nanotechnologie: 2
    santé: 2
datasteal: 10
sabotage: 20
extraction: 20
detection: 30
on_first:
    update('spinrad', 2)
on_last:
    update('spinrad', -1)
    update(ladder[-2], 1)   
on_crash:
    # TBD

Description Appleseed
