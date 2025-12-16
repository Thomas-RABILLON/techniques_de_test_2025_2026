# RETEX

Lors de ce TP, j'ai eu l'occasion de faire du TDD pour la première fois, bien que j'aie déjà eu l'occasion d'aborder les tests en profondeur durant mon BUT.

J'ai trouvé plutôt difficile de mettre en place le TDD, notamment en raison de la complexité de la triangulation et du fait de ne pas avoir de code déjà existant à tester. Il fallait donc que je crée mes tests tout en pensant à la manière dont je pourrais implémenter la logique.

Dans ma première version des tests, je me suis contenté d'implémenter les tests que j'avais décidés dans le [plan](./PLAN.md). Mais, au fur et à mesure de l'implémentation, je me suis rendu compte que je devais en rajouter, car certains cas étaient manquants.

Une fois les tests unitaires en place, je n'ai pas eu de problème pour implémenter la logique des classes testées. De même pour les tests d'intégration/end-to-end, j'ai seulement dû modifier quelques tests, car j'avais remarqué que je ne testais pas certains codes de retour.

La partie difficile a été de mettre en place les tests de performance, car l'algorithme de triangulation est assez complexe et il est difficile de définir un temps d'exécution. De plus, mon implémentation n'est pas très optimisée et elle met beaucoup plus de temps que ce que j'imaginais au début pour un grand nombre de points.

Pour finir avec la qualité, je n'ai pas vraiment eu de problème avec ruff, bien que j'aie eu du mal à comprendre certaines erreurs. J'ai réussi à obtenir un coverage de 98 %, car en rajoutant des tests auxquels je n'avais pas pensé au cours du temps, j'ai pu tester quasiment tous les cas importants. Même si ce coverage est plutôt élevé, je ne pense pas avoir de tests « inutiles ».

Pour conclure, ce TP m'a permis de vraiment comprendre les difficultés à mettre en place un TDD, mais aussi son importance, car j'ai remarqué que l'implémentation de la logique devenait beaucoup plus simple, puisque je l'avais déjà "structurée" grâce aux tests.
