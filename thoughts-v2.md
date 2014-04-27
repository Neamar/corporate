# Changements entre la v1 et la v2

## Runs
Chaque type de run a un pool de runners attitrés : par exemple, pour le Sabotage, des runners à 90%, 80%, 70%, 60%.

On doit miser sur ces runners ; par exemple "je mise 700k¥ pour que les runners à 90% fassent ma run". Celui qui a l'enchère la plus élevée sur ces runners remporte la run pour le tour. On peut miser autant de fois que l'on a d'IC par type de run (donc au début une mise sabotage, une mise datasteal, une mise information, une extraction et une protection).

Une même mise cumulée remporte l'enchère (par exemple, le joueur A paie 500k¥ pour saboter Horizon. B paie 400k¥ pour saboter Ares, C paie 300k¥ pour saboter Ares : A perd l'enchère, et les runners récupèrent l'argent de B et C pour aller contre Ares).

* La mise minimum est de 50k¥.
* Si notre enchère échoue, on perd quand même 10% de la mise (frais de dossier).
* Si la run échoue, on est remboursé à 50%.
* Le malus de timing reste présent.
* Le système est le même pour les runs de protection, qui passent par enchère. * La valeur de protection vient s'additionner avec la valeur de base des corpos (plutôt qu'en complément). Dans tous les cas, elle ne peut pas dépasser 60% de protection.

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
