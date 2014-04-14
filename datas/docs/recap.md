## Valeurs numériques (en k¥)
* **Parts**
    * Achat : `100 × (actifs)`
    * Achat dans la première corpo : `125 × (actifs)` (sauf si citoyen corpo)
    * Dividendes : `50 × (actifs)`
    * Dividendes de la première corpo: `75 × (actifs)`
    * Dividendes de la dernière corpo: `25 × (actifs)`
* **Influence** : 
    * Achat : `400 × (nouvel indice)`
* **Runs** :
    * `50 × (paliers de 10%)`
    * Autant de bonus de `30%` que d'IC
* **Spéculation** :
    * Limite de `100 × (influence)`
    * Côte de 1 pour 2 pour les produits dérivés
        - *Nikkei* : Sony, Shiawase, Renraku
        - *Dow Jones* : Ares, NeoNET, Spinrad, Prometheus
    * Côte de 1 pour 3 pour les première et dernière corporation
    * Côte de 1 pour 5 pour les autres
* **MDC** :
    * Nombre de voix : `1 + (nb corpo majoritaire)`
    * *Contrats Publics* :
        - `+1` pour les corpos dans la coalition,
        - `-1` pour les corpos dans *Développement Urbain*,
    * *Développement Urbain* :
        - `-1` pour les corpos dans *Contrats publics*,
    * *Contrôles Ciblés*
        - Pas de Protection pour les joueurs dans *Transparence*
    * *Transparence* :
        - `+20%`  pour les runs contre les corpos,
        - `-20%` pour les runs ciblant les corpos dans *Contrôles Ciblés*
    * *Garde-fous bancaires* :
        - Les spéculations ratées ne font pas perdre d'argent pour les joueurs dans la coalition
    * *Dérégulation*
        - Côtes augmentées de `1` pour les joueurs dans la coalition
        - Pas de spéculation pour les joueurs dans la coalition *Garde-fous bancaires*

## Effets
### Effets premiers
<img src="/static/graphviz/first.svg" alt="Effets premiers" style="width:95%"/>

#### Ares Macrotechnology
* +1 actif pour les deux dernières corpos.

#### NeoNET
* -1 actif pour Spinrad Industries.
* -1 actif pour la 2eme corpo.

#### Shiawase Corporation
* -1 actif pour Renraku.
* +1 actif pour Sony.

#### Renraku Computer Systems
* -1 actif pour Neonet.
* -1 actif pour Shiawase.

#### Sony Corporation
* +1 actif pour Renraku.
* +1 actif pour Shiawase.

#### Aztechnology
* -1 actif pour Horizon 
* -1 actif pour la dernière corpo.

#### Horizon Corporation
* -2 actifs pour la dernière corpo.

#### Saeder Krupp
* -2 actifs pour la 2eme corpo.

#### Spinrad industries
* +2 actifs pour Spinrad.

#### Prometheus Engineering
* +1 actif pour Prometheus
* +1 actif pour la deuxième corpo.

### Effets derniers :
<img src="/static/graphviz/last.svg" alt="Effets derniers" style="width:95%"/>
#### Ares Macrotechnology
* -1 actif pour les deux premières corpos.
>
#### NeoNET
* +1 actif pour NeoNET.
* +1 actif pour Renraku.

#### Shiawase Corporation
* -1 actif pour l'avant-dernière corpo.
* -1 actif pour Sony.

#### Renraku Computer Systems
* -1 actif pour Sony.
* +1 actif pour Shiawase.

#### Sony Corporation
* -2 actifs à l'avant dernière corpo.

#### Aztechnology
* +2 actifs pour Horizon.

#### Horizon Corporation
* +1 actif pour Aztechnology.
* -1 actif pour la première corpo.

#### Saeder Krupp
* +2 actifs pour Saeder Krupp.

#### Spinrad industries
* -1 actif pour Spinrad.
* +1 actif pour l'avant dernière corpo.

#### Prometheus Engineering
* +2 actifs pour la première corpo.
