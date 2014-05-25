# CG 4

## Classement des corporations
Cinq "marchés" sont définis sur le jeu, par exemple "Militaire", "Transport", etc.

Chaque corporation possède des actifs dans certains marchés en début de jeu. Elle a 2 "interdictions" de marché et un marché "principal".

## Runs
Les runs ont un coût de base de 350k¥ pour 50%, puis coûtent 50k¥ / 10% additionnels.

Le coût de base est annulé pour autant de runs que l'on a d'IC.
Les runs sont résolues par précision décroissantes.

### Sabotage
Cible un marché et une corpo. Ne peut passer qu'une fois par marché / corpo / tour. -2 actifs, sans descendre en dessous de 0.

### Extraction
Cible un marché et deux corpos. Ne peut passer qu'une fois par marché / corpo / tour. -1 actif / +1 actif. Si la cible a 0 dans le marché, échec.

### Datasteal
Cible un marché et deux corpos. Ne peut passer qu'une fois par marché / corpo / tour. +1 actif. Si la cible a 0 dans le marché, échec.

### Protection
Cible un marché et une corpo. La protection permet de diminuer la précision maximum des runs attaquantes. Contrairement aux autres runs, elle part à 90% et il faut payer pour descendre (le prix de base reste de 250k¥).

Coût Protection (+ prix de base)      50k¥   100k¥   150k¥   200k¥
Valeur maximale des runs attaquantes  80%    70%     60%     50%

Toute run de précision supérieure est maxée par la valeur de protection.

### Information
Coût de base 0, 50k¥ par palier de 10%, maximum 50%.

Donne accès à N% des logs "globaux" (tout compris : main invisible, runs, vote, ...)

## Spéculation
Une seule spéculation par tour, de valeur max `200 * IC`.
Suppression des spéculations sur produits dérivés.

## Citoyenneté corpo
Possible de s'affilier à une corpo au tour 0 : il faudra ensuite prendre la citoyenneté indiquée ou perdre 4 PV. Devient inactif si plusieurs joueurs ont pris la même corpo.

PV : -6 + tour de prise de citoyenneté, ou -6PV si pas de citoyenneté corpo en fin de jeu
Les joueurs citoyens de la première corpo gagnent 16PV, puis 14, 12...
Deux personnes dans la même corpo prennent -6.

## IC
Prix IC : 750k¥ * indice actuel

## Vote
Le vote est séparé en deux ordres distincts (un +, un -)

## MDC
Le calcul des voix n'inclut que les parts actuelles, pas les changements de majorité potentiels pendant le tour.

Système triangulaire :

* **Opérations Clandestines** : à définir
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
* Le titre Opportuniste passe à 5PV
