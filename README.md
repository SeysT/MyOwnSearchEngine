# Projet de moteur de recherche - RI Web

## Instructions pour exécuter le Projet

### Installation

Pour faciliter la mise en place du projet, nous utilisons l'outil make :

```
make install
```
Cela téléchargera les collections CACM et Stanford CS276 nécéssaires, installera les librairies python3 utilisées, créera les dossiers nécéssaires à la bonne éxécution du code, construira les collections et les index inversés nécéssaires.
Les collections brutes sont stockées dans Data/CACM et Data/CS276 (fichiers texte), les collections parsées sont stockées sous forme binaire pour réutilisation du programme dans Data/Collection, et les index inversés et les tables de correspondence token / id dans Data/Index (sous forme texte/json).

Le temps total de construction est d'environ 25 min sur un ordinateur moyen, et consomme jusqu'à 1.7GB de mémoire vive.


### Analyse

Une fois le projet buildé, il est possible d'exécuter les fichiers `cacm_questions.py` et `stanford_questions.py` pour générer les réponses aux questions posées dans le sujet (détaillées plus bas dans ce README), et d'exécuter le fichier `cacm_measures.py` pour obtenir les résultats des mesures de pertinence.

### Execution de requêtes

Le fichier `engine.py` est notre moteur de requête. Voici le mode d'emploi du CLI :
```
Usage:
    engine.py cacm (vectorial | boolean) <request> [--collection=<filepath>]
                                                   [--index=<filepath>]
                                                   [--results=<len>]
    engine.py cs276 (vectorial | boolean) <request> [--collection=<filepath>]
                                                    [--index=<filepath>]
                                                    [--results=<len>]
    engine.py (-h | --help)
    engine.py --version

General options:
    -h --help                   Show this screen.
    --version                   Show version.
    -r --results=<len>          Number of results to display [default: 10].
```

Préciser la collection permet de la charger en mémoire à partir du fichier binaire plutôt que de la reconstruire.
Préciser l'index inversé permet au programme de réaliser des requête plus rapidement, mais implique le chargement en mémoire de l'index (peut consommer jusqu'à 3-4GB de RAM). Si cette option n'est pas précisée, l'index n'est pas chargé en mémoire et les recherches de correspondances document / terme se font directement sur le disque (lecture dans un fichier JSON) donc sont plus lentes.

Exemple de requête :
```
python engine.py cacm vectorial information --collection='Data/Collection/cacm.collection' --index='Data/Index/cacm.index'
```


## Structure du projet

L'ensemble des classes et des fonctions utiles sont documentées sous forme de docstring dans les fichiers.



## Questions et sujet

Pour chaque collection répondre aux questions suivantes :

1. Combien y-a-t-il de tokens dans la collection ?
2. Quelle est la taille du vocabulaire ?
3. Calculer le nombre total de tokens et la taille du vocabulaire pour la moitié de la
collection et utiliser les résultats avec les deux précédents pour déterminer les paramètres k et b de la
loi de Heap.
4. Estimer la taille du vocabulaire pour une collection de 1 million de tokens (pour chaque
collection).
5. Tracer le graphe fréquence (f ) vs rang (r) pour tous les tokens de la collection. Tracer
aussi le graphe log(f ) vs log(r).

## Réponses aux questions pour la collection CACM

Le script `cacm_question.py` nous permet de répondre aux questions du sujet pour la collection CACM.

**Question 1 :**

La collection contient 114 383 tokens.

**Question 2 :**

La taille du vocabulaire de la collection vaut 11 179.

**Question 3 :**

La première moitié de la collection CACM contient 32 420 tokens et a un vocabulaire de taille 5 909. On peut alors en déduire les paramètres de la loi de Heap : k = 30,93 et b = 0,51.

**Question 4 :**

Grâce aux paramètres obtenus à la question précédente, si la collection CACM contient 1 000 000 de tokens, alors la taille de son vocabulaire serait d'environ 33 464.

**Question 5 :**

![Graphe des fréquences en fonction du rang de chaque token de la collection](https://github.com/SeysT/MyOwnSearchEngine/blob/master/Data/Answers/cacm_answer_question_5.png)

## Réponses aux questions pour la collection Stanford CS276

Le script `stanford_question.py` nous permet de répondre aux questions du sujet pour la collection CS276.

**Question 1 :**

La collection contient 25 498 340 tokens.

**Question 2 :**

La taille du vocabulaire de la collection vaut 347 071.

**Question 3 :**

La première moitié de la collection CS276 contient 12 753 515 tokens et a un vocabulaire de taille 233 501. On peut alors en déduire les paramètres de la loi de Heap : k = 20,10 et b = 0,57.

**Question 4 :**

Grâce aux paramètres obtenus à la question précédente, si la collection CS276 contient 1 000 000 de tokens, alors la taille de son vocabulaire serait d'environ 54 422.

**Question 5 :**

![Graphe des fréquences en fonction du rang de chaque token de la collection](https://github.com/SeysT/MyOwnSearchEngine/blob/master/Data/Answers/cs_276_answer_question_5.png)
