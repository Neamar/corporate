# CG 4

## Runs
### Fixers
On définit une nouvelle entité capable de réaliser des runs.
Un **fixer** se définit par :

* Son pourcentage en Extraction
* Son pourcentage en Datasteal (et Information)
* Son pourcentage en Sabotage
* Son prix de base
* Sa valeur de connectivité
* Ses corporations alliées
* Ses corporations ennemies

### Mises
Les joueurs peuvent miser une fois par IC et par type de run sur un fixer pour lui faire réaliser une run (donc au début une mise sabotage, une mise datasteal, une mise information, une extraction et une protection). Le joueur avec la plus grosse mise remporte le fixer et émet une run avec le pourcentage de chance du fixer. *Le second plus haut miseur remporte une run avec pourcentage - 10%, etc.* Au total, le fixer peut envoyer autant de run que sa connectivité.

* La mise minimum est la connectivité multipliée par 100k.
* Le malus de timing reste présent.
* Une run n'est pas maxée à 90%

Un fixer n'attaquera jamais une corporation dont il est l'allié.
En revanche, il donnera la priorité à un Sabotage sur une corporation ennemie.

### Runs de protection
Un fixer peut aussi réaliser une run de protection. Sa valeur en protection est sa valeur d'attaque divisée par deux (Sabotage de 70% => protection de 35%).
La valeur de protection vient s'additionner avec la valeur de base des corpos (plutôt qu'en complément). Dans tous les cas, elle ne peut pas dépasser 60% de protection.

## Spéculation
Une seule spéculation par tour, de valeur max `200 * IC`.

## Citoyenneté corpo
Impossible à prendre au tour 0.
PV : -6 + tour de prise de citoyenneté
-6PV si pas de citoyenneté corpo en fin de jeu
Augmenter les points de citoyenneté en fin de jeu.

## IC
Prix IC : 750k¥ pour IC2, ensuite double à chaque fois

| IC | Coût       |
|----|------------|
| 2  |  750k      |
| 3  |  1500      |
| 4  |  3000      |
| 5  |  6000      |


## Vote
Le vote est séparé en deux ordres distincts (un +, un -)

## MDC
Le calcul des voix n'inclut que les parts actuelles, pas les changements de majorité potentiels pendant le tour.

Système triangulaire :

* **Opérations Clandestines** : +20% de succès sur runs, -20% sur CPub
* **Contrats Publics** : +1 actif sur corpos majoritaires, -1 actif sur corpos de Consolidation
* **Consolidation** : +3PV, -3PV opérations clandestines

## Dividendes
Les dividendes de la dernière corpo sont de `40 * actifs`.

## Wiretransfer
Affiche une popup de validation "définitive"

## Effet crash
Une corporation qui crashe applique un effet spécial sur les autres corpos, plus puissant que les effets premiers derniers.

## Points de Victoire

* Une spéculation n'est réussie que si misée à son niveau max
* 7 tours de jeu uniquement, au lieu de 8.
* Les runs d'Information ne comptent que sur joueur distincts.
* Le titre Opportuniste disparaît
