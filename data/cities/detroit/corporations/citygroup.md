name: CityGroup
markets:
    BTP: 2
    télécom: 3
    énergie: 3
    transport: 2
datasteal: 10
sabotage: 10
extraction: 10
detection: 90
on_first:
    update(ladder[1], 1)
    update(ladder[-1], -1)
on_last:
    update('taurus', -1)
    update('citygroup', 1)
on_crash:
    update(ladder[1], -1)
    update('taurus', -3)
    update('iris', 2)
    
> *Construire aujourd’hui les villes de demain*

CityGroup est une corporation jeune basée à Détroit. Son fondateur a déployé une fortune extraordinaire et déployant un matériau unique, le biobéton. Issu d’un procédé complexe, ce matériau gardé secret permet de convertir les déchets organiques en une matrice idéale pour la construction d’immeuble : facile à mettre en œuvre, léger et surtout, peu cher. Bien que d’une odeur exécrable, d’une isolation sonore faible et d’un aspect peu attrayant, ce matériau répondait tout simplement à un double besoin : la gestion des déchets et une population mondiale toujours croissante cherchant à se loger à bas prix. 


Aujourd’hui, les 3 milliards de personnes qui vivent dans des barres d’immeubles en biobéton ont toutes CityGroup à remercier. C’est ce produit phare qui a ensuite permis à CityGroup de récolter une myriade de contrats gouvernementaux ayant abouti à une diversification de son activité tout en restant dans sa vision initiale de voir de l’or là où tous voient de la fiente et s’adresser aux plus modestes : transport en commun, vitres panneaux solaires, relais de télécommunication, 


CityGroup n’est pas sur les panneaux d’affichage ou dans vos écrans 3D, un tiers de la population mondiale leur verse simplement un loyer.


## Effet premier
CityGroup surfe sur son avantage concurrentiel pour créer des infrastructures et trouver de nouveaux alliés puissants. De plus, elle impose une guerre des prix, empêchant les corporations en difficulté de remonter la pente.

* +1 actif pour la deuxième corporation.
* -1 actif pour la dernière corporation.

## Effet dernier
Fier de son aptitude à trouver de bonnes opportunités même dans les situations les plus désespérées, CityGroup trouve le moyen de regagner un second souffle. Néanmoins, l'infrastructure des villes diminuant, les options de transport en souffrent autant, imposant un ralentissement à Taurus Industries.

* -1 actif pour Taurus.
* +1 actif pour CityGroup.

## Effet crash
CityGroup chute et ses infrastructures s’effondrent. Taurus Industries souffre particulièrement, ses transports n'étant plus aussi bien managés. Iris réalise une campagne de médiatisation mettant en scène la chute de CityGroup comme la mort d'un héros populaire, faisant grimper l'audimat.

* -1 actif pour la deuxième corporation.
* -3 actifs pour Taurus.
* +2 actifs pour Iris.

---

>Tu vois ce taudis dans lequel on vit. Tu sais qu’avant les villes ne sentaient pas en permanence cette odeur de merde… Mais regarde maintenant, tout le monde a de quoi se loger. Tout le monde peut vivre en ville dans un appartement dégueulasse pour profiter des plaisirs urbains qu’ils ne peuvent pas se payer. 

>Et c’est CityGroup qui orchestre tout ça. Ces fumiers bossent avec tous les gouvernements : des moutons bien parqués sont plus faciles à gérer hein ? Quoi ? Oui ben franchement le biobéton c’est dégueulasse… Et ça me gave de voir mon loyer arriver sur les comptes de ces salauds. 

>Si tu vas pour les faire chier, prépare-toi, ils ont des alliés politiques et gouvernementaux encore mieux placé que les autres corpos. En plus, on dit qu'ils ont un étrange partenariat avec Iris pour contrôler les masses… Et ça marche drôlement bien…
