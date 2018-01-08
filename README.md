# Projet de moteur de recherche - RI Web

## Questions et sujet

Pour chaque collection répondre aux questions suivantes :

1. Question 1 : Combien y-a-t-il de tokens dans la collection ?
2. Question 2 : Quelle est la taille du vocabulaire ?
3. Question 3 : Calculer le nombre total de tokens et la taille du vocabulaire pour la moitié de la
collection et utiliser les résultats avec les deux précédents pour déterminer les paramètres k et b de la
loi de Heap.
4. Question 4 : Estimer la taille du vocabulaire pour une collection de 1 million de tokens (pour chaque
collection).
5. Question 5 : Tracer le graphe fréquence (f ) vs rang (r) pour tous les tokens de la collection. Tracer
aussi le graphe log(f ) vs log(r).

## ODG sur les collections données

### CACM
- nb_tokens = 100 000 ... 250 000
- taille_voc = 9 000
- k = 20 ... 40
- b = 0,4 ... 0,5

### Stanford
- nb_tokens = 25 000 000
- taille_voc = 400 000

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

## TODO

- [x] Construire CLI booléen
- [x] Construire CLI vectoriel

### Collection CACM

- [x] Identifier documents, puis les opérandes
- [x] Tokeniser les élements
- [x] Comparer avec la stop list
- [x] Construire l'index inversé
- [x] Prévoir un système d'import / export d'index dans un fichier pour sauvegarde
- [x] Ecrire l'algo de recherche vectoriel
- [x] Ecrire l'algo de recherche booléen
- [ ] Ecrire les méthodes de pondération pour une requete
- [x] Afficher les informations de performance pour une requete
- [ ] Créer des test de pertinence : courbe rappel/précision, F-Measure, E-Measure et R-Measure, Mean Average Precision

### Collection Stanford

- [x] Charger les documents de la collection
- [ ] Indexer la collection stanford avec une reprsentation par bloc, et avec une approche map-reduce pour l'indexation des blocs , algo BSBI -> Yoann
- [x] Prévoir un système d'import / export d'index dans un fichier pour sauvegarde
- [ ] Adapter l'algo de recherche vectoriel de CACM
- [ ] Adapter l'algo de recherche booléen de CACM
- [ ] Ecrire les méthodes de pondération pour une requete
- [x] Afficher les informations de performance pour une requete
- [ ] Créer des test de pertinence : courbe rappel/précision, F-Measure, E-Measure et R-Measure, Mean Average Precision
- [ ] Compresser l'index inversé
