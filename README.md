# GÜDLFT — Plateforme de réservation

Application Flask permettant aux secrétaires de clubs de réserver des places aux compétitions, payées en points. Les données sont stockées dans des fichiers JSON, sans base de données.

Fork de [Python_Testing](https://github.com/OpenClassrooms-Student-Center/Python_Testing),
projet 12 du parcours Développeur d'application Python — OpenClassrooms.

## Prérequis

**Python 3.14**

> Les versions épinglées dans le dépôt d'origine ne fonctionnent plus : Werkzeug 1.0.1
> utilise `ast.Str`, supprimé de Python depuis la 3.12. Les dépendances ont été portées
> vers Flask 3.1.3 **sans aucune modification du code applicatif**.

## Installation

```powershell
git clone https://github.com/Hermes3x/Python_Testing.git
cd Python_Testing
python -m venv env
.\env\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

| Fichier | Contenu |
|---|---|
| `requirements.txt` | Flask et ses dépendances — pour faire tourner l'application |
| `requirements-dev.txt` | pytest, pytest-cov, locust — pour les tests |

`requirements-dev.txt` commence par `-r requirements.txt` : une seule commande installe
l'application **et** l'outillage.

## Lancer l'application

```powershell
python -m flask --app server run
```

→ http://127.0.0.1:5000

| Email | Club | Points |
|---|---|---|
| `john@simplylift.co` | Simply Lift | 13 |
| `admin@irontemple.com` | Iron Temple | 4 |
| `kate@shelifts.co.uk` | She Lifts | 12 |

## Lancer les tests

```powershell
pytest -v
pytest --cov=server --cov-report=term-missing
```

**56 tests · 100 % de couverture**

## Structure et classification des tests

```
tests/
├── unit/                26 tests
├── integration/         27 tests
├── functional/           3 tests
└── performance_tests/   locustfile.py
```

La classification suit la définition du cours OpenClassrooms :

> « Un test faisant appel à une base de données, une API **ou encore une autre méthode** ne sera pas considéré comme un test unitaire. »

| Dossier | Critère |
|---|---|
| `unit/` | appel **direct** d'une fonction, sans Flask ni HTTP |
| `integration/` | **une** requête HTTP — la route collabore avec d'autres fonctions |
| `functional/` | **plusieurs** requêtes enchaînées, un parcours utilisateur complet |

## Tests de performance

Deux terminaux :

```powershell
python -m flask --app server run
```

```powershell
python -m locust -f tests/performance_tests/locustfile.py --host http://127.0.0.1:5000
```

→ tableau de bord sur http://localhost:8089, **6 utilisateurs** (valeur imposée par les specs).

Seuils visés : moins de **5 s** pour afficher la liste des compétitions, moins de **2 s**
pour mettre à jour un total de points.

## Conventions

**Branches** — `<fonctionnalite|bug|amelioration>/nom-descriptif`, sans accent ni underscore.

**Commits** — `type: description`, avec `fix:`, `feat:`, `test:`, `refactor:`, `style:`, `chore:`.
Le suffixe `(closes #N)` relie le commit à son issue GitHub.

La branche `QA` est créée depuis `master` et **n'est jamais fusionnée** : c'est elle qui est
soumise à la relecture.

## Choix et limites assumés

<!-- À COMPLÉTER : une ou deux phrases par point. Dis CE QUE tu as choisi et POURQUOI. -->

- **Persistance** : les données sont chargées depuis les fichiers JSON au démarrage puis modifiées en mémoire ; rien n'est réécrit sur le disque. Redémarrer. Les specs n'exigent pas de persistance, et cette absence garde les tests déterministes. Dans une application réelle, perdre toutes les réservations à chaque redémarrage serait inacceptable.

- **Dates en dur dans `competitions.json`** : deux compétitions à venir (2030) ont été ajoutées pour rendre les règles testables : sans elles, le blocage des compétitions passées interdirait toute réservation. Ces dates finiront par appartenir au passé. Une version plus robuste les calculerait relativement à la date du jour.

- **Absence d'authentification** : l'application ne gère ni mot de passe ni session. L'email saisi identifie un club, il ne l'authentifie pas. Conséquence : toute personne connaissant une URL peut ouvrir une page de réservation, et rien n'empêche de dépenser les points d'un autre club. Les specs n'exigent aucune sécurité ; la faille est  identifiée et laissée hors périmètre, pas ignorée.

- **Ratio tests unitaires / intégration** : 26 tests unitaires pour 30 tests d'intégration et fonctionnels, là où les specs suggèrent deux fois plus d'unitaires. Toute la logique métier a été extraite en six fonctions pures, chacune testée isolément ; atteindre le ratio demandé aurait supposé de fabriquer des tests sans valeur de vérification. L'écart est documenté plutôt que masqué.

## Ressources

- [Flask 3.1](https://flask.palletsprojects.com/en/stable/)
- [pytest](https://docs.pytest.org/)
- [coverage.py](https://coverage.readthedocs.io/)
- [Locust](https://docs.locust.io/)
