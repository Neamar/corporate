name: c
markets:
    armement: 3
    cyberware: 3
    alimentaire: 3
    nanotechnologie: 3
datasteal: 0
sabotage: 0
extraction: 0
detection: 0
on_first:
    update('c', 1)
on_last:
    update(ladder[0], -1)

Test corporation #1
