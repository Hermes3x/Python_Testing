# Rapport de tests

Projet 12 — GÜDLFT · application Flask de réservation de places de compétition.

## Outillage

| Outil | Version | Rôle |
|---|---|---|
| pytest | 9.1.1 | exécution des tests |
| pytest-cov | 7.1.0 | mesure de la couverture |
| coverage.py | 7.15.2 | moteur de couverture |

## Résultats

**56 tests · 0 échec · 100 % de couverture** (88 instructions dans `server.py`).

| Catégorie | Nombre | Ce qu'elle vérifie |
|---|---|---|
| Unitaires | **26** | une fonction appelée directement, sans Flask ni HTTP |
| Intégration | **27** | une requête HTTP — la route et ses collaborateurs |
| Fonctionnels | **3** | un parcours utilisateur complet, plusieurs requêtes enchaînées |

La classification suit la définition du cours OpenClassrooms : « un test faisant appel à une
base de données, une API **ou encore une autre méthode** ne sera pas considéré comme un test
unitaire ».

## Anomalies corrigées

### Issues du dépôt

| Issue | Anomalie | Comportement obtenu |
|---|---|---|
| #1 | un email inconnu provoquait une erreur 500 | message d'erreur, retour à la page de connexion |
| #2 | un club pouvait dépenser plus de points qu'il n'en possède | achat refusé, points inchangés |
| #4 | un club pouvait réserver plus de 12 places | plafond **cumulé** par club et par compétition |
| #5 | les compétitions passées restaient réservables | réservation bloquée, compétition toujours visible |
| #6 | les points n'étaient jamais déduits | déduction effective à chaque achat |
| #7 | pas de tableau des points | route publique en lecture seule |
| #282 | on pouvait réserver plus de places qu'il n'en reste | achat refusé, places inchangées |

### Anomalies trouvées hors issues, en relisant le code

| Anomalie | Comportement obtenu |
|---|---|
| `/book` avec un nom de club ou de compétition inexistant → erreur 500 | message d'erreur |
| le test `if foundClub and foundCompetition` était inatteignable (code mort) | condition désormais effective |
| la page d'erreur de `/book` recevait une chaîne au lieu d'un club | page correctement remplie |
| champ « places » vide → erreur 500 | message d'erreur |
| places négatives acceptées : le club **gagnait** des points | saisie refusée |
| places à zéro acceptées | saisie refusée |
| `/purchasePlaces` avec un nom inexistant → erreur 500 | message d'erreur |

## Architecture de test

Toute la logique métier a été extraite de `server.py` en six fonctions pures, chacune couverte
unitairement :

`find_by` · `has_enough_points` · `has_enough_places` · `is_within_twelve_limit` ·
`is_valid_places_input` · `is_competition_in_the_future` · `register_purchase`

Les routes ne contiennent plus que des clauses de garde et le choix de la page à afficher.
`flash()` et `render_template()` restent dans les routes : une fonction qui les appellerait
exigerait un contexte de requête Flask et ne serait plus testable isolément.

## Ratio unitaires / intégration

Les spécifications suggèrent deux fois plus de tests unitaires que de tests d'intégration et
fonctionnels. Le ratio obtenu est de **26 pour 30**.

L'objectif n'est pas atteint, et c'est assumé : la logique métier de l'application, une fois
entièrement extraite, ne représente que sept fonctions. Atteindre 60 tests unitaires aurait
supposé d'en fabriquer sans valeur de vérification. L'écart est documenté plutôt que masqué.

## Ce que la couverture ne prouve pas

La couverture mesure les lignes **exécutées**, pas les comportements **vérifiés**. Deux
observations faites pendant le projet l'illustrent :

- 71 % de couverture ont été atteints avec un test incapable de détecter que la mauvaise page
  était affichée ;
- un test est passé au vert alors que le message d'erreur avait été écrit en dur dans le
  template : le test passait, le bogue était intact.

100 % de couverture signifie donc qu'aucune ligne n'échappe aux tests, pas qu'aucun bogue ne
subsiste.

## Limites connues

- **Dates en dur** dans `competitions.json` : deux compétitions datées de 2030 rendent les
  règles testables ; ces dates finiront par appartenir au passé.
- **Jeux de données calibrés** pour isoler chaque règle (nombre de places ajusté, clubs choisis
  selon leur solde de points).
- **Aucun test de bout en bout réel** : les tests fonctionnels reproduisent les requêtes qu'un
  navigateur enverrait, ils ne cliquent pas. Un formulaire dont les champs cachés seraient vides
  ne serait pas détecté — il faudrait Selenium.
- **Cas de connexion non couverts** : email vide, champ `email` absent de la requête, différence
  de casse. Ils aboutissent au même chemin que l'email inconnu, déjà testé.

## Reproduire les résultats

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
pytest -v
pytest --cov=server --cov-report=term-missing
pytest --cov=server --cov-report=html      # rapport visuel dans htmlcov/index.html
```
