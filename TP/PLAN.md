# Plan de test

## Objectif

Mettre en place un ensemble de tests pour vérifier le bon fonctionnement du micro-service de triangulation, et notamment :

- la justesse des calculs de triangulation  
- le respect du format des données comme indiqué dans le [sujet](./SUJET.md#représentations-de-pointset-et-triangles)  
- la robustesse face aux erreurs  
- les performances du micro-service  
- la qualité du code

## Organisation des tests dans le code

Chaque module (`PointSetManager`, `Triangulator`) aura l'organisation de tests suivante :

```
{nom_du_module}/
|--- tests/
│   |-- unit/
│   |-- integration/
│   |-- performance/
```

## Tests unitaires

### `PointSetManager`

| Test              | Pourquoi              | Comment               |
|-------------------|-----------------------|-----------------------|
| Conversion d'un `PointSet` en binaire | Vérifier que l'encodage soit conforme | Avec différents jeux de points, tester si leur format binaire correspond à ce qui est attendu |
| Conversion d'un binaire vers un `PointSet` | Vérifier que la lecture du format binaire soit correcte | Avec différents jeux de points, tester si la lecture du format binaire renvoie l'objet attendu |

Pour chaque test, des données valides mais aussi des données invalides seront fournies pour ne pas avoir uniquement des "happy paths".  
Exemples de données invalides utilisables pour tester les cas ci-dessus :

- des points qui ont des coordonnées invalides (vides, NaN, None)  
- des binaires tronqués, avec plus (ou moins) de bytes par rapport au format souhaité  
- le nombre de points indiqué dans un `PointSet` ne correspond pas au nombre de points réels  

### `Triangulator`

| Test              | Pourquoi              | Comment               |
|-------------------|-----------------------|-----------------------|
| Conversion d'un `Triangle` en binaire | Vérifier que l'encodage soit conforme | Avec différents jeux de triangles, tester si leur format binaire correspond à ce qui est attendu |
| Conversion d'un binaire vers un `Triangle` | Vérifier que la lecture du format binaire soit correcte | Avec différents jeux de triangles, tester si la lecture du format binaire renvoie l'objet attendu |
| Triangulation simple | Vérifier que l'algorithme est capable de créer un seul triangle valide | Avec un jeu de trois points, tester si un triangle composé des trois points est renvoyé |
| Triangulation complexe | Vérifier la cohérence d'un ensemble de triangles créés | Avec un jeu d’un certain nombre de points, tester si le nombre de triangles renvoyé est cohérent avec les points donnés et vérifier que des triangles ne se chevauchent pas |

Pour chaque test, des données valides mais aussi des données invalides seront fournies pour ne pas avoir uniquement des "happy paths".  
Exemples de données invalides utilisables pour tester les cas ci-dessus :

- des triangles qui ont des points avec des coordonnées invalides (vides, NaN, None)
- des binaires tronqués, avec plus (ou moins) de bytes par rapport au format souhaité
- des triangles avec plus de sommets que de points
- le nombre de triangles indiqué ne correspond pas au nombre de triangles réels contenus dans l'objet
- tester la création d'un triangle avec des points colinéaires ou un ensemble de point trop petit (2 points)

## Tests d'intégration

### `Triangulator`

| Test              | Pourquoi              | Comment               |
|-------------------|-----------------------|-----------------------|
| Requête vers `/triangulation/{pointSetId}` | Vérifier le bon fonctionnement de l'end-point | En simulant un appel API et en observant la réponse obtenue |

Ce test n'aura pas pour but de vérifier que les triangles renvoyés correspondent à ce qui est attendu, car ceci est le rôle des tests unitaires définis plus haut ([ici](./PLAN.md#triangulator)).  
Voici des exemples de données utilisables pour les tests ci-dessus :

- un `PointSetID` existant  
- un `PointSetID` inexistant  
- un `PointSetID` vide  
- un `PointSetID` avec un triangle incalculable (points colinéaires ou pas assez de points)  

### `PointSetManager`

| Test              | Pourquoi              | Comment               |
|-------------------|-----------------------|-----------------------|
| Requête vers `/pointset` | Vérifier l'enregistrement d'un `PointSet` | En simulant un appel API et en observant la réponse obtenue |
| Requête vers `/pointset/{pointSetId}` | Vérifier le bon fonctionnement de l'end-point | En simulant un appel API et en observant la réponse obtenue |

Le but de ces tests sera de vérifier que l'API renvoie les réponses appropriées par rapport à ce qui lui est envoyé.  
Voici des exemples de données utilisables pour les tests ci-dessus :

- un `PointSetID` existant  
- un `PointSetID` inexistant  
- un `PointSetID` vide  

## Tests de performance

| Test              | Pourquoi              | Comment               |
|-------------------|-----------------------|-----------------------|
| Triangulation de 100 points | Vérifier la rapidité de l'algorithme sur un petit volume de points | Lancer plusieurs fois la triangulation des 100 points, mesurer le temps à chaque fois et faire une moyenne, puis comparer cette moyenne à un seuil (pas encore défini) au-dessus duquel il est considéré que l'algorithme est trop lent |
| Triangulation de 1 000 points | Vérifier la montée en charge de l'algorithme | Lancer plusieurs fois la triangulation des 1 000 points, mesurer le temps à chaque fois et faire une moyenne, puis comparer cette moyenne à un seuil (pas encore défini) au-dessus duquel il est considéré que l'algorithme est trop lent |
| Triangulation de 10 000 points | Vérifier la robustesse de l'algorithme (pas de dépassement, etc.) | Lancer un nombre limité de fois la triangulation pour 10 000 points, et calculer le temps moyen d'exécution |

Le but de ces tests est de vérifier que l'algorithme ne plantera pas et permettra une réponse rapide, que ce soit pour une utilisation normale (100 points), élevée (1 000 points) ou extrême (10 000 points) du micro-service.

## Tests de qualité

| Test                      | Pourquoi                                 | Comment                                     |
| ------------------------- | ---------------------------------------- | ------------------------------------------- |
| Lint (`ruff`)           | Garantir la propreté du code.            | Lancer `make lint` et corriger les erreurs. |
| Couverture de code (`coverage`)   | Vérifier que le code est bien testé.     | Lancer `make coverage`.                     |
| Documentation (`pdoc3`) | Vérifier que le code est bien documenté. | Générer la doc avec `make doc`.            |

## Critères de validation

- Tous les tests passent (unitaires, intégration, performance, qualité)  
- Couverture de code ≥ 90 %  
- Aucun avertissement `ruff`  
- Documentation générée sans erreur  
- Temps de calcul raisonnable sur les gros jeux de données  
