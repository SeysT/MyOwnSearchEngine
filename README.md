# Projet de moteur de recherche - RI Web

## Questions et sujet
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
- nb_tokens = 100 000 ... 250000
- taille_voc = 9 000
- k = 20 ... 40
- b = 0,4 ... 0,5

### Stanford
- nb_tokens = 25 000 000
- taille_voc = 400 000

## TODO
1. Traiter la colection CACM
1. Identifier documents, puis les opérandes
2. Tokeniser les élements
3. Comparer avec la stop list
2. Construire l'index inversé
3. Prévoir un système d'import / export d'index dans un fichier pour sauvegarde
1. Mettre en place l'algo BSBI
2. Avoir une approche distribuée de l'index avec MapReduce (=> à éclaircir)
4. Construire un CLI pour analyser les requêtes simples du modèle booléen
5. Construire un CLI pour la requête du moteur de recherche vectoriel
1. Construire une liste ordonnée de réponses, en fonction de la pertinence de plusieurs mesures et méthodes de pondération à tester
2. Le programme doit faire une mesure de pondération entre la requête et le résultats
6. Construire une évaluation de la pertience des résultats sur la collection CACM
