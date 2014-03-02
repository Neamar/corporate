title: Comment jouer?

Vous incarnez un cadre corporatiste décidé à se tailler un empire dans une des places financières les plus concurrentielles du 6<sup>ème</sup> monde : l’île de Manhattan.

[TOC]

## Concepts de base
Les **corporations, ou "corpos"**, sont au coeur du jeu. De gigantesques multinationales qui ont supplanté le pouvoir des nations et fait main basse sur l'économie planétaire. Elles sont innombrables, mais le Corporate Game ne tient compte que des dix plus grosses s’étant implantées à Manhattan.

La taille de ces dix corpos est représentée par leur nombre d'**actifs**, qui évoluera en fonction des actions des joueurs et des caprices du marché. Plus une corpo possède d'actifs, plus elle engrange de bénéfices. Au début de la partie, les actifs des 10 corpos sont tirés au hasard. [(cf. Classement initial)](rules.md#classement-initial)

Le **classement** trie les corpos par nombre d'actifs et leur attribue un rang de 1 à 10, 1 correspondant à la corpo possédant le plus d'actifs, celle qui domine le marché.

Les joueurs commencent la partie avec 1 point d'**Influence corporatiste, ou "IC"**. Cette caractéristique représente l'étendue de leur pouvoir et de leurs réseaux dans l'île de Manhattan et sert de limite à certaines de leurs actions. Elle pourra être augmentée en cours de partie.

Pour leur permettre de démarrer, chaque joueur reçoit au début du jeu 2 millions de **nuyens (ny)**, la monnaie globale du 6<sup>ème</sup> Monde.

La partie se joue en 8 **tours**, chaque tour correspondant à un trimestre. À la fin du jeu, chaque joueur compte ses **points de victoire**, et celui qui en possède le plus est déclaré vainqueur. [(cf. Fin du jeu)](endgame.md)

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

> Une part dans la corpo en tête du classement (rang 1) coûte `125 000 ny × actifs` pour joueurs qui n’en ont pas la "nationalité" [(cf. Citoyenneté corpo)](rules.md#citoyenneté-corpo).

À la fin de chaque tour, les joueurs touchent les **dividendes** de leurs parts. Chaque part rapporte à son propriétaire `50 000 ny ny × (actifs de la corpo)`. Un joueur possédant 2 parts dans une corpo de 5 actifs et 1 part dans une corpo de 10 actifs touchera donc `2 × (50 000 × 5) + 1 × (50 000 × 10)`, soit 1 million de ny.

> Les parts de la corpo en tête du classement rapportent `75 000 ny × actifs`.
> Les parts de la dernière corpo rapportent `25 000 ny × actifs`.

## Évolution du marché
À chaque tour, les corpos vont gagner et perdre des actifs. Ce n'est qu'après toutes les modifications effectuées que sont calculés les dividendes.

### Les Votes
En tant qu'acteur majeur du marché, chaque joueur a droit à un **Vote** par tour. Il choisit :

* Une corpo qui gagne 1 actif.
* Une corpo qui perd 1 actif.

### La main invisible du marché
Le reste des aléas de la bourse de Manhattan est laissé à la chance. À chaque tour :

* Une corpo au hasard gagne 1 actif.
* Une corpo au hasard perd 1 actif.

### Effet premier / effet dernier
Les effets premier et dernier des corpos en tête et en fin de classement s'appliquent chaque tour, après tous les autres modificateurs, et peuvent chambouler les actifs des corpos. Voir la page des corporations pour une description individuelle de chaque corpo et [le recap](recap.md) pour une liste de leurs effets premiers / derniers.

### Crash
Au cours de la résolution du tour, une corpo peut descendre à 0 actifs ou moins. Son effet dernier peut tout de même s'appliquer, mais si elle n'est pas remontée à au moins 1 actif à la fin de la résolution, elle **Crashe** et est définitivement retirée du classement. Pas de remboursement pour les parts investies.

## Achat d'Influence
Un fois par tour, les joueurs peuvent payer pour augmenter leur Influence corporatiste d'un point. Le coût est de `400 000 ny × nouvel indice`, soit 1 200 000 ny pour passer de 2 à 3. 

La nouvelle valeur d’IC ne prendra effet qu’au tour suivant.

## Citoyenneté corpo
Dans le sixième monde, les corporations ont tellement de pouvoir qu'elles sont de véritables états, avec leurs propres lois et leur propres citoyens. À chaque tour, un joueur peut réclamer la citoyenneté d'une corpo dans laquelle il possède au moins une part.

Un **citoyen corpo** :

* Gagne davantage de points de victoire si sa corpo est bien placée dans le classement à la fin de la partie [(cf. Fin du jeu)](endgame.md#points-de-citoyen).
* Paie les parts de sa corpo au prix usuel de `100 000 ny × actifs` même si elle est en tête du classement (au lieu de `125 000 ny × actifs`).
* Bénéficie de la protection de sa corpo contre ceux qui voudraient en apprendre plus sur ses actions [(cf. Information)](rules.md#information).
* Reçoit les informations détectées par sa corpo dans son message de résolution.

Changer de nationalité corpo coûte au joueur un nombre de points de victoire égal au tour en cours, soit -6 s'il change de nationalité au tour 6. Il est possible de commencer la partie avec une nationalité corporatiste [(cf. Mise en place)](start.md#citoyenneté-corpo).

Si la corpo dont le joueur est citoyen Crashe, il en perd la citoyenneté et pourra s'il le souhaite en réclamer une nouvelle au tour suivant. Il subit normalement le malus de points de victoire.

## Runs
Les requins corpos ont tendance à ne pas jouer selon les règles. Pour manipuler le marché et gagner un avantage sur la concurrence, ils n'hésitent pas à engager des agents indépendants, appelés shadowrunners, pour effectuer toutes sortes d'opérations clandestines, ou shadowruns. **Runs**, pour les intimes.

Il existe 5 type de runs : **Datasteal**, **Sabotage**, **Extraction**, **Information** et **Protection**. Elles ont chacune des résultats spécifiques et une chance de réussite de base en pourcentage (%): par exemple, 30% pour les runs de Sabotage. Le joueur **commanditaire** peut augmenter les chances de réussite de sa run à raison de 50 000 ny pour 10% supplémentaires. Un joueur qui investit 150 000 ny dans une run de Sabotage aura donc 60% de chance de la voir réussir (`30% de base + 3 × 10%``).

Pour lancer une run, un joueur doit investir un minimum de 50 000 ny, soit +10%.

Pour chaque point d'IC qu'il possède, un joueur peut gratuitement ajouter +30% à une run par tour. Un joueur possédant une IC de 3 pourra donc ajouter +30% à 3 runs par tour. Ces bonus ne peuvent pas être cumulés sur une même run.

Une run a un maximum de 90% de chances de réussir, mais il est possible de payer un pourcentage supérieur pour contrebalancer des malus. [(cf. Malus de timing)](rules.md#malus-de-timing) et [(cf. Contrôles ciblés)](rules.md#contrôles-ciblés).

Si une run autre que Protection échoue ou est contrée (voir ci-dessous), son commanditaire récupère la moitié des nuyens investis.

### Défense
Les corporations n'apprécient pas particulièrement d'être la cible de runs, et investissent des sommes colossales dans leur sécurité. Chaque corpo possède un indice de **Défense** qui lui est propre en Datasteal, Sabotage et Extraction. La Défense en Datasteal est également utilisée pour contrer les runs d'Information (voir plus bas).

> Par exemple, la corpo Renraku a une Défense de 20 en Datasteal, de 10 en Sabotage et de 20 en Extraction.

L'indice de Défense représente le pourcentage de chances qu'une run du même nom soit contrée par la sécurité de la corpo.

> Renraku a donc 20% de chance de contrer toute run d'Extraction qui la cible.

### Détection
En plus de leurs indices de Défense, les corpos possèdent un indice de **Détection** (30 pour Renraku). Ce nombre correspond au pourcentage de chances que la corpo détecte les runs qui la ciblent. Une run détectée est déclarée dans le message de résolution de tous les citoyens de la corpo ciblée avec tous les détails, commanditaire et chances de réussite inclus.

Une run détectée sera également mentionnée dans les Newsfeeds de fin de tour, mais sans davantage d’information que la corpo ciblée.

> Les runs de Protection ne sont jamais détectées.
> Les runs de Sabotage réussies sont particulièrement voyantes, et apparaissent dans les Newsfeeds même si elles n’ont pas été détectées.
> Même détectées, les runs d’Information ne font pas de vagues et ne sont pas révélées dans les Newsfeeds.

### Malus de timing
Lorsque plusieurs équipes de shadowrunners sont engagées pour des runs similaires, elles risquent d’entrer en concurrence et de se marcher sur les pieds.

Une run subit un malus de **-10%** pour chaque autre run qui **correspond aux 3 critères** suivants :
* Est du **même type** (Datasteal, Sabotage, Extraction ou Information).
* A la **même cible**, joueur ou corpo.
* A un **pourcentage de réussite supérieur ou égal** au sien (avant que les malus de timing ne soient appliqués).

    2 runs de Sabotage (même type) sont lancées contre Renraku (même cible) le même tour :
    * Si elles ont toutes les deux 70% de chance de réussite, chacune fait subir à l’autre un malus de timing de -10%.
    * En revanche, si la première a 80% de chance de réussite et la seconde 70%, seule la seconde subit un malus.

> Les runs de Protection n'entrent pas en concurrence.

## Les types de runs
### Datasteal
* Base : 30 %

Le commanditaire choisit une **corpo cible** et une **corpo bénéficiaire**. En cas de réussite, la corpo bénéficiaire gagne **+1 actif** grâce aux précieuses informations dérobées à la concurrence.

### Sabotage
* Base : 30 %

Le commanditaire choisit une **corpo cible**, et tente de saboter une de ses opérations. En cas de réussite, la corpo subit **-2 actifs**.

> Qu'elles aient été détectées ou non, les runs de Sabotage réussies sont révélées dans les Newsfeeds.

### Extraction
* Base : 10 %

Le commanditaire choisit une **corpo cible** et une **corpo bénéficiaire**. En cas de réussite, un employé crucial est kidnappé des locaux de la corpo cible, qui subit **-1 actif**, et rejoint la corpo bénéficiaire, lui faisant gagner **+1 actif**.

### Information
* Base : 60 %

Le commanditaire choisit un **joueur cible**. En cas de réussite, une enquête approfondie lui fournit tous les **messages de résolution** du joueur ciblé depuis le début de la partie (à l'exception des éventuels résultats de runs d'Information), ainsi que ses **Secrets** [(cf. Secrets)](start.md#secrets).

> La Défense de Datasteal de la corpo dont la cible est citoyen est utilisée pour contrer les runs d'Information.
> Même détectées, les runs d’Information n’apparaissent pas dans les Newsfeeds.

### Protection
* Base Datasteal : 40 %
* Base Sabotage : 0 %
* Base Extraction : 10 %

Le commanditaire choisit une **corpo bénéficiaire**, et lui attribue une Défense supplémentaire en Datasteal, Sabotage ou Extraction. Cette seconde Défense s'applique en complément de celle de la corpo (elles ne s'additionnent pas, elles s'enchaînent), et ne peut pas dépasser 50%. Il est possible de lancer plusieurs Protections similaires sur une même corpo.

    Jack Finn, un requin sans scrupule, désire effectuer une Extraction contre Renraku, la corpo de son rival Shiro Kuboka, afin de booster les actifs d'Horizon dans laquelle il a largement investi.

    Il paye 250 000 ny pour ajouter 50% de chance de réussite à sa run, et utilise un de ses bonus d'IC pour 30% supplémentaire. Sa run a donc 90% de chance de réussite (10% de base + 50% de ny + 30% de bonus d'IC).

    Shiro Kuboka, devinant la manoeuvre, paye 50 000 ny pour organiser une Protection en Extraction en faveur de Renraku. Il ajoute un de ses propres bonus d'IC pour atteindre 50%, (10% de base + 10% de ny + 30% d’IC ; 50 % étant le maximum pour une Protection).

    Test de réussite de l'Extraction, 90% : réussite
    Test de Défense de Renraku contre les Extractions, 20% : échec
    Test de la Protection de Shiro Kuboka, 50% : échec
    Test de Détection, 30% : réussite

    Un scientifique de renom est arraché à son laboratoire. Renraku perd 1 actif, Horizon en gagne 1. La run a cependant été détectée, et tout Manhattan est au courant qu'elle a eu lieu, sans savoir que Jack Finn est son commanditaire ou qu’Horizon en a bénéficié. Shiro Kuboka, en revanche, est citoyen de Renraku, et apprend donc l'ensemble de la vérité. Maudissant l'incompétence de ses employés, il rassemble ses fonds pour un Sabotage bien senti contre Horizon...

## Spéculation &ndash; Le miracle de Wall Street
Les investissements à long termes sont cruciaux pour bâtir un empire corporatiste, mais les cadres endurcis savent qu'il y a beaucoup d'argent à faire en spéculant à court terme sur les remous du marché. 

Les joueurs qui veulent miser dans le grand casino de l’East Coast Stock Exchange peuvent effectuer un nombre de **spéculations** par tour égal à leur IC. Le nombre de spéculations qu’un joueur peut effectuer est limité par son IC, et le montant de chaque spéculation ne peut dépasser `100 000 ny × (IC du spéculateur)`. Il est possible d’effectuer la même spéculation plusieurs fois.

Chaque spéculation peut viser :

* La croissance ou la chute des actifs d'un **produit dérivé** (voir plus bas)
* La place d’une corpo dans le classement de fin de tour.

Si le spéculateur se trompe, il perd la somme misée.

Si sa spéculation est juste, il fait un bénéfice de :

* 1 fois la somme misée s'il a spéculé sur la **fluctuation d'un produit dérivé** -- soit une cote de **1 pour 2**. (S’il a placé 100 000 ny, il en récupère 200 000)
* 2 fois la somme misée s'il a spéculé qu’une corpo finirait le tour **première ou dernière** -- soit une cote de **1 pour 3**.
* 4 fois la somme misée s’il a spéculé qu’une corpo finirait le tour à un autre rang (**de deuxième à avant-dernière**) -- soit une cote de **1 pour 5**.

Le MDC peut modifier ces côtes, voir plus bas.

> Si deux corpos ont des actifs négatifs (et crasheront donc en fin de tour), la corpo étant le plus loin dans le négatif est considéré dernière.

### Produits dérivés
Un produit dérivé est la somme des actifs d'un ensemble de corpos. 

* Le **Nikkei** (indice de Bourse de Neo Tokyo) est la somme des actifs des corpos Sony, Shiawase et Renraku
*  Le **Dow Jones** est la somme des actifs d’Ares, Neonet, Spinrad et Prometheus.

    Jack Finn a la ferme intention de faire travailler son argent. Ayant une IC de 2, il effectue deux spéculations :
    * 200 000 ny sur une chute du Nikkei. Après tout, il a un sabotage prévu sur Renraku...
    * 100 000 ny sur la position d'Horizon, dont il pense qu'elle sera 2ème à la fin du trimestre.

    Son sabotage échoue, et la Bourse de Néo Tokyo croît de 2 actifs ce trimestre. Il ne reverra pas ses 200 000 ny.
    Horizon, malgré une Extraction vicieuse, finit en seconde position. Il garde ses 100 000 ny et en touche 400 000 de plus qui le font largement rentrer dans ses frais.


## Le Manhattan Development Consortium
Le MDC (ou Manhattan Inc.) n'est pas exactement une corporation, mais la structure à travers laquelle des corpos se sont alliées pour coordonner la reconstruction, assurer l'extraterritorialité de Manhattan et partager sa gouvernance entre ses membres. Cet équivalent corporatiste d'un conseil municipal tente de maintenir un contrôle absolu sur presque toutes les activités de Manhattan.

Les corpos membres ont changé plusieurs fois depuis la fin de la reconstruction. Aujourd'hui, elles sont dix, et ont chacune une voix lors des votes du consortium. Ces votes légifèrent sur tous les aspects de la vie et des affaires à Manhattan, des juteux contrats de la voirie, de la sécurité, du traitement des déchets ou du développement de la matrice aux lois de régulations des marchés qui ont le potentiel de bouleverser le cours des actions des corpos les plus stables. Les votes du MDC rythment la vie politique de Manhattan, et sont disputés par des coalitions fluctuantes qui ne reculent devant aucun coup bas pour rafler la mise.

Chaque tour, les joueurs peuvent participer au cirque du MDC en rejoignant une **coalition** défendant une cause particulière. Ces causes, détaillées plus bas, peuvent être une redistribution des  **Contrats publics**, un projet de **Développement urbain**, des **Contrôles ciblés**, de nouvelles lois de **Transparence**, de **Gardes fous bancaires** ou de **Dérégulation**.

Un joueur qui possède **le plus de parts** dans une corpo peut influencer ses décisions politiques : la corpo rejoint la même coalition que lui.

> Les parts achetées ce tour-ci sont prises en compte.
> En cas d'égalité sur le nombre de parts possédées, la corpo reste neutre. 

La coalition à laquelle le plus de (joueurs + corpos) appartiennent domine le MDC pour ce tour, et est libre d’appliquer sa ligne politique. Voir pus bas pour les effets spécifiques.

> En cas d'égalité, aucune coalition ne l'emporte.
> Les gains et pertes d’actifs prennent effet le tour même, avant les effets premier/dernier. Tous les autres effets sont appliqués le tour suivant.

### Contrats publics
De gros contrats d'entretien et de sécurité sont redistribués entre les corpos du MDC.

Effets :

* Les **corpos** appartenant à la coalition **Contrats publics** gagnent immédiatement **+1 actif**. 
* Les **corpos** appartenant à la coalition **Développement urbain** subissent **-1 actif**.

### Développement urbain
De grands travaux sont lancés par le MDC, redessinant la carte de Manhattan au profit de certaines corpos.

Effets :

* Les **corpos** appartenant à la coalition **Développement urbain** gagnent immédiatement **+1 actif**. 
* Les **corpos** appartenant à la coalition **Contrats publics** subissent **-1 actif**.

### Contrôles ciblés
De nouvelles lois sont votées, renforçant certains contrôles ciblés au détriment de certaines zones.

Effets : 

* Au prochain tour, les runs de **Datasteal**, **Sabotage** et **Extraction** ciblant les **corpos** appartenant à la coalition **Contrôles ciblés** subissent un malus de **-10%**.
* Les **joueurs** appartenant à la coalition **Transparence** ne pourront pas effectuer de runs de protection au prochain tour.

### Transparence
L'ouverture de bases de données privées offre de nouvelles possibilités de runs pour ceux qui y ont accès.

Effets : 

* Au prochain tour, les **joueurs** appartenant à la coalition **Transparence** gagnent un bonus de **+10%** sur toutes leurs runs de **Datasteal**, **Sabotage**, **Extraction**. 
* Les **joueurs** appartenant à la coalition **Contrôles ciblés** subissent **-10%** sur toutes leurs runs **Datasteal**, **Sabotage**, **Extraction** et **Information**.

### Garde-fous bancaires
Malgré les protestations de Wall Street, de nouvelles régulations pour l'ECSE entrent en action. Elles garantissent davantage de sécurité pour ceux en mesure d'en tirer profit, mais limitent les opérations de certains.

Effets :

* Au prochain tour, les **joueurs** appartenant à la coalition **Garde-fous bancaires** **gardent l'intégralité des mises** de leurs spéculations manquées.
* Les **joueurs** appartenant à la coalition **Dérégulation** ne pourront pas effectuer de **spéculations**.

### Dérégulation
De nouvelles barrières sautent, repoussant encore les limites de l'avidité boursière mais en laissant certains à la traîne.

Effets :

* Au prochain tour, les spéculations des **joueurs** appartenant à la coalition **Dérégulation** voient les **côtes augmentées de 1** (1 pour 2 devient 1 pour 3, 1 pour 5 devient 1 pour 6...)
* Les **joueurs** appartenant à la coalition **Garde-fous bancaires** ne pourront pas effectuer de **spéculations**.

Autrement dit, de grosses possibilités de coopération pour d'énormes opportunités de backstab.

## Classement initial
Au début du jeu, les corpos reçoivent respectivement 13, 12, 11, 11, 10, 10, 9, 9, 8 et 7 actifs, dans l'ordre décroissant du classement. Le classement initial est laissé au hasard à deux exceptions près : Spinrad et Prometheus ne peuvent pas recevoir un rang supérieur à 5, pour un maximum de 10 actifs.
