# Changements entre la v1 et la v2

## Runs
### Fixers
On défnit une nouvelle entité, les fixers, capable de réaliser des runs.
Un fixer se définit par :

* Son pourcentage en Extraction
* Son pourcentage en Datasteal (et Information)
* Son pourcentage en Sabotage
* Son prix de base
* Ses corporations alliées
* Ses corporations ennemies

### Mises
Les joueurs peuvent miser une fois par IC et par type de run sur un fixer pour lui faire réaliser une run (donc au début une mise sabotage, une mise datasteal, une mise information, une extraction et une protection).. Le joueur avec la plus grosse mise remporte le fixer et émet une run avec le pourventage de chance du fixer. Le second plus haut miseur remporte une run avec pourcentage - 10%, etc. Seule exception : si la mise d'un joueur est deux fois inférieurs au miseur directement supérieur, le fixer ne prend même pas la peine d'envoyer la run.

* La mise minimum est le prix de base du fixer. Ensuite, il faut miser par incrément sur le prix de base (pour un prix de base de 150k¥, on peut miser 150, 300, 450...)
* Si la run échoue, on est remboursé à 50%.
* Le malus de timing reste présent.

Un fixer n'attaquera jamais une corporation dont il est l'allié. En revanche, il donnera la priorité à un Sabotage sur une corporation ennemie.

# Runs de protection
Un fixer peut aussi réaliser une run de protection. Sa valeur en protection est sa valeur d'attaque divisée par deux (Sabotage de 70% => protection de 35%).
La valeur de protection vient s'additionner avec la valeur de base des corpos (plutôt qu'en complément). Dans tous les cas, elle ne peut pas dépasser 60% de protection.

## Spéculation
Une seule spéculation par tour, de valeur max `200 * IC`.

## Citoyenneté corpo
Impossible à prendre au tour 0.
PV : -6 + tour de prise de citoyenneté
-6PV si pas de citoyenneté corpo en fin de jeu

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

Contrôles Ciblés est renommé en XXX ?

## Dividendes
Les dividendes de la dernière corpo sont de `40 * actifs`.

## Wiretransfer
Affiche une popup de validation "définitive"

## Points de Victoire

* Une spéculation n'est réussie que si misée à son niveau max
* 7 tours de jeu uniquement, au lieu de 8.
* Les runs d'Informations ne comptent que sur joueur distincts.
* Le titre Opportuniste disparaît
