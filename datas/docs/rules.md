title: Comment jouer ?

Vous incarnez un cadre corporatiste décidé à se tailler un empire dans une des places financières les plus concurrentielles du 6<sup>ème</sup> monde : l'île de Manhattan.

[TOC]

## Concepts de base
Les **corporations, ou "corpos"**, sont au coeur du jeu. De gigantesques multinationales qui ont supplanté le pouvoir des nations et fait main basse sur l'économie planétaire. Elles sont innombrables, mais le Corporate Game ne tient compte que des dix plus grosses s'étant implantées à Manhattan.

La taille de ces dix corpos est représentée par leur nombre d'**actifs**, qui évoluera en fonction des actions des joueurs et des caprices de la bourse. Plus une corpo possède d'actifs, plus elle engrange de bénéfices.

Au début de la partie, les actifs des 10 corpos sont tirés au hasard (entre 7 et 12). ([cf. Classement initial](rules.md#classement-initial))

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

Si une corporation a plus d'actifs que toutes les autres sur un marché, elle **domine** ce marché et gagne un actif. Attention cependant, cet actif est perdu dès la fin du tour où la corporation cesse de dominer le marché. En cas d'égalité, aucune corpo ne domine.

Les joueurs commencent la partie avec 1 point d'**Influence corporatiste**, ou **"IC"**. Cette caractéristique représente l'étendue de leur pouvoir et de leurs réseaux dans l'île de Manhattan et sert de limite à certaines de leurs actions. Elle pourra être augmentée en cours de partie.

Pour leur permettre de démarrer, chaque joueur reçoit au début du jeu 2 millions de **nuyens (ny)**, la monnaie globale du 6<sup>ème</sup> Monde.

La partie se joue en 7 **tours**, chaque tour correspondant à un trimestre. À la fin du jeu, chaque joueur compte ses **points de victoire**, et celui qui en possède le plus est déclaré vainqueur. ([cf. Fin du jeu](endgame.md))

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
* Une corpo au hasard perd 1 actif sur son marché historique sans pouvoir descendre en dessous de 0.

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

À la fin de la partie, si un joueur n'a pas de nationalité corpo, il perd 6 points de victoire.

Si la corpo dont le joueur est citoyen Crashe, il en perd la citoyenneté et pourra s'il le souhaite en réclamer une nouvelle au tour suivant. Il subit normalement le malus de points de victoire.

## Runs
Les requins corpos ont tendance à ne pas jouer selon les règles. Pour manipuler le marché et gagner un avantage sur la concurrence, ils n'hésitent pas à engager des agents indépendants, appelés shadowrunners, pour effectuer toutes sortes d'opérations clandestines, ou shadowruns. **Runs**, pour les intimes.

### Les runs classiques
#### Datasteal

Le commanditaire choisit **un marché**, une **corpo cible** et une **corpo bénéficiaire**. En cas de réussite, le marché de la corpo bénéficiaire gagne **+1 actif** grâce aux précieuses informations dérobées à la concurrence. 

* Vous pouvez lancer cette run uniquement si la corporation bénéficiaire et la corporation cible partagent le même marché.
* Vous ne pouvez pas lancer cette run si la corpo bénéficiaire possède plus d'actifs dans le marché que la corpo cible

#### Sabotage

Le commanditaire choisit **un marché** d'une **corpo cible**, et tente de saboter une de ses opérations. En cas de réussite, le marché de la corpo cible subit **-2 actifs**.

#### Extraction

Le commanditaire choisit **un marché**, une **corpo cible** et une **corpo bénéficiaire**. En cas de réussite, un employé crucial est kidnappé des locaux de la corpo cible, qui subit **-1 actif** sur ce marché, et rejoint la corpo bénéficiaire, lui faisant gagner **+1 actif** sur ce marché.

* Vous pouvez lancer cette run uniquement si la corporation bénéficiaire et la corporation cible partagent le même marché.
* Vous ne pouvez pas lancer cette run si la corpo bénéficiaire possède plus d'actifs dans le marché que la corpo cible. 

### Coût d'une run

Chaque run coûte 350 000 ny et a 50% de chances de réussir. Le joueur **commanditaire** peut augmenter la **précision** (les chances de réussite de sa run) à raison de 50 000 ny par tranche de 10% supplémentaires.  

> Un joueur qui investit 450 000 ny dans une run de Sabotage aura donc 70% de chance de la voir réussir (`50% de base + 2 × 10%`)
Attention, on ne peut pas payer plus de 250 000 ny pour augmenter la précision de sa run (et donc dépasser les 100%).

Pour chaque point d'IC, un joueur peut réduire le coût de base d'une run à 50 000 ny (au lieu de 350 000 ny). Il paye normalement les bonus de précision apportés à sa run.

### Les runs spéciales
#### Protection

Les corporations n'apprécient pas particulièrement d'être la cible de runs, et investissent des sommes colossales dans leur sécurité. 
Vous pouvez lancer une run de protection sur un marché d'une corporation pour réduire la précision maximale des runs qui le cible. Son coût de base est de 350 000 ny comme les autres run. La précision maximum des runs attaquantes sur ce marché baisse en fonction du coût payé :

| Coût amélioration de la protection   | 350k¥ | 400k¥ | 450k¥ | 500k¥ |
|--------------------------------------|-------|-------|-------|-------|
| Valeur maximale des runs attaquantes |  80%  |  70%  |  60%  |  50%  |

> Vous pouvez utiliser la réduction du prix de base de la run à 50 000 ny avec l'IC comme pour les autres runs. Si vous avez 1 d'IC, vous pouvez avoir la réduction sur un sabotage, un datasteal, une extraction ou une protection. Vous n'aurez pas deux réductions.

#### Information

Le commanditaire choisit des **joueurs cible** et des **corpos cible**

Vous recevrez un message contenant toutes les actions faites par les joueurs cibles ce tour-ci ainsi que leurs  **Secrets** ([cf. Secrets](start.md#secrets)).
Vous recevez un détail de toutes les actions réussies et échouées sur les corpo cible.

Cette run d'Information a un coût particulier :
* 150 000 ny par joueur selectionné
* 50 000 ny par joueur selectionné

### Résolution

Le pourcentage de chances maximum qu'une run peut atteindre est de 90%. Ce chiffre peut être baissé par les runs de Protection.

> Une run d'Extraction qui a 100% de chances de réussite sera donc maxée à 90%.

Les runs sont résolues par % de réussite décroissants. Une seule run de chaque type peut être réussie par cible et par marché.

> Une run qui a 70% de chances de réussir passera toujours avant une run qui a 60% de chances de réussir. Si la première run passe, la seconde échoue automatiquement.

    Jules, Matthieu et Bom cherchent à lancer une extraction qui a pour cible le marché Militaire de Renraku.
    Yoann, qui a des parts dans cette corpo, les a vu venir et lance une run de Protection sur ce marché.
    Matthieu lance une run en mettant Horizon comme bénéficiaire à 60% de chances de réussite sans son bonus d'IC qu'il a utilisé pour une autre run (350 000 ny de base + 50 000 ny d'amélioration)
    Jules lance une run avec Ares en bénéficiaire avec 70% de chance de réussite avec son bonus d'IC (50 000 ny de coût de base + 100 000 ny d'améliorations)
    Bom lance une run avec Ares en bénéficiaire avec 50% de chances de réussite avec son bonus d'IC (50 000 ny de coût de base)
    Yoann lance une run de protection à 50% de chances de réussite maximum sur le marché Militaire de Renraku sans son bonus d'IC. (350 000 ny de base + 150 000 ny d'améliorations)

    La run de Jules s'éxecute en premier puisqu'elle a plus de précision. La run de protection de Yoann s'applique, la run de Jules a donc 50% de chances de réussite. La chance n'est pas avec lui et la run échoue. La run de Matthieu s'exécute alors (avec 50% de chances puis la run de protection est active tout le tour) et la run est un succès. La branche Militaire de Renraku perd un actif et la branche Militaire de Horizon gagne un actif. Bom arrive en dernier. Une run d'extraction a déjà eu lieu sur cette cible, sa run échoue automatiquement.

## Spéculation
Les investissements à long termes sont cruciaux pour bâtir un empire corporatiste, mais les cadres endurcis savent qu'il y a beaucoup d'argent à faire en spéculant à court terme sur les remous du marché. 

Les joueurs qui veulent miser dans le grand casino de l'East Coast Stock Exchange peuvent effectuer autant de **spéculation** qu'ils veulent. Le montant de ces spéculation ne peut dépasser `200 000 ny × (IC du spéculateur)`.

Dans chaque spéculation, le joueur choisit une corporation et mise sur son classement en fin de tour.

Si le spéculateur se trompe, il perd la somme misée.

Si sa spéculation est juste, il fait un bénéfice d'une côte de :

* **1 pour 3** s'il a spéculé qu’une corpo finirait le tour **première ou dernière**. (S’il a placé 100 000 ny, il les conserve et gagne 150 000 ny suplémentaires)
* **1 pour 5** s’il a spéculé qu’une corpo finirait le tour à un autre rang (**de seconde à avant-dernière**) .

> Si deux corpos ont des actifs négatifs (et crasheront donc en fin de tour), la corpo étant le plus loin dans le négatif est considéré dernière.


    Jack Finn a la ferme intention de faire travailler son argent. Ayant une IC de 2, il peut miser jusqu'à 400 000 :
    
    * il mise 100 000 ny sur la position d'Horizon, dont il pense qu'elle sera 2ème à la fin du trimestre.

    Horizon, malgré une Extraction vicieuse, finit en seconde position. Il garde ses 100 000 ny et en touche 400 000 de plus qui le font largement rentrer dans ses frais. Si Horizon avait finit 3eme, il aurait perdu ses 100 000ny.


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
Au début du jeu, les corpos reçoivent respectivement 12, 11, 11, 10, 10, 9, 9, 8, 8 et 7 actifs, dans l'ordre décroissant du classement. Le classement initial est laissé au hasard à deux exceptions près :

* Ares fait partie des 3 premières corpos.
* Spinrad et Prometheus ne peuvent pas recevoir un rang supérieur à 5 (soit un maximum de 10 actifs).
