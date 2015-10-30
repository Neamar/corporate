name: Bastion
markets:
    militaire: 2
    médias: 3
    énergie: 3
    transport: 2
datasteal: 10
sabotage: 10
extraction: 30
detection: 30
on_first:
    update('bastion', 1)
    update('tlaloc', -1)
on_last:
    update('bastion', -1)
    update('tlaloc', 1)
on_crash:
    update(ladder[0], 1)
    update('taurus', 1)
    update('impulse', -2)
    update('tlaloc', 2)

> *Solvendum nodum per gladium* 

Bastion est issue d’une union unique entre un fond d’investissement et plusieurs sociétés privées de sécurité. Corporation à la réputation sordide, Bastion est probablement l’une des mégas les moins soucieuses de son image auprès du public. 

Que vous l'aimiez ou que vous la haïssiez, Bastion sait que lorsque les choses tourneront mal, vous la supplierez d’intervenir. De son QG de Washington DC, le conseil de Bastion impose une vision du monde basée sur un interventionnisme assumé et la mise en place de la solution la plus pragmatique. Ses activités varient de la production d’énergie à bas coût faisant fi des normes environnementales à la diffusion de propagande dans les pays instables en passant par la fabrication d’armes chimiques par des usines aux conditions déplorables ou la production de véhicule de hautes sécurité (transports de troupe ou de fonds). 

De manière générale, Bastion est réputée pour mettre régulièrement l’éthique de côté et de ne laisser parler que les résultats. Déployant la force armée privée la plus puissante du monde, Bastion peut compter à la fois sur des forces spéciales d’élite augmentées, une multitude de milices armées à travers le monde et même son propre porte-avion : l’Alexandre. Cette présence permanente et sa capacité à agir sans compromis font de Bastion une puissance que nul ne peut regarder de haut.


## Effet premier
Profitant de sa position de premier, Bastion capitalise pour étendre sa vision du monde et renforcer ses positions. Tlaloc et ses alliés reculent face à la pression ultra moderniste.

* +1 actif pour Bastion.
* -1 actif pour Tlaloc.

## Effet dernier
Au fond du trou, les investisseurs de Bastion quittent le navire. Sa vision s'effrite avec ses actifs, profitant à Tlaloc et sa philosophie New Age.

* -1 actif pour Bastion.
* +1 actif pour Tlaloc

## Effet crash
Bastion perd définitivement le pari de l'interventionnisme. Sa chute propulse Tlaloc vers l'avant ainsi que Taurus Industries qui s'impose comme la nouvelle norme militaire. De nombreux projets militaires Impulse destinés au projet Mars sont abandonnés. Les meilleurs actifs de Bastion sont vendus au plus offrant.

* +1 actif pour la première corporation
* +1 actif pour Taurus
* -2 actifs pour Impulse
* +2 actifs pour Tlaloc

---

>Ah... Bastion... Ces gars-là, c'est des guerriers, qui ne lâchent rien sur le terrain comme sur les marchés. Ils tranchent dans le vif, droit au but. Pas de subtilités…  Et leurs putains de cyborgs… Bon dieu avec leurs implants de combat, ces gars font passer Terminator pour un enfant de cœur. J’en ai vu un soulever d’une seule main un écoterroriste de Tlaloc et l'éclater sur son genou à mains nues.

>Si tu veux bosser pour eux, t’as intérêt à montrer que t’es le plus grand salopard que la Terre ait jamais connu et que t’es prêt à foutre tes mains dans la merde et tes pieds dans des gueules. Personne ne les aime mais tout le monde les respecte, je peux comprendre pourquoi : il faut bien admettre qu’ils sont les meilleurs à ce qu’ils font.

>Alors si tu vas leur chercher des noises, assure toi d’être équipé contre du gros calibre, ils n’hésiteront pas à tirer à la mitrailleuse lourde au milieu d’un hypermarché  bondé pour te choper. 
