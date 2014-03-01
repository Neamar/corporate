# Corporate Game Manhattan

## Tasks orders
* [0] **BuyShareTask** : Buy all shares for all players
* [100] **VoteTask** : Resolve player's corporation votes
* [100] **MDCVoteTask** : Choose the MDC party line, and save it in an MDCVoteSession
* [300] **MDCLineCPUBTask** : Enforce the effects of the MDC CPUB party line
* [300] **MDCLineDEVETask** : Enforce the effects of the MDC DEVE party line
* [349] **ProtectionRunTask** : Debit Protection runs from players
* [350] **OffensiveRunTask** : Resolve Offensive corporations runs (DataSteal, Sabotage, Extraction)
* [350] **InformationRunTask** : Resolve Information runs
* [400] **InvisibleHandTask** : Give +1 and -1 asset for two random corporations
* [600] **FirstLastEffectsTask** : Apply first and last corporations effects
* [650] **SaveCorporationAssetTask** : Save the assets of all corporations after the turn resolution
* [800] **DividendTask** : It's time to get money!
* [900] **CitizenshipTask** : Update players citizenships
* [900] **CorporationSpeculationTask** : Resolve corporations speculations
* [900] **DerivativeSpeculationTask** : Resolve derivatives speculations
* [1000] **BuyInfluenceTask** : Buy new Influence level
* [1000] **CrashCorporationTask** : Let's crash corporations that didn't made it through the turn


## Frontend
### Docs
Documentation

### Newsfeeds
* Bulletin du MDC
    * ligne politique votée (rédigé)
    * coalitions (rédigé)
* People
    * influence
    * changement nat. corpo
* Économique
    - achat de part
    - effets premiers derniers
* Matrix buzz
    * runs (rédigé)

### Wall Street
Tableau des corpos :
(nom, actifs, anciens actifs, changements inconnus, premier, dernier, sabotage, mdc, ds, s, e)

| Nom     | Ac | Old|  ? | P  |  D | Sab| MDC| DS | S | E
|---------|----|----|----|----|----|----|----|----|---|--:|
| Renraku | 15 | 12 | +2 | +1 | -1 | +5 | -2 | 2  | 0 | 2 |

(Le 15 est en gras rouge ou vert selon le delta)

Graphique de la bourse

Tableau des produits dérivés :

| Nom  | Ac | Old| Delta |
|------|----|----|------:|
| Nikkei | 45 | 38 | +7  |

Graphique des produits dérivés

foreach corpo:

* Lien vers la corpo
* graphique de la corpo

### Corporations
Tableau des corpos:

* Nom de la corpo
* Actifs
* Défense Datasteal,
* Défense Sabotage
* Défense Extraction
* Détection

| Nom   | Actif  | DS | S  | E  | D  |
|-------|--------|----|----|----|---:|
|Renraku| **15** | 20 | 10 | 20 | 30 |

#### Corporation
Nom
Logo

Actifs actuels
Ligne votée
Défenses

| Nom   | Actif  | DS | S  | E  | D  |
|-------|--------|----|----|----|---:|
|Renraku| **15** | 20 | 10 | 20 | 30 |

Graphique de la corpo
Description
Parts possédées
Citoyens corpos

|Renraku    | Parts   | Citoyen  |
|-----------|---------|---------:|
Tiroshi     | 18      | KING     |
Remi        | 12      | Oui      |
Jules       | 12      |          |

(tableau trié par parts possédées)

Effet premier dernier

### Parts
Tableau croisé :

* Nom du joueur
* Corporation
* en gras cellule citoyenneté corpo

|         |   Renraku |    MCT |    Ares |
|---------|-----------|--------|--------:|
| Tiroshi | 0         | 0      | 0       |
| Remi    | 0         | 0      | 0       |


### Joueurs
Nom du joueur
IC
Vote de ligne
Citoyenneté

| Nom    |  IC   | Ligne        | Citoyen |
|--------|-------|--------------|--------:|
|Tiroshi | **2** | Transparence | Renraku |

#### Joueur
* Nom
* avatar
* ic
* vote

| Nom    |  IC   | Ligne        | Citoyen |
|--------|-------|--------------|--------:|
|Tiroshi | **2** | Transparence | Renraku |

* description
* citoyenneté
* parts


### Commlink
Messages privés entre PJ et de fin de tour, résultat runs d'informations et message de résolution

#### Messages
* Argent restant
* Achat de part
* Changement de nationalité corporatiste
* Augmentation d'influence corporatiste
* Runs
    * Runs défensives
    * Runs offensives
* Détections
    * Toutes les runs détectées
* Spéculations
    * Spéculations
* Votes
    * Vote
    * Vote de coalition
