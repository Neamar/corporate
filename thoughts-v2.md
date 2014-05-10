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
Suppression des spéculations sur produits dérivés.

## Citoyenneté corpo
Possible de s'affilier à une corpo au tour 0 : il faudra ensuite prendre la citoyenneté indiquée ou perdre 4 PV.
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


-----
# Lite Version
Les corporations ont :
* leur nombre d'actifs
* leur classement
* plus de valeur de défense spécifiques. Les chances de succès sont prises en compte uniquement dans les runs.

Acheter une part dans une corporation et les bénéfices que la corporation génère dépendent de sa position dans le classement :

|rank| Coût part| Dividendes |
|----|---------|--------|
| 1  |   2M    |  1M    |
| 2  |   1M4   |  700k  |
| 3  |   1M3   |  650k  |
| 4  |   1M2   |  600k  |
| 5  |   1M1   |  550k  |
| 6  |   1M0   |  500k  |
| 7  |   900K  |  450k  |
| 8  |   800k  |  400k  |
| 9  |   700k  |  350k  |
| 10 |   600k  |  300k  |

## Runs
Les run ont un prix fixe :

* Information 100k
* Sabotage    200k
* Datasteal   300k
* Extraction  400k

Le pourcentage de chance qu'elle passe est de `90%-10%` par autre run de même type ayant la même cible avec un minimum de 25%. 

    Trois personnes qui font un sabotage sur Horizon ont 70% de chance chacun.
    10 run de sabotage sur Horizon ont 25% chacune.

Pour info, statistiquement ça donne :

    nombre de run       1   2   3   4   5   6   7   8   9   10  11  12  13  14
    % de chance/run     90  80  70  60  50  40  30  25  25  25  25  25  25  25
    %total sur cible    90  160 210 240 250 240 210 200 225 250 275 300 325 350

## IC
L'influence corporatiste a un effet dès le tour où on l'achète. Le prix est de `indice actuel x 750K` (750 pour le niveau 2, 1m5 pour le niveau 3...)

## MDC
On a le triangle suivant :

* Vos parts dans les corporations vous rapportent comme si elle étaient un rang plus haut. Aucun effet sur la corpo au top Exemple : une part dans Renraku 5eme vous rapporterai 600k au lieu de 550k.
* Les corporations dans lequelle vous êtes majoritaires gagnent +1 actif
* Vous gagnez +3 Points de Victoire pour la fin de la partie

Et avec les effets des perdants qui est l'exact opposé :

* Vos parts vous rapportent comme si elles étaient un rang plus bas. Sans effet sur la dernière corpo. 
* Les corporations dans lequelles vous êtes majoritaires perdent un actif
* Vous perdez 3 points de victoire.
