title: Comment jouer ?

Vous incarnez un cadre corporatiste décidé à se tailler un empire dans une des places financières les plus concurrentielles du 6<sup>ème</sup> monde : l'île de Manhattan.

[TOC]

## Concepts de base
Les **corporations, ou "corpos"**, sont au coeur du jeu. De gigantesques multinationales qui ont supplanté le pouvoir des nations et fait main basse sur l'économie planétaire. Elles sont innombrables, mais le Corporate Game ne tient compte que des dix plus grosses s'étant implantées à Manhattan.

La taille de ces dix corpos est représentée par leur nombre d'**actifs**, qui évoluera en fonction des actions des joueurs et des caprices de la bourse.

Plus une corpo possède d'actifs, plus elle engrange de bénéfices. Au début de la partie, les actifs des 10 corpos sont tirés au hasard (entre 7 et 12). ([cf. Classement initial](rules.md#classement-initial))

Le **classement** trie les corpos par nombre d'actifs et leur attribue un rang de 1 à 10, 1 correspondant à la corpo possédant le plus d'actifs, celle qui domine le marché.

Chaque corporation voit ses actifs répartis en quatre **marchés**. 

> Par exemple, Ares possède 10 actifs répartis comme suit :
>
> * 5 en Militaire
> * 2 en Alimentaire
> * 3 en Sécurité
> * 0 en Magie

Ces marchés sont définis au début de la partie. Une corporation ne pourra donc jamais ouvrir un marché dans lequel elle n'est pas compétente (en tout cas, pas dans cette ville ni dans cette partie). 
Chaque corporation a un **marché historique**, qui est ciblé par certains effets de jeu.
Au total, il existe 10 marchés différents répartis entre les corporations. Chacune possède un marché historique différent.

Si une corporation a plus d'actifs que toutes les autres sur un marché, elle **domine** ce marché et gagne un actif. Attention cependant, cet actif est perdu dès l'instant où la corporation ne domine plus le marché. En cas d'égalité, aucune corpo ne domine.

Les joueurs commencent la partie avec 1 point d'**Influence corporatiste**, ou **"IC"**. Cette caractéristique représente l'étendue de leur pouvoir et de leurs réseaux dans l'île de Manhattan et sert de limite à certaines de leurs actions. Elle pourra être augmentée en cours de partie.

Pour leur permettre de démarrer, chaque joueur reçoit au début du jeu 2 millions de **nuyens (ny)**, la monnaie globale du 6<sup>ème</sup> Monde.

La partie se joue en 8 **tours**, chaque tour correspondant à un trimestre. À la fin du jeu, chaque joueur compte ses **points de victoire**, et celui qui en possède le plus est déclaré vainqueur. ([cf. Fin du jeu](endgame.md))

## Structure d'un tour
Chacune des étapes suivantes sera expliquée en détails.

1. Chaque joueur remplit et envoie un **formulaire d'ordres**, où il peut effectuer des achats, spéculer et manipuler le marché.
2. À midi chaque jour jusqu'à la fin du jeu, les ordres sont tous résolus simultanément, faisant gagner et perdre des actifs aux corpos.
3. Chaque corpo est différente et possède un **effet premier** qui s'applique lorsque la corpo est en tête du classement et un **effet dernier**, qui s'applique lorsque qu'elle est dernière. Les deux effets sont résolus simultanément, une fois tous les autres modificateurs appliqués.
4. Chaque joueur touche ses divers retours sur investissements.
5. Les onglets **Wall Street** et **Newsfeeds** révèlent respectivement le nouveau classement et les évènements publics du tour écoulé, et chaque joueur reçoit en plus un **message de résolution** personnalisé qui contient les informations plus confidentielles.

Un nouveau tour peut commencer.

## Comment ça marche ?
À chaque tour, les joueurs peuvent acheter des **parts** dans les corpos de leur choix. Le nombre maximum de parts qu'un joueur peut acheter par tour est égal à son IC (Influence Corporatiste, de 1 au début du jeu).

Une part coûte `100 000 ny × (actifs de la corpo)`. Soit 500 000 ny pour une corpo de 5 actifs. 

> Une part dans la corpo en tête du classement (rang 1) coûte `125 000 ny × actifs` pour joueurs qui n'en ont pas la "nationalité" ([cf. Citoyenneté corpo](rules.md#citoyennete-corpo)).

