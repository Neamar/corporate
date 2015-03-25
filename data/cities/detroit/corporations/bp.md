name: BP
markets:
    sécurité: 3
    nanotechnologie: 2
    cyberware: 2
    santé: 0
datasteal: 20
sabotage: 10
extraction: 20
detection: 30
on_first:
    update('neonet', -1)
    update('shiawase', -1)
on_last:
    update('sony', -1)
    update('shiawase', 1)
on_crash:
    # TBD

Description BP
