# Dashboard

Le dashboard est la vitrine qui permet une vue d'ensemble sur les différents services de notre réseau. Il doit y afficher des métriques pour chacun [des signaux d'or](./metrique.md#les-4-signaux-dor).

Le dashboard doit être **facile à lire** et les **différents signaux et métriques doivent être bien identifié**.

D'autres éléments qui peuvent être pertinent pour un dashboard:

- Affiche si le service est up
- Affiche si le service est en santé (est-ce que la route /health retourne un `200`)

## Grafana

## Créer un nouveau dashboard

Jusqu'à présent, Grafana a été utilisé afin de pouvoir visualiser tous les logues et les métriques de nos services. Les dashboards ne font pas exceptions.

Pour créer un dashboard il faut d'abord cliquer sur la section dashboard dans le menu à gauche.

## Ajouter des éléments au *dashboard*

Il faut ensuite cliquer sur *new* et ensuite *new dashboard*.

Pour ajouter des éléments au *dashboard* il faut cliquer sur *add* et ensuite *add visualisation*.

### Visualisation

Il y a plusieurs types de visualisations tel que:

- Plusieurs types de graphiques:
  - séries temporelles
  - graphique à barre
  - gauge
  - barre à gauge
  - table
  - tartes
  - histogramme
  - ect
    - C'est à vous d'utilisez votre bon jugement pour savoir quel type de graphique permet de mieux comprendre les données.
- Champ texte
  - Important afin de délimité des sections en fonction du type de signal **OU** ajouter plus d'information à un graphique si ce n'est pas assez explicite
    - Rien de pire qu'un dashboard qui est difficile à lire. C'est pourquoi il doit avoir seulement les informations nécessaires
- Liste de logues
  - Peut être pertinent d'avoir des logues filtrés du service à même le dashboard.
- Liste d'alertes et si elles ont sonné dernièrement.
- Et plusieurs autres

Ces visualisation servirons à déterminer de quel manières les métriques seront affichées

### Sources de données

Il faut sélectionner la source de données que l'on souhaite visualiser:
- Pour visualiser des logues, il faut sélectionner *Loki*
- Pour des métriques, il faut sélectionner *Prometheus*

### Requête

En fonction de la source de données sélectionné, il faut maintenant faire la requête que l'on souhaite visualiser. La requête sera donc en `promQL` si la source est *Prometheus* ou `logQL` si la source est *Loki*.


## Ajouter des variables

[référence Grafana](https://grafana.com/docs/grafana/latest/visualizations/dashboards/variables/add-template-variables/#add-variables)

Dans les dashboards, les variables sont des valeurs qui peuvent être partager entre tous les éléments du dashboard.

Par exemple, vous avez un dashboard de vos bases de données et vous voulez visualiser les données d'une base de donnée en particulier.

Pour ajouter une variable au dashboard, il faut d'abord cliquer sur *settings* ensuite cliquer sur *Variables* et *Add variable*.

Il existe plusieurs types de variables, tel que:

- Les *query*: les valeurs de la variable sont tirer d'une source de données. Par exemple, les noms des bases de données.
- Intervalle: définir des intervalles de temps (1m, 1h, 1d)
- Constante: Permet de définir des valeurs constante, par exemple, un préfixe d'une métrique.

### Ajouter variable de requête Prometheus

1. Il faut définir le nom de la variable, C'est important car c'est le nom que l'on va utiliser pour référencer notre variable dans le dashboard
1. Sélectionnez variable de type query
2. Sélectionnez la source de donnée *Prometheus*
3. Sélectionnez le type de requête *label values*
4. Sélectionnez l'étiquette dont vous voulez extirper les données (ex: *method*).
5. Sélectionnez une métrique afin de définir les valeurs dont la variable peut avoir (ex: *express_http_request_total*). Cette étape n'est pas obligatoire mais permet de s'assurer des données qui seront affichées pour la variable
6. Vous pouvez aussi ajouter des filtre l'étiquette choisit ou d'autres étiquettes
7. La variable peut maintenant être utilisé dans des requêtes du dashboard. Par exemple:

```promQL
sum by(method) (rate(express_http_request_total{method=~"$method"}[5m]))
```

`method=~"$method"` filtrera toutes les méthodes sélectionnées.

N'oubliez pas `=~` si la variable peut avoir plusieurs résultats possibles.

### Variables globales

Certaines variables globales sont déjà défini dans l'environnement Grafana. Ils ont toujours le préfix `$__`.


- `$__dashboard`
- `$__from` et `$__to`
- `$__interval`
- `$__interval_ms`
- `$__name`
- `$__org`
- `$__user`
- `$__range`
- `$__rate_interval`
- `$__rate_interval_ms`
- `$__timeFilter`
- `$__timezone`

[Référence grafana](https://grafana.com/docs/grafana/latest/visualizations/dashboards/variables/add-template-variables/#global-variables) pour les variables globales

## Exportation dashboard

L'ensemble des configuration d'un dashboard sont sauvegardé dans un fichier `JSON`. Pour obtenir ce fichier, il suffit de cliquer sur *Export* et ensuite *Export as code*.

## Observabilité programmable

*Observability as code*

Pour ajouter encore plus de dynamisme dans les dashboard, il est même possible de programmer des fonctions et plus encore avec du [jsonnet](https://github.com/grafana/grafonnet). Cependant, nous ne verrons pas ça dans le cadre du cours.

## Maquette de dashboard

Grafana propose plusieurs maquette de dashboard [ici](https://grafana.com/grafana/dashboards/). Vous pouvez facilement copier le JSON des maquettes et l'importer dans votre projet Grafana.

Par exemple:

- [PostgreSQL](https://grafana.com/grafana/dashboards/9628-postgresql-database/)
- [Node.JS](https://grafana.com/grafana/dashboards/11159-nodejs-application-dashboard/)
- [NGINX](https://grafana.com/grafana/dashboards/14900-nginx/)

**IMPORTANT**: Les maquettes sont de bon points de départ lors de la création de dashboard. Cependant, il est primordiale de l'adapté. Lors du TP4 je serai extremement exigeant et pénalisant si vous avez juste importé un dashboard sans l'adapter. 
