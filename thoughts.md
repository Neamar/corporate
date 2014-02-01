# Corporate Game Manhattan.

## Concepts
### Ordres disponibles
* Acheter un point d'influence corpo *(une fois par tour)*
* Acheter une part *(dispo autant de fois qu'influence corpo)*
    - Paramètre :
        + Corpo
* Voter *(dispo autant de fois qu'influence corpo)*
    - Paramètre :
        + Corpo+
        + Corpo-
* Spéculation sur une corporation *(dispo autant de fois qu'influence corpo - nb spéculations sur produit dérivé)*
    - Paramètre :
        + Corpo
        + Actifs en fin de tour
        + Mise (maxé par influence corpo * 100k)
* Spéculation sur un produit dérivé *(dispo autant de fois qu'influence corpo - nb spéculations sur corporation)*
    - Paramètre :
        + Produit dérivé
        + À la hausse / à la baisse
        + Mise (maxé par influence corpo * 100k)
* Run de Protection *(dispo autant de fois que voulu)*
    - Paramètre :
        + Corpo bénéficiaire
        + Pourcentage
        + Bonus de 30%
* Run de Sabotage *(dispo autant de fois que voulu)*
    - Paramètre :
        + Corpo victime
        + Pourcentage
        + Bonus de 30%
* Run de Datasteal *(dispo autant de fois que voulu)*
    - Paramètre :
        + Corpo victime
        + Corpo bénéficiaire
        + Pourcentage
        + Bonus de 30%
* Run d'Effraction *(dispo autant de fois que voulu)*
    - Paramètre :
        + Corpo victime
        + Corpo bénéficiaire
        + Pourcentage
        + Bonus de 30%
* Run d'Information *(dispo autant de fois que voulu)*
    - Paramètre :
        + Joueur cible
        + Pourcentage
        + Bonus de 30%
* Changer de nationalité corpo *(une fois par tour)*
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
Engine modules are standard Django apps, in the `engine_modules` folder.

They can implement:
* `tasks.py` : `tasks` can include a list of tasks to instanciate and run at each resolution
* `orders.py` : `orders` can include a list of Orders (models) available to the player

### Engine modules

#### engine.influence
Player level of influence

Models:
* Influence
    - -> Player
    - level
* BuyInfluenceOrder
    - -> Player

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

Resolution:
* (0) BuyShareOrder
* (10) VoteOrder
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

Resolution:
* (60) FirstLastEffect

#### engine.corporations.speculation
Spéculation corporation : si mauvaise valeur, mise perdue. Sinon, mise * 2 (quitte ou triple)
Spéculation produit dérivé : si égalité, argent conservé. Si mauvais sens choisi, mise perdue. Sinon, mise * 1 (quitte ou double)

Models:
* DerivativeProduct
    - <-> M2M Corporation
    - Name

Resolution:
* (70) SpeculationOrder
 
#### engine.runs
* Run
    - 30% bonus
    - price

#### engine.corporation_runs
Base application for everything run related.

Models:
* ProtectionRunOrder
    - ->protected_corporation
* SabotageRunOrder
    - ->sabotaged_corporation
* DatastealRunOrder
    - ->stolen_corporation
    - ->stealer_corporation

Resolution:
* (30) ProtectionRun
* (35) SabotageRun / DatastealRun

## Frontend
### Wall Street
Tableau des corpos :
* Nom de la corpo
* Actifs actuels
* Delta dernier tour
* Effet premier dernier
* Effet ligne

Renraku     15      +3      +1-1+1

Graphique de la bourse

foreach corpo:
    graphique de la corpo

### Corporations
Tableau des corpos:
* Nom de la corpo
* Actifs
* Défense
* Citoyens

#### Corporation
Nom
Logo
Actifs actuels
Parts possédées
Citoyen corpo
Ligne votée
Défense
Description
Graphique de la corpo
Effet premier dernier
Vote de ligne

### Joueurs
Tableau des joueurs :
* Nom du joueur
* Citoyenneté
* IC
* Vote

Tableau croisé :
* Nom du joueur
* Corporation
* en gras cellule citoyenneté corpo

#### Joueur
    * Nom
    * avatar
    * description
    * ic
    * citoyenneté
    * parts
    * vote

### Newsfeeds
Récapitulatif :
* Ligne du tour

Rapport public de fin de tour
    * runs publiques
    * ligne choisie (+ détails)
    * achat de parts
    * bref, tout le public

### Commlink
MEssages privés entre PJ et de fin de tour, résultat runs d'informations
