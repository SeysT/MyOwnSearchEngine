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

### Parsing des collections (`models/document.py`)
Nous avons des classes qui représentent chaque document et permettent de le parser (particulièrement pour la collection CACM qui a besoin d'être tokenisée).
A chaque document on attribue un id (entier incrémenté) pour l'identifier de manière unique, et réduire la taille de l'index (plutôt que d'utiliser le nom du fichier pour la collection Stanford notamment)

Ensuite nous utilisons des classes représentant les collections de document, ce qui permet de les sauvegarder dans des fichiers uniques, de les charger plus rapidement en mémoire, et d'aggréger des données pour répondre aux questions d'analyse des collections.
La collection Stanford utilise également une classe MetaDocumentCollection qui aggrège plusieurs sous-collections (qui correspondent en fait aux dossiers de la collection). Elle garde la même interface externe qu'une collection (permet d'uniformiser les accès pour les requêtes par exemple) en retournant les mêmes objets, et permet d'avoir une séparation des blocs pour l'approche MapReduce lors de la construction de l'index.


### Construction de l'index inversé : BSBI & approche MapReduce ( `models/reverse_index.py`)
La construction de l'index inversé suit l'algo BSBI :
- on génère une table terme/id (qui est enregistrée en JSON et chargée pour chaque requête)
- pour chaque bloc on aggrège les éléments de la collection par term_id, puis on les trie. On écrit la sortie dans un fichier json temporaire. Dans notre implémentation actuelle, les blocs sont processés 1 par 1 à la suite.
- pendant la phase de reducing, on ouvre tous les fichiers JSON temporaires crées, et on fait un k-way merge en fusionnant les entrées ayant le même term_id, avant de les écrire dans un dernier fichier. Pour s'assurer que la sortie est bien triée, on utilise des buffers contenant la dernière ligne non lue de chaque fichier intermédiaire et on prend le buffer ayant le term_id minimal.


### Parsing de la requête (`engine.py`, `models/parser.py` et `models/request.py`)
TODO

L'accès aux clefs de l'index inversé se fait par table de hachage (une table simple et peu volumineuse reliant un terme et son id attribué arbitrairement). Elle peut se faire soit directement en mémoire si l'index a été chargé (mais consommateur de ressources), soit directement dans le fichier json triés du disque.

### Pondération (`models/poderation.py` et `models/request.py`)
TODO

### Remarques
Le projet n'est pas totalement optimisé par manque de temps mais voici des pistes d'améliorations que nous avons exploré sans les finaliser :
- pour le mapping lors de la création de l'index, on peut utiliser du multiprocessing pour traiter plusieurs blocs en même temps (plutôt que les parser successivement), surtout vu que notre implémentation, le facteur limitant est la puissance de calcul plutôt que la mémoire.
- nous avons utilisé qu'un seul reducer vu que la quantité de données à assembler n'est pas très grande, mais optimalement on devrait trier les entrées de l'index dans différents fichiers par term_id avant d'assembler des différents fichiers en un seul avec plusieurs reducers
- on peut compresser l'index inversé
- on peut séparer les étapes de chargement en mémoire de l'index inversé et de la requête de l'utilisateur dans le CLI pour pouvoir faire plusieurs requêtes


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
