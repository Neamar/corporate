Corporate game
===============

[![Circle CI](https://circleci.com/gh/Neamar/corporate.svg?style=svg)](https://circleci.com/gh/Neamar/corporate)

> You think this is a game? This is not. This is only The Game.

## What's this ?
Corporate Game (CG) is a small, fun online game. Players compete to trade corporations assets, hoping to one day beat the market.

## Installation
This is a standard Django project. Check you meet all the requirements listed in `requirements.txt`, then run `./manage.py syncdb` to create the database.

Once you're done, run `./manage.py runserver` to get started on http://localhost:8000/.
You'll need to create a game and add some players in it.

## Game data
Rules can be found in [data/docs/index.md](data/docs/index.md).

### Tasks list
> Number between [] is the resolution order.

* [0] **BuyShareTask** : Buy all shares for all players
* [100] **VoteTask** : Resolve player's corporation votes
* [100] **MDCVoteTask** : Choose the MDC party line, and save it in an MDCVoteSession
* [300] **MDCLineCPUBTask** : Enforce the effects of the MDC CPUB party line
* [349] **ProtectionRunTask** : Debit Protection runs from players
* [350] **OffensiveRunTask** : Resolve Offensive corporations runs (DataSteal, Sabotage, Extraction)
* [350] **InformationRunTask** : Resolve Information runs
* [400] **InvisibleHandTask** : Give +1 and -1 asset for two random corporations
* [600] **FirstLastEffectsTask** : Apply first and last corporations effects
* [650] **SaveCorporationAssetTask** : Save the assets of all corporations after the turn resolution
* [800] **DividendTask** : It's time to get money!
* [900] **CitizenshipTask** : Update players citizenships
* [900] **CorporationSpeculationTask** : Resolve corporations speculations
* [1000] **BuyInfluenceTask** : Buy new Influence level
* [1000] **CrashCorporationTask** : Let's crash corporations that didn't made it through the turn

### Orders list
* **BuyInfluenceOrder** : Order to increase Player Influence
* **VoteOrder** : Order to vote for a Corporation
* **CitizenshipOrder** : Order to become citizen from a new corporation
* **BuyShareOrder** : Order to buy a corporation share
* **DataStealOrder** : Order for DataSteal runs
* **ProtectionOrder** : Order for Protection runs
* **SabotageOrder** : Order for Sabotage runs
* **ExtractionOrder** : Order for Extraction runs
* **InformationOrder** : Order for information runs
* **CorporationSpeculationOrder** : Order to speculate on a corporation's rank
* **MDCVoteOrder** : Order to vote for the MDC coalition
* **WiretransferOrder** : Send money to another player
