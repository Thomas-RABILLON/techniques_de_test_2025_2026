# RETEX

## Tests unitaires et implémentation du modèle

Pour les tests unitaires, j’ai commencé par les implémenter comme décrit dans le [plan](./PLAN.md). Au début, j’ai perdu du temps car, pour coder les triangles et les points, je faisais des tests avec des bytes en dur. J’ai finalement découvert le module `struct`, qui permet d’encoder facilement des données en bytes, ce qui a grandement simplifié le processus.

Pendant l’implémentation, je me suis rendu compte que je n’avais pas suffisamment prévu de tests pour les données erronées pouvant provoquer des erreurs. J’ai donc adapté mes tests pour qu’ils vérifient les erreurs attendues :

* `ValueError` pour les problèmes de valeurs (par exemple, bytes trop courts)
* `TypeError` pour les mauvais types de données (par exemple `None` ou `str` au lieu de `float`)
* `IndexError` pour les `Triangle`, si des indices de point utilisés ne correspondent à aucun point existant dans le `PointSet`

Chaque méthode possède maintenant des tests couvrant les erreurs possibles, en plus des tests vérifiant le bon fonctionnement normal.

Bien que j’aie dû ajouter quelques tests supplémentaires pendant l’implémentation pour des cas que je n'avais pas prévus, je trouve que l'implémentation a été grandement simplifiée grâce au fil directeur fourni par les tests.

## Tests d’intégration/end-to-end et implémentation des endpoints

Pour les tests d’intégration/end-to-end, je n’ai pas rencontré de difficulté majeure, suivant simplement mon plan de test. J’ai cependant ajouté un test sur l’endpoint `pointset`, car j’avais oublié de vérifier le cas d’un `PointSetID` non-existant.

J’ai choisi de ne pas mocker l’API, estimant que cela prendrait trop de temps. Mes tests utilisent donc l’API finale, ce qui nécessite que le serveur Flask soit démarré. Pour pouvoir faire des requêtes à l'API, j’ai utilisé le `test_client` de Flask.

## Tests de performance

Les tests de performance ont été, pour moi, les plus difficiles. L’implémentation des tests en soi n’était pas problématique, mais l’estimation d’un temps “type” pour l’exécution de l’algorithme l’était. Mes prévisions initiales étaient trop optimistes, notamment pour le test avec 10 000 points, probablement parce que mon algorithme de triangulation n’est pas ultra-optimisé. J’ai donc ajusté à la hausse le temps attendu pour ce test.

Pour les tests sur de plus petits ensembles de points, j’ai fait tourner l’algorithme plusieurs fois avec des points différents et aléatoires, et calculé la moyenne des temps d’exécution. Le test avec 10 000 points n'est exécuté qu’une seule fois, car il prend trop de temps.

## Qualité du code

La qualité du code ne m’a pas posé de difficultés particulières, à part certaines erreurs `ruff` que j’ai eu du mal à comprendre.

Finalement, je n’ai plus d’erreurs `ruff` et j’ai atteint un coverage de 98 %. Ce score élevé est certainement dû à l’ajout de tests pendant l’implémentation, pour couvrir des cas que je n’avais pas initialement prévus. Malgré ce coverage très élevé, je ne pense pas avoir créé de tests inutiles.

Pour ce qui est de la documentation, je n'ai pas eu de problème particulier, l'extension VSCode `autodocstring` m'a bien aidé à structurer mes docstrings. Vous pourrez la trouver dans le dossier `docs`.

## Ce que j’ai bien fait et ce que j’aurais pu améliorer

Je pense que le fait d'avoir alimenter mes tests pendant l’implémentation a été bénéfique car cela a amélioré la qualité globale de mes tests et m’a fait réaliser à quel point un TDD est difficile à mettre en place. Il est quasiment impossible de prévoir toutes les situations qui méritent d’être testées à l’avance.

J’aurais pu mieux réfléchir à la mise en place des tests et anticiper davantage de cas, par exemple pour vérifier si l’algorithme renvoie des triangles qui se croisent (dans `test_triangulation`, test : `test_croisement`), que j'ai rajouté pendant l'implémentation.

## Conclusion

Ce TP a été une expérience enrichissante, car c’est la première fois que je pratique réellement le TDD, bien que j’aie déjà étudié les tests en profondeur durant mon BUT. J’ai pu mesurer la difficulté de mettre en place un bon TDD, mais aussi constater que c’est une excellente approche car elle facilite grandement l’implémentation de la logique ensuite.
