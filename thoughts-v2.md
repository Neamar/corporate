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

---
# Alternative : Not so Lite Version
Chaque fixer a une valeur de base dans les différents types de runs.
Pour faire une run, on choisit un fixer, puis on mise pour augmenter les probas par paliers de 10%.
Le fixer réalisera autant de runs que sa connectivité lui permet, en prenant les mises les plus hautes.

En début de jeu, on n'a accès qu'à une dizaine de fixers.
À chaque tour, on peut "débloquer" un fixer donné pour un certain prix (tous les fixers sont publics, on en choisit juste un auquel on n'a pas encore accès).

Pas de limite sur le nombre de runs lancées par tour.
Une run échouée n'est pas remboursée, en revanche une enchère insuffisante l'est.
Pas de malus de timing.

Pour la protection, on ne passe pas par les fixers.
On peut juste payer sur une corpo pour la protéger d'un évènement donné (DS / E / S).
La valeur de base est la défense de la corpo, ce qu'on paie vient s'ajouter au dessus et ne peut pas dépasser 60% de protection.
Le palier est de 10k¥ * actifs / 10%.
Si A et B protègent à hauteur de 20% une corpo protégée de base à 10%, il n'y a qu'une protection à hauteur 20 + 20 + 10 = 50.


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

Une corpo ne peut pas gagner ou perdre plus de 4 actifs par tour par le biais de runs.

    Ares prend 2 sabotage (-4), 3 extraction (-3) et réussit 2 datasteal sur d'autres (+2), elle ne perd que 4 actifs au lieu de 5.

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

--------------
# Not So Lite Version

Même règles que Manahttan mais...

Evidences d'abbord : Un "MDC" triangulaire et une absence de produits dérivés.

Si on réduit le nombre de spéculations à 1, il faudrait une option pour spéculer sur plusieurs positions à la fois, avec une cote plus basse. Pour que ceux qui ne veulent pas se prendre la tête sur la spéculation puissent se la jouer safe.

Révision du prix de l'IC, mais suppression de la limite d'un point acheté par tour. Pas nécessaire, et ça empèche de rattraper son retard.

Les runs :

Précision : 50k pour 10 %. Maximum 100% après bonus (très important!). La défense, alllant de 10 à 30 %, se soustrait à la précision.
Un indice de Préparation, de 0 à 5 qui peut être décidé sans coût.
Bonus d'IC à 50%.
La thune dans les runs échouées est perdue.

Les runs de même type sur une même corpo sont résolues par ordre de Préparation croissante. Random en cas d'égalité, ou éventuellement priorité au plus haut score de Précision (pas fan).

Malus de timing de 20% pour les runs de sabotage, 40% pour Extraction et Datasteal. Il s'applique pour chaque run de ce type déjà réussie.

Possibilité de mettre des Protections sur une corpo dans laquelle on a au moins une part. Une protection coûte 200 k. Lors de la résolution du tour, une corpo aura x Protections sur elle. Les runs sont résolues dans l'ordre suivant : Sabotage, Extraction puis Datasteal. Tant que x>1, toute run qui passe a 70% de chance d'être contrée -10% par point de préparation. Si une run est contrée, on retire 1 à x. "Système cartouches".
Autre possibilité qui peut être viable : une unique protection par palier, qui diminue à chaque run bloquée.


Si un joueur a mis une protection sur une corpo, il en reçoit les détections comme s'il en avait la nationalité.

Voilà en gros pour la base. Plusieurs options pour le reste.

Pour les runs, soit :

* 2 fois plus de bonus d'IC à chaque tour, en réajustant peut-être le bonus.
* Des fixers.

Pour les fixers : une douzaine avec des score en Datasteal ( comptant eventuellement pour les runs d'Information), Sabotage et Extraction. Bonus allant de +10 à +50%.

Possibilité de choisir un fixer pour booster sa run. Si le fixer "refuse", la run se fait quand même, mais avec un malus de 10%.

Chaque tour, les joueurs, peuvent acheter des points de Loyauté. Chaque achat est un ordre distinct. Le prix est de 100k, plus 100k par point déjà acheté ce tour ci. Le premier à 100k, le second à 200k, le troisième à 300k... peu importe qu'ils soient tous achetés dans le mêmes fixer ou non. Annuler l'achat d'un point annule tous les autres, sauf si coût des autres points peut être recalculé. A voir.

Un fixer ne peut soutenir qu'une run par tour. Il donne la priorité au joueur qui y a le plus de points de Loyauté. En cas d'égalité, la run qui a la plus haute précision. Puis random.
Autre options : moins de fixer, mais ils peuvent soutenir 2 runs par tour ou plus. Ca me parait plus compliqué, cela dit.

Les fixers ont des alliés et des ennemis.

Alliés :
Ils refusent les runs qui ciblent la corpo.
Les Johnsons citoyens de la corpos comptent comme ayant un point de Loyauté supplémentaire.

Ennemis :
Ils refusent toutes les runs proposées par les citoyens de la corpo.

Si on fait tout ça, la hard limit de +4/-4 me parait superflue. Un malus de timing de 40% sur les datasteal, c'est raide.

Information, mère de toute stratégie. Volet crucial s'il en est.

J'ai quelques idées, mais je préfererai qu'on en cause plus longuement avant de rentrer dans le détail. En gros, je suis pour :

* Supprimer les runs d'Information.
* Donner aux joueurs le choix d'investir dans une carac Renseignement similaire à l'IC, qui est boostée d'une manière ou d'une autre par la Détéction de la corpo du joueur.
* Les joueurs choisissent les joueurs sur lesquels ils veulent se renseigner. Ils reçoivent des informations partielles sur les fiches ordres, loyautés et secrets des joueurs ciblés. La quantité d'information reçue dépend du Score de Renseignement, de la défense Datasteal des joueurs ciblés et le nombre de joueurs ciblés.

Quelques idées de plus qui me paraissent interessantes :

* Lorsque la ligne Opération clandestine passe, toutes les corpos perdent un actif.
* A chaque corpo est associée une coalition. Un joueur citoyen de la corpo pèse +1 quand il rejoint la coalition corespondant à sa corpo.
* Au début du jeu, chaque joueur reçoit un allié et un ennemi parmi les joueurs. Réciproques, donc ça marche qu'avec un nombre pair de joueur. On laisse le temps à ceux qui veulent se mettre d'accord, et le reste est tiré random. -3 points si un allié termine dans les 3 derniers en fin de partie. -3 si un ennemi termine dans les 3 premiers. Possiblement plus graduel, tu as compris l'idée. Fait partie des Secrets.

D'autres idées dont je ne suis pas trop sur, mais qui méritent d'être mises sur la table :

* Les joueurs reçoivent des bonus à leurs runs correspondants aux Défense des corpos dont ils sont citoyen.
* Des effets randoms qui twistent le jeu pour un tour, placés en secret à des tours random. Possibilité de se renseigner sur la nature du prochain event, et, séparément, sur le tour auquel il arrive. Exemple d'event : Deux corpos entrent en guerre ouverte. Celle qui termine le tour au dessus de l'autre gagne 2 actifs, l'autre en perd 2.
* Des "groupes" dans lesquels il est possible d'acheter des points pour gagner +10% par point dans les runs associées pour le reste de la partie / réduisent le coût de la Protection. Police, pegre, agences d'espionage...
Des CROCs, qui fonctionnent en gros comme un fixer perso.

Un autre système complètement diférent pour les runs. Beaucoup plus simple d'un point de vue prog', mais beaucoup plus chiant à apréhender pour les joueurs. En gros je suis pas pour, mais je te le donne quand même :

Pas de Préparation, et elles se résolvent toutes en même temps. On garde le malus de timing actuel. Les joueurs peuvent payer 50k pour ajouter 10% de Protection à la corpo. La Protection est soustraite au % de toutes les runs sans distinction de type, mais est réduite de 10% pour chaque tranche de 30% de précision dirigée contre la corpo. Le malus sur une même run ne peut pas dépasser -50%.
