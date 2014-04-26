Avec Mich et Jules, on a tiré les conclusions suivantes du jeu :

* **Trop d'inflation**. Les corpos prennent trop de valeur trop rapidement, ce n'est pas normal. Cette inflation donne beaucoup trop d'argent aux joueurs, au point que des décisions qui devraient être complexes et demander un choix (je prends A ou B ?) ne se font plus, et que l'on est simplement bloqué par notre IC.
* **Les runs de Protection sont beaucoup trop fortes**. Elles bloquent tout le jeu : il suffit de voir ce qu'il s'est passé le dernier tour ! (réponse : rien)
Les lignes du MDC pour les spéculations n'ont aucun intérêt par rapport aux 4 autres
* Il y a quelques fails dans le comptage des PV en fin de partie
* Les BG sont déséquilibrés
* Les 4 premiers tours étaient intéressants et demandaient des prises de décisions complexes, ça s'est ensuite perdu et c'est devenu très mécanique, ce qui est dommage.

La question : *comment garder l'intérêt des 4 premiers tours sans ruiner la suite* ?

On a commencé à y réfléchir, voici des pistes potentielles pour une hypothétique prochaine partie plus équilibrée. C'est juste des idées, ça demande une discussion plus approfondie.

## Runs

Les runs doivent être totalement revues. Les Datasteals sont bien trop déséquilibrés par rapport au reste, et la protection trop puissante.

On envisageait donc de réintroduire de façon détournée la notion de fixer. Globalement, chaque type de run a un pool de runners attitrés : par exemple, pour le Sabotage, des runners à 90%, 80%, 70%, 60%.

Plutôt que de payer 50k / 10%, on doit plutôt miser ; par exemple "je mise 700k¥ pour que les runners à 90% fassent ma run". Celui qui a l'enchère la plus élevée sur ces runners remporte la run pour le tour. On peut miser autant de fois que l'on a d'IC par type de run (donc au début une mise sabotage, une mise datasteal, une mise information, une extraction et une protection). Évidemment, les runners à 90% sont les plus intéressants, mais la question devient : quelqu'un d'autre va-t-il miser là dessus ? Et si oui, quelle valeur ?

De plus, le prix est dynamique et s'ajuste avec le budget. En début de partie, pas cher, ensuite quand tout le monde est riche, au lieu de se battre contre un système fixe à 50k¥ / 10%, on se bat contre les autres joueurs et leur argent. Une même mise cumulée remporte l'enchère (par exemple, le joueur A paie 500k¥ pour saboter Horizon. B paie 400k¥ pour saboter Ares, C paie 300k¥ pour saboter Ares : A perd l'enchère, et les runners récupèrent l'argent de B et C pour aller contre Ares).

* La mise minimum est de 50k¥.
* Si notre enchère échoue, on perd quand même 10% de la mise (frais de dossier).
* Si la run échoue, comme avant, on est remboursé à 50%.
* Le malus de timing reste présent.
* Le système est le même pour les runs de protection, qui passent par enchère. * La valeur de protection viendrait s'additionner avec la valeur de base des corpos (plutôt qu'en complément). Dans tous les cas, ça ne peut pas dépasser 60% de protection.

Ça permet d'éviter les blocages complets que l'on a pu voir, et de redonner de l'intérêt aux Sabotages.

## MDC

Le calcul des voix n'inclut que les parts actuelles, pas les changements de majorité potentiels pendant le tour.

On hésite pour les lignes 5 et 6 du MDC :

* Soit augmenter les mises (genre +20% sur toutes tes mises pour les runners)
* Soit rajouter une section de méta-jeu : "Gagner 3PV / enlever 3PV à la coalition opposée"

## Points de Victoire

* Les spéculations ne sont considérées comme réussies que si pleines.  (Investissement max par rapport à l'IC, pour éviter certains bugs exploits. Si on investit une spéculation à fond et une à moitié, on ne compte donc qu'une spéculation réussie)
* 7 tours de jeu uniquement, au lieu de 8.
* Les runs d'Informations ne comptent que sur joueur distincts. Idem, évite les bugs exploits.
* Le titre Opportuniste disparaît (ou est réduit à 5 points)

## UI

Du travail :

* reprendre le graphisme
* Afficher les dividendes des joueurs
* Faire un tableau global
* etc

(en cours de discussion)
