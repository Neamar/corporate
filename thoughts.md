# Corporate Game Manhattan.

## Concepts
### Ordres disponibles
* Acheter un point d'influence corpo
* Acheter une part
    - Paramètre :
        + Corpo
* Voter
    - Paramètre :
        + Corpo+
        + Corpo-
* Spéculation
    - Paramètre :
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
4. La main du marché (+1|-1 * 2)
5. Calcul des nouveaux actifs
6. Effets premiers / derniers
7. Gain spéculation : 100k * spéculation réussie
8. Distribution des dividendes
    - Les parts achetées ce tour-ci ne comptent pas, sauf pour les tours 1 et 2
    - 50 * actifs * nbparts * (1.25 si corpo première) * (0.75 si corpo dernière) * (1.1 si citoyenneté corpo)
9. Achat d'influence corporatiste

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

Models:
* User
    - mail
    - phone
    - image

Views:
* /login
* /
* /game/new

### Engine
Holds datas for a game

Models:
* Game
    - current_turn
    - total_turn
* Player
    - -> User
    - -> Game
    - Name
    - money
* Message
    - title
    - content
    - author
    - public?
    - M2M Player
* Order
    - signal::pre_display
    - -> Player
    - -> Game
    - turn
    - getForm()
    - getCost()

Views:
* /game/:game/players
* /game/:game/orders
* /game/:game/orders/new/:order
* /game/:game/orders/:order_id
* /game/:game/orders/:order_id/delete
* /game/:game/messages

#### Module architecture
Engine modules can be standard Django apps, with models and views. To use as a module, call `engine.registerModule(taskBuilder, orders, views, setup)`, where:

* `taskBuilder` is a function which will be called with the current game, and must returns a list of ResolveTasks to handle resolution
* `orders` is a list of Orders to register
* `views` is a dict whose keys are regexp and values associated functions. If a conflict occurs between multiple apps, the last entry prevails.
* `setup` is a function to call on game initialisation

### Engine modules

#### engine.influence
Player level of influence

Models:
* Influence
    - -> Player
    - level

Resolution:
* (90) Buying influence

#### engine.corporations
Base models for everything corporation related.

Models:
* CorporationDefinition
    - name
    - description
* Corporation
    - -> CorporationDefinition
    - -> Game
    - assets

Setup: create corporations for this game, define initial shares

Views:
* /game/:game/corporations/corporation/:id : corporation details

#### engine.corporations.orders
Basic Orders issued around corporations : buy share, vote, speculate

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

Resolution:
* (0) BuyShareOrder
* (10) VoteOrder
* (70) SpeculationOrder
* (80) DividendDistribution

#### engine.corporations.assets_history
Store the corporation assets turn by turn, to display stocks graphs.

Models:
* CorporationAsset
    - ->corporation
    - assets
    - turn

Resolution:
* (100) RegisterAssets

Views :
* /corporations/market

#### engine.corporations.invisible_hand
Invisible market hand.

Resolution:
* (40) InvisibleHand

#### engine.corporations.citizenship
Deal with corporation citizenship

Models:
* Citizenship
    - -> Corporation
* CitizenshipOrder
    - -> Corporation

Resolution:
* (90) SwitchCitizenship

#### engine.corporations.effects
Apply first / last effects

Models:
* CorporationEffect
    - -> Corporation
    - onFirst
    - onFirstDescription
    - onLast
    - onLastDescription

Resolution
* (60) FirstLastEffect