À la fin de chaque tour, les joueurs touchent les **dividendes** de leurs parts. Chaque part rapporte à son propriétaire `50 000 ny × (actifs de la corpo)`. Un joueur possédant 2 parts dans une corpo de 5 actifs et 1 part dans une corpo de 10 actifs touchera donc `2 × (50 000 × 5) + 1 × (50 000 × 10)`, soit 1 million de ny.

> Les parts de la corpo en tête du classement rapportent `75 000 ny × actifs`.

## Évolution du marché
À chaque tour, les corpos vont gagner et perdre des actifs. Ce n'est qu'après toutes les modifications effectuées que sont calculés les dividendes.

### Les Votes
En tant qu'acteur majeur du marché, chaque joueur a droit à un **Vote** par tour. Il choisit :

* Un marché d'une corpo qui gagne 1 actif.
* Un marché d'une corpo qui perd 1 actif.

### La main invisible du marché
Le reste des aléas de la bourse de Manhattan est laissé à la chance. À chaque tour :

* Une corpo au hasard gagne 1 actif sur son marché historique.
* Une corpo au hasard perd 1 actif sur son marché historique. Le marché ne peut pas tomber en dessous de 0.

### Effet premier / effet dernier
Les effets premier et dernier des corpos en tête et en fin de classement s'appliquent chaque tour, après tous les autres modificateurs, et viennent chambouler les actifs des corpos en s'appliquant sur leurs marchés historiques.

Voir la page des corporations pour une description individuelle de chaque corpo et [le recap](recap.md) pour une liste de leurs effets premiers / derniers. 

### Crash
Au cours de la résolution du tour, une corpo peut descendre à 0 actifs ou moins. Son effet dernier peut tout de même s'appliquer, mais si elle n'est pas remontée à au moins 1 actif à la fin de la résolution, elle **Crashe** et est définitivement retirée du classement. Pas de remboursement pour les parts investies.

## Achat d'Influence
Les joueurs peuvent payer pour augmenter leur Influence Corporatiste d'un point. Le coût est de `750 000 ny × indice`, soit 1 500 000 ny pour passer de 2 à 3. 

La nouvelle valeur d'IC ne prendra effet qu'au tour suivant.

## Citoyenneté corpo
Dans le sixième monde, les corporations ont tellement de pouvoir qu'elles sont de véritables états, avec leurs propres lois et leur propres citoyens. À chaque tour, un joueur peut réclamer la citoyenneté d'une corpo dans laquelle il possède au moins une part.

Un **citoyen corpo** :

