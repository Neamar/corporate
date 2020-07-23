Corporate game
===============

[![Circle CI](https://circleci.com/gh/Neamar/corporate.svg?style=svg)](https://circleci.com/gh/Neamar/corporate)

> You think this is a game? This is not. This is only The Game.

## What's this ?
Corporate Game (CG) is a small, fun online game. Players compete to trade corporations assets, hoping to one day beat the market.

## Installation
Install python environment in visual studio and Python 2.7 64bits
Add folowing variables in windows environment variables :
- Debug = true
- AWS_ACCESS_KEY_ID = xxxxxx
- AWS_SECRET_ACCESS_KEY = xxxxxx
- AWS_STORAGE_BUCKET_NAME = xxxxxx
theses should point to read/write S3 instance with a folder named "avatar"
Open corporate-vs.sln in visual studio
Create Python env with python 2.7
Install requirements with requirements.txt
Right clic on project/Python :
- Django Migrate ... (Django > 1.7)
- Collect Static Files
Start project

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
* [500] **UpdateMarketBubblesTask** : Count the bubbles and apply them
* [600] **FirstLastEffectsTask** : Apply first and last corporations effects
* [625] **UpdateMarketBubblesAfterEffectsTask** : Recount the bubbles and apply them again, this time for good
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

### RUN WITH DOCKER
```bash
docker run -p 8000:8000 --name=corpo corporate bash -c "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn corporate.wsgi -w $(( 2 * `cat /proc/cpuinfo | grep 'core id' | wc -l` + 1 )) -b 0.0.0.0:8000 --timeout 1200 --access-logfile '-' --error-logfile '-' --worker-tmp-dir /dev/shm --log-level INFO"
```
