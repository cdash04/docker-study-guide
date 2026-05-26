# Gestions de logs dans une application gérer en micro-services

![](./assets/NAD_mark_1.webp)

## Niveau de sévérité des logs

Dans les années 1980, [syslog](https://en.wikipedia.org/wiki/Syslog) avait définit les niveaux de sévérités suivants pour les systèmes *UNIX*:

1. `emerg`: Indique que le système **n'est plus utilisable** et nécessite une attention immédiate
2. `alert`: Indique qu'une **intervention immédiate** est nécessaire afin de régler un problème critique
3. `crit`: Indique que le programme est dans une **situation critique** et qu'une attention immédiate est nécessaire afin de **prévenir** le système de planter
4. `error`: Indique que des erreurs **altèrent** des opérations 
5. `warn`: Indique une erreur potentiel qui **pourrait éventuellement** mener à une erreur
6. `notice`: Indique des opérations normales, mais **observation supplémentaire pourrait être requis selon les circonstances**
7. `info`: Indique des **opérations normales** du système
8. `debug`: Indiques des informations pertinentes **lors de débogages** seulement

## *Frameworks* de logs

Il est important dans un système de log de ne pas utiliser les librairies d'affichages des langages de programmations. Par exemple: `print` en *python*, `Debug.WriteLine` en *C#*, `system.out.println` en *Java* et `console.log` en *javascript*.

La raison est que les *frameworks* de logs sont plus **personnalisable** et **flexible**. Par exemple, on peut attribuer à un log, un **niveau de sévérité**, un ***timestamp***, ou un **ID de traçage** beaucoup plus facilement.

Des exemples de librairies pour les langages cités plus haut sont `logger` pour *python*, `Log4net` pour *C#*, `Log4j` pour *Java* et `winston` pour *javascript*.

Puisque l'exemple suivant est réalisé en *Node JS*, la librarie `winston` sera utilisé.

Les niveaux de sévérité des frameworks de logs ressemblent habituellement beaucoup à ceux de *syslog*. Par exemple, pour `winston`, les niveaux sont:

```js
const levels = {
  error: 0,
  warn: 1,
  info: 2,
  http: 3,
  verbose: 4,
  debug: 5,
  silly: 6
};
```

## Agrégateur de logs

C'est bien beau de produire des logs, mais s'ils ne sont pas entreposé et qu'il n'ets pas possible de les analyser lors d'incident, elles ne servent à rien. C'est pourquoi il est important d'avoir un agrégateur afin d'avoir une rétention sur les logs qu'on produit. Dans le cadre de cet exemple, [Loki](https://grafana.com/docs/loki/latest/) sera utilisé comme agrégateur de logs.

**Loki** agrège et entrepose les logs dans une base de données. Il est ensuite possible de visualiser les logs avec des requêtes [LogQL](https://grafana.com/docs/loki/latest/query/).

Afin de visualiser les logs, nous allons utiliser [Grafana](https://grafana.com), un outil de visualisation de métriques, logs et traces.

### Visualiser les logs de *Loki* avec *Grafana*

Le *docker compose* est déjà configuré avec un serveur grafana et loki fonctionnel. De plus, l'*API* a déjà été configuré afin d'envoyer ses logs à *Loki*. Cependant, il faut ajouter un *data source* à grafana afin qu'il se connecte à Loki.

1. Connectez-vous au *dashboard* de *grafana* via le proxy en utilisant l'adresse http://localhost/grafana
2. Identifiez-vous, l'utilisateur et le mot de passe sont tous les deux **admin**
   1. Des fois, une fois authentifier, il faut actualiser la page afin que ça fonctionne
3. Allez dans Connections -> Data sources et cliquez sur *Add data source*
4. Sélectionnez le service Loki et ajoutez l'adresse de Loki, soit http://loki:3100.
5. Cliquez sur *Save & test*
6. Vous pouvez maintenant visualiser les logs de Express JS dans l'onglet Drilldown -> Grafana Logs Drilldown

### Requête de log

Il est possible de faire des requêtes sur les logs avec *Grafana* et *Loki* en utilisant *LogQL*.

Les logs dans Loki ont 3 parties:

- L'Horodatage (*timestamp*)
- Les étiquettes/sélecteur (*labels*/*selectors*)
- Contenue du log

Ex:

```log
2026-03-31 10:08:35.570 { "level": "info", "appName": "Express" } INFO GET /health
```

Le *timestamp* `(2026-03-31 10:08:35.570)` et les *labels* (`{ "level": "info", "appName": "Express" }`) sont indexés, mais pas le contenu de la log.

### Format de logs

Les requêtes *LogQL* ont le format suivant:

`{ sélecteur flux de log } | pipeline de log`

### Sélecteur de flux

Les *sélecteurs* sont une combinaison d'étiquettes (*labels*). La combinaison d'étiquette se nomme un flux (*stream*). Le but du sélecteur est de limiter la quantité de logs avant de traiter ou de filter les logs.

Les sélecteurs sont spécifiés grace à des pairs de clé/valeur comme suit:

`{ appName="Express", level="info" }`

4 opérations possible sur les sélecteurs:
- `=` : l'étiquette possède exactement la valeur du sélecteur
- `!=` : l'étiquette ne possède pas la valeur du sélecteur
- `=~` : l'étiquette correspond à l'expression régulière du sélecteur
- `!~` : l'étiquette ne correspond pas à correspond à l'expression régulière du sélecteur

Exemples:

- Afficher toutes les logs de niveaux `info` de l'application *Express*:

`{ appName="Express", level="info" }`

- Afficher toutes les logs sauf les erreurs:

`{ level!="error" }`

- Afficher seulement les logs de niveau `info` ou `error`:

`{ level=~"(info|error)" }`

- Afficher seulement les logs qui ne sont pas de niveau `info` ou `error`:

`{ level!~"(info|error)" }`

### Pipeline de flux

Le flux sert principalement à faire les traitements suivants sur les logs:
- filter
- personnaliser
- formatter

Dans le cadre de ce cours, nous allons surtout nous attarder au filtrage, mais sachez qu'il est possible d'ajouter des fonctions de formatage au pipeline afin de modifier la façon dont les logs seront retournées.

#### Filter

Permet de filtrer les logs en fonction des étiquettes ou du contenu des logs.

4 opérations sont disponibles pour filtrer le contenu de la log:

- `|=` : Le log contient la chaîne de caractère
- `!=` : Le log ne contient pas la chaîne de caractère
- `|~` : Le log a une une correspondance avec l'expression régulière
- `!~` : Le log ne contient aucune correspondance avec l'expression régulière

Par exemple:

- Conserver seulement les logs qui mentionne le mot *db*:

`{ appName="Express",level="error" } |= "db"`

- Ignorer les nombreux logs causés par le *health check*:

`{ appName="Express",level="info" } != "/health"`


Comme tout pipeline qui se respecte, les opérations peuvent se succéder les uns les autres. Par exemple, cette requête retourne toutes les erreurs et les infos de l'application *Express*, ensuite séquentiellement les logs contenant `GET` sont conserver et ensuite ceux qui contiennent `/health` sont retiré.

`{ appName="Express",level=~"(info|error)" } |= "GET" != "/health"`


#### Fonction de gabarit

Grafana fournit [plusieurs fonction](https://grafana.com/docs/loki/latest/query/template_functions/) permettant de personnaliser les logs en sorties. Je vous invite à les consulter si vous êtes curieux.