* Gagne davantage de points de victoire si sa corpo est bien placée dans le classement à la fin de la partie ([cf. Fin du jeu](endgame.md#points-de-citoyen)).
* Paie les parts de sa corpo au prix usuel de `100 000 ny × actifs` même si elle est en tête du classement (au lieu de `125 000 ny × actifs`).

Changer de nationalité corpo coûte au joueur un nombre de points de victoire égal au double du tour en cours, soit -12 s'il change de nationalité au tour 6. Il est possible de commencer la partie avec une nationalité corporatiste ([cf. Mise en place](start.md#citoyennete-corpo)).

A la fin de la partie, si un joueur n'a pas de nationalité corpo, il perd 6 points de victoire.

Si la corpo dont le joueur est citoyen Crashe, il en perd la citoyenneté et pourra s'il le souhaite en réclamer une nouvelle au tour suivant. Il subit normalement le malus de points de victoire.

## Runs
Les requins corpos ont tendance à ne pas jouer selon les règles. Pour manipuler le marché et gagner un avantage sur la concurrence, ils n'hésitent pas à engager des agents indépendants, appelés shadowrunners, pour effectuer toutes sortes d'opérations clandestines, ou shadowruns. **Runs**, pour les intimes.

Il existe 5 type de runs : **Datasteal**, **Sabotage**, **Extraction**, **Information** et **Protection**. Elles ont chacune des résultats spécifiques, coûtent 350 000 ny et ont 50% de chances de réussir. Le joueur **commanditaire** peut augmenter les chances de réussite de sa run à raison de 50 000 ny pour 10% supplémentaires. Un joueur qui investit 400 000 ny dans une run de Sabotage aura donc 60% de chance de la voir réussir (`50% de base + 1 × 10%`).

Le pourcentage de chances maximum qu'une run peut atteindre est de 90%. Ce chiffre peut être baissé par les runs de protection.

Pour chaque point d'IC qu'il possède, un joueur peut réduire le coût de base d'une run à 50 000 ny (au lieu de 350 000 ny).

Les runs sont résolues par % de réussite décroissants. Donc une run qui a 70% de chances de réussir passera toujours avant une run qui a 60% de chances de réussir.

Un run cible un marché au sein d'une corpo. Une seule run de chaque type peut passer par cible. 

Exemple :
Jules, Mathieu et BOM cherchent à lancer une extraction sur le marché 'Militaire' de Renraku.
-Jules lance une run à 70% de chances de réussite avec son bonus d'IC (50 000 ny de coût de base + 100 000 ny d'améliorations)
-Mathieu lance une run à 60% de chances de réussite sans son bonus d'IC qu'il a utilisé pour une autre run (350 000 ny de base + 50 000 ny d'amélioration)
-BOM lance une run à 50% de chances de réussite avec son bonus d'IC (50 000 ny de coût de base)



### Défense
Les corporations n'apprécient pas particulièrement d'être la cible de runs, et investissent des sommes colossales dans leur sécurité. Vous pouvez lancer une run de protection sur un marché d'une corporation pour réduire le pourcentage de chances que les runs passent. Son coût de base est de 350 000 ny comme les autres run et plus vous payez, plus le pourcentage de chances maximum que les runs réussissent est diminué.

| Coût Protection                      |  50k¥ | 100k¥ | 150k¥ | 200k¥ |
|--------------------------------------|-------|-------|-------|-------|
| Valeur maximale des runs attaquantes |  80%  |  70%  |  60%  |  50%  |


### Détection
En plus de leurs indices de Défense, les corpos possèdent un indice de **Détection** (30 pour Renraku). Ce nombre correspond au pourcentage de chances que la corpo détecte les runs qui la ciblent. Une run détectée est déclarée dans le message de résolution de tous les citoyens de la corpo ciblée avec tous les détails ; bénéficiaire, commanditaire et chances de réussite inclus.

Une run détectée sera également mentionnée dans les Newsfeeds de fin de tour, mais sans davantage d'information que la corpo ciblée.

> Les runs de Protection ne sont jamais détectées.
> Les runs de Sabotage réussies sont particulièrement voyantes, et apparaissent dans les Newsfeeds même si elles n'ont pas été détectées.
> Même détectées, les runs d'Information ne font pas de vagues et ne sont pas révélées dans les Newsfeeds.

### Malus de timing
Lorsque plusieurs équipes de shadowrunners sont engagées pour des runs similaires, elles risquent d'entrer en concurrence et de se marcher sur les pieds.

Une run subit un malus de **-10%** pour chaque autre run qui **correspond aux 3 critères** suivants :

* Est du **même type** (Datasteal, Sabotage, Extraction ou Information).
* A la **même cible**, joueur ou corpo.
* A un **pourcentage de réussite supérieur ou égal** au sien (avant que les malus de timing ne soient appliqués).

> Les runs de Protection n'entrent pas en concurrence.

    2 runs de Sabotage (même type) sont lancées contre Renraku (même cible) le même tour.
    Si elles ont toutes les deux 70% de chance de réussite, chacune fait subir à l'autre un malus de timing de -10%.
    En revanche, si la première a 80% de chance de réussite et la seconde 70%, seule la seconde subit un malus.


### Les types de runs
#### Datasteal
* Base : 30 %

Le commanditaire choisit une **corpo cible** et une **corpo bénéficiaire**. En cas de réussite, la corpo bénéficiaire gagne **+1 actif** grâce aux précieuses informations dérobées à la concurrence.

#### Sabotage
* Base : 30 %

Le commanditaire choisit une **corpo cible**, et tente de saboter une de ses opérations. En cas de réussite, la corpo subit **-2 actifs**.

> Qu'elles aient été détectées ou non, les runs de Sabotage réussies sont révélées dans les Newsfeeds.

#### Extraction
* Base : 10 %

Le commanditaire choisit une **corpo cible** et une **corpo bénéficiaire**. En cas de réussite, un employé crucial est kidnappé des locaux de la corpo cible, qui subit **-1 actif**, et rejoint la corpo bénéficiaire, lui faisant gagner **+1 actif**.

#### Information
* Base : 60 %

Le commanditaire choisit un **joueur cible**. En cas de réussite, une enquête approfondie lui fournit tous les **messages de résolution** du joueur ciblé depuis le début de la partie (à l'exception des éventuels résultats de runs d'Information), ainsi que ses **Secrets** ([cf. Secrets](start.md#secrets)).

> La Défense de Datasteal de la corpo dont la cible est citoyen est utilisée pour contrer les runs d'Information.
> Même détectées, les runs d'Information n'apparaissent pas dans les Newsfeeds.

#### Protection
* Base Datasteal : 40 %
* Base Sabotage : 0 %
* Base Extraction : 10 %

Le commanditaire choisit une **corpo bénéficiaire**, et lui attribue une Défense supplémentaire en Datasteal, Sabotage ou Extraction. Cette seconde Défense s'applique en complément de celle de la corpo (elles ne s'additionnent pas, elles s'enchaînent), et ne peut pas dépasser 50%. Il est possible de lancer plusieurs Protections similaires sur une même corpo.

    Jack Finn, un requin sans scrupule, désire effectuer une Extraction contre Renraku, la corpo de son rival Shiro Kuboka, afin de booster les actifs d'Horizon dans laquelle il a largement investi.

    Il paye 250 000 ny pour ajouter 50% de chance de réussite à sa run, et utilise un de ses bonus d'IC pour 30% supplémentaire. Sa run a donc 90% de chance de réussite (10% de base + 50% de ny + 30% de bonus d'IC).

    Shiro Kuboka, devinant la manoeuvre, paye 50 000 ny pour organiser une Protection en Extraction en faveur de Renraku. Il ajoute un de ses propres bonus d'IC pour atteindre 50%, (10% de base + 10% de ny + 30% d'IC ; 50 % étant le maximum pour une Protection).

    Test de réussite de l'Extraction, 90% : réussite
    Test de Défense de Renraku contre les Extractions, 20% : échec
    Test de la Protection de Shiro Kuboka, 50% : échec
    Test de Détection, 30% : réussite

    Un scientifique de renom est arraché à son laboratoire. Renraku perd 1 actif, Horizon en gagne 1. La run a cependant été détectée, et tout Manhattan est au courant qu'elle a eu lieu, sans savoir que Jack Finn est son commanditaire ou qu'Horizon en a bénéficié. Shiro Kuboka, en revanche, est citoyen de Renraku, et apprend donc l'ensemble de la vérité. Maudissant l'incompétence de ses employés, il rassemble ses fonds pour un Sabotage bien senti contre Horizon...

## Spéculation
Les investissements à long termes sont cruciaux pour bâtir un empire corporatiste, mais les cadres endurcis savent qu'il y a beaucoup d'argent à faire en spéculant à court terme sur les remous du marché. 

Les joueurs qui veulent miser dans le grand casino de l'East Coast Stock Exchange peuvent effectuer une **spéculation**. Le montant de cette spéculation ne peut dépasser `200 000 ny × (IC du spéculateur)`.

Dans sa spéculation, le joueur choisit une corporation et mise sur son classement en fin de tour.

Si le spéculateur se trompe, il perd la somme misée.

Si sa spéculation est juste, il fait un bénéfice d'une côte de :

* **1 pour 3** s'il a spéculé qu’une corpo finirait le tour **première ou dernière**. (S’il a placé 100 000 ny, il les conserve et gagne 150 000 ny suplémentaires)
* **1 pour 5** s’il a spéculé qu’une corpo finirait le tour à un autre rang (**de seconde à avant-dernière**) .

> Si deux corpos ont des actifs négatifs (et crasheront donc en fin de tour), la corpo étant le plus loin dans le négatif est considéré dernière.

### Produits dérivés
Un produit dérivé est la somme des actifs d'un ensemble de corpos. 

* Le **Nikkei** (indice de Bourse de Neo Tokyo) est la somme des actifs des corpos Sony, Shiawase et Renraku
* Le **Dow Jones** est la somme des actifs d'Ares, Neonet, Spinrad et Prometheus.

> Si une corporation crashe dans un produit dérivé, elle n'est pas remplacée.

    Jack Finn a la ferme intention de faire travailler son argent. Ayant une IC de 2, il effectue deux spéculations :
    
    * 200 000 ny sur une chute du Nikkei. Après tout, il a un sabotage prévu sur Renraku...
    * 100 000 ny sur la position d'Horizon, dont il pense qu'elle sera 2ème à la fin du trimestre.

    Son sabotage échoue, et la Bourse de Néo Tokyo croît de 2 actifs ce trimestre. Il ne reverra pas ses 200 000 ny.
    Horizon, malgré une Extraction vicieuse, finit en seconde position. Il garde ses 100 000 ny et en touche 400 000 de plus qui le font largement rentrer dans ses frais.


## Le Manhattan Development Consortium
Le MDC (Manhattan Development Consortium) n'est pas exactement une corporation, mais la structure à travers laquelle des corpos se sont alliées pour coordonner la reconstruction, assurer l'extraterritorialité de Manhattan et partager sa gouvernance entre ses membres. Cet équivalent corporatiste d'un conseil municipal tente de maintenir un contrôle absolu sur presque toutes les activités de Manhattan.

Les corpos membres ont changé plusieurs fois depuis la fin de la reconstruction. Aujourd'hui, elles sont dix, et ont chacune une voix lors des votes du consortium. Ces votes légifèrent sur tous les aspects de la vie et des affaires à Manhattan, des juteux contrats de la voirie, de la sécurité, du traitement des déchets ou du développement de la matrice aux lois de régulations des marchés qui ont le potentiel de bouleverser le cours des actions des corpos les plus stables. Les votes du MDC rythment la vie politique de Manhattan, et sont disputés par des coalitions fluctuantes qui ne reculent devant aucun coup bas pour rafler la mise.

Chaque tour, les joueurs peuvent participer au cirque du MDC en rejoignant une **coalition** défendant une cause particulière. Ces causes, détaillées plus bas, peuvent être une redistribution des **Contrats publics**, une restriction des **Opérations Clandestines** ou des **Consolidations**.

Le joueur qui possède **le plus de parts** dans une corpo peut influencer ses décisions politiques : la corpo rejoint la même coalition que lui.

> En cas d'égalité sur le nombre de parts possédées, la corpo reste neutre. 

La coalition rejointe par le plus de `(joueurs + corpos)` domine le MDC pour ce tour, et est libre d'appliquer sa ligne politique détaillée plus bas.

> En cas d'égalité, aucune coalition ne l'emporte.

### Contrats publics
De gros contrats d'entretien et de sécurité sont redistribués entre les corpos du MDC.

Effets :

* Les **corpos** appartenant à la coalition **Contrats publics** gagnent immédiatement **+1 actif** dans leur marché historique. 
* Les **corpos** appartenant à la coalition **Consolidation** subissent **-1 actif** dans leur marché historique, sans pouvoir descendre en dessous de 0.

### Opérations Clandestines
De nouvelles lois sont votées, renforçant les contrôles militaires au détriment de certaines zones.

Effets :

* Au prochain tour, les **joueurs** appartenant à la coalition **Opérations Clandestines** gagnent **+20%** sur chacune de leurs runs. Ce bonus peut permettre de dépasser les 100%, améliorant la vitesse de la run.
* Au prochain tour, les **joueurs** appartenant à la coalition **Contrats publics** subissent un malus de **-20%**.

### Consolidation
Des opérations de presse et des réunions avec les citoyens permettent à certaines personnes de se faire connaître et apprécier du grand public.

Effets : 

* Les **joueurs** appartenant à la coalition **Consolidation** gagnent **+3PV** pour la fin de partie.
* Les **joueurs** appartenant à la coalition **Opérations Clandestines** subissent un malus de **-3PV** pour la fin de partie.

Autrement dit, de grosses possibilités de coopération pour d'énormes opportunités de backstab.

    Jack Finn a 3 parts dans Horizon, ce qui est davantage que n'importe quel autre joueur. Lorsqu'au tour 4 il choisit de rejoindre la coalition Consolidation, la corpo l'appuie dans cette coalition pour le tour.
    Shiro Kuboka étant le seul a avoir investi dans les corpos Renraku et Sony, elles le suivent lorsqu'il opte pour la coalition Contrats Publics.
    Si aucun autre joueur n'intervient dans le MDC ce tour, la coalition Contrats Publics a une valeur de 3 (1 joueur + 2 corpos), ce qui l'emporte sur la coalition Contrats Publics (1 joueur + 1 corpo = 2).
    Les Contrats Publics votés au MDC rapportent 1 actif dans leurs marchés historiques à Renraku et Sony. Horizon, en opposition, est malmenée et perd 1 actif dans son marché historique.

## Classement initial
Au début du jeu, les corpos reçoivent respectivement 13, 12, 11, 11, 10, 10, 9, 9, 8 et 7 actifs, dans l'ordre décroissant du classement. Le classement initial est laissé au hasard à deux exceptions près :

* Ares fait partie des 3 premières corpos.
* Spinrad et Prometheus ne peuvent pas recevoir un rang supérieur à 5 (soit un maximum de 10 actifs).
