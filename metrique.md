![](./assets/NAD_mark_1.webp)

# Gestion des métriques

Contrairement aux logues qui sont des informations laissé par un système, les métriques sont des mesures que nous faisons sur le système afin d'évaluer son niveau de *santé*.

## Les 4 signaux d'or

Il existe 4 catégories de métriques. Lorsqu'un service dans un réseau a un problème rencontré par un client, il est important de pouvoir visualiser **au moins** **une métrique par signal** pour **chaque services**.

- **Latence**
  - Le temps qu'uue requête à un service prend
    - Par exemple: Si votre service retourne des erreurs 500 lorsqu'il reçoit une requête HTTP et que la **latence est basse** (la requête retourne une erreur 500 très rapidement), ce n'est probablement pas le même problème que si votre service retourne des erreurs 500 mais que la **latence est haute**.
    - Dans cet exemple, une latence basse pourrait signaler qu'une dépendance du service n'est pas *up* (par exemple une base de données), tandis qu'une latence élevé pourrait indiquer un problème bien plus grave.
    - C'est pourquoi il est primordiale de **mesurer la latence des erreurs**
- **Trafique**
  - Mesure la demande pour un service données.
    - ex: Taux de requête HTTP, taux de trafique réseau I/O, nombre de transaction dans une base de données, nombre de connexion ou de client connecté à un service.
- **Erreurs**
  - Le taux de requêtes qui cause des erreurs.
    - ex: Taux de requêtes qui échouent explicitement (erreurs 500)
- **Saturation**
  - À quel point un service donnée est à pleine capacité (100%).
  - ex:
    - mémoire vive
    - mémoire de stockage
    - capacité du CPU
    - nombre de connection
  - Il est important de comprendre que la majorité des services vont se dégrader avant même d'atteindre le 100%. Donc dans le chapitre sur les alertes, il sera important de se doter d'une cible de capacité dont le service ne doit pas dépasser
    - ex:
      - capacité de la base de données ne doit pas dépasser 80% car au delà de ce seuil, le temps de réplication augmente rapidement et ralentit considérablement la base de données
      - la mémoire vive ne doit pas dépasser le seuil de 90% car sinon le *swappiness* (conversion de mémoire vive en mémoire dur) consomme trop de ressources
  - Ce signal permet aussi de faire des prédictions sur les saturations futures.
    - Par exemple: déterminer qu'avec le taux actuel de données qui sont écrient dans la base de données, celle-ci sera pleine dans 4h

## Essence vs phénomène

Lors du diagnostique, les 4 signaux permettent d'apporter plusieurs dimensions à la problématique et permet d'écarter les **phénomènes** et de pouvoir cerner l'**essence** du problème.

### Phénomènes

Problématiques secondaire causé par la racine du problème. Exemple, de la **latence causé par une saturation**.

### Essence

La racine du problème et des phénomènes qui en découle. Exemple, un système qui est *down* qui a causé de la latence sur les autres services du réseau.

Exemple:

Une application peut avoir des erreurs 500 (signal d'erreurs), mais ce n'est qu'un **phénomène** causé par une augmentation du temps des requêtes HTTP à un API (signal latence) qui cause un *timeout*. Cette latence peut elle aussi être un **phénomène** causé, par exemple, par une saturation d'un service de base données dans le réseau qui serait dans ce cas-ci l'**essence** de la problématique.

Donc, la dépendance des divers problème rencontrer serait le suivant:

Base de données saturé (**essence**) → Latence de l'API (**phénomène**) → Erreur 500, *timeout* (**phénomène**)
