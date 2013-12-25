Corporate Game Manhattan.

## Étude de cas.
Réduire les concepts au maximum...

### Ordres disponibles
* Acheter un point d'influence corpo
* Acheter une part
    - Paramètre :
        + Corpo
* Voter
    - Paramètre :
        + Corpo+
        + Corpo-
        + Rang Corpo+
        + Rang Corpo-
* Run de Protection
    - Paramètre :
        + Corpo bénéficiaire
        + Pourcentage
        + Bonus de 30%
* Run de Sabotage
    - Paramètre :
        + Corpo victime
        + Pourcentage
        + Bonus de 30%
* Run de Datasteal
    - Paramètre :
        + Corpo victime
        + Corpo bénéficiaire
        + Pourcentage
        + Bonus de 30%
* Changer de nationalité corpo
    - Paramètre :
        + Corpo hôte

## Phase de résolution
1. Achat de parts
2. Votes : + 1 / -1 par vote 
3. Runs
    - Runs de protection : par corpo, triées par %
    - Autres runs, triées par % :
        + Tester réussite, tester protection
            * R0P0 : échec
            * R0P∅ : échec
            * R0P1 : capture
            * R1P0 : succès
            * R1P∅ : succès
            * R1P1 : interception
        + En cas de...
            * Succès : appliquer les effets (datasteal +1 bénéficiaire, sabotage -2 victime). Le datasteal ne s'applique qu'une fois par corpo
            * Échec : ∅
            * Interception : ∅ [feedback]
            * Capture : ∅ [feedback++]
5. La main du marché (+1|-1 * 2)
5. Calcul des nouveaux actifs
5. Effets premiers / derniers
5. Gain spéculation : 100k * spéculation réussie
5. Distribution des dividendes
    - Les parts achetées ce tour-ci ne comptent pas, sauf pour les tours 1 et 2
    - 50 * actifs * nbparts * (1.25 si corpo première) * (0.75 si corpo dernière) * (1.1 si citoyenneté corpo)
5. Achat d'influence corporatiste

### Feedbacks
* Global
    - Classement final des corpos, avec Δ
    - Sabotages
    - Citoyenneté corpo
    - Effets 1er / derniers
    - Achat de parts
* Privé
    - Feedback pour chaque run : échec, réussite, interceptino, capture, datasteal déjà fait
    - Feedback des runs sur la corpo dont on est citoyen : interception, capture
    - Feedback des runs de protection : interception, capture
    - Datasteal sur la corpo dont on est citoyen

## Architecture
### Website
Holds global datas

* User
    - mail
    - phone
    - image

### Engine
Holds datas for a game

* Game
    - current_turn
    - total_turn
* Player
    - -> User
    - -> Game
    - Name
* Message
    - title
    - content
    - author
    - public?
* MessageRecipient
    - ->Player
* Order
    - -> Player
    - -> Game
    - turn
    - canBeCreated():bool
    - getForm():Form

#### Module architecture
Engine modules can be standard Django apps, with models and views. To use as a module, call `engine.registerModule(taskBuilder, orders, views)`, where:

* `taskBuilder` is a function which will be called with the current game, and must returns a list of ResolveTasks to handle resolution
* `orders` is a list of Orders to register
* `views` is a dict whose keys are regexp and values associated functions. If a conflict occurs between multiple apps, the last entry prevails.

### Engine modules
#### engine.corporations
Base models for everything corporation related.

Depends on: []

Models:
* CorporationDefinition
    - name
    - description
* Corporation
    - -> CorporationDefinition
    - assets

Views:
* /corporations/corporation/:id : corporation details

#### engine.corporations.orders
Basic Orders issued around corporations : buy share, vote, speculate

Depends on: ['corporations']

Models:
* BuyShareOrder
    - -> corporation
* VoteOrder
    - -> corporation+
    - -> corporation-
* SpeculationOrder
    - -> VoteOrder
    - Rank+
    - Rank-

#### engine.corporations.assets_history
Store the corporation assets turn by turn, to display stocks graphs.

Depends on: ['corporations']

Models:
* CorporationAsset
    - ->corporation
    - assets
    - turn

Views :
* /corporations/market

#### engine.corporations.invisible_hand
Invisible market hand.

Depends on: ['corporations']


#### engine.runs
