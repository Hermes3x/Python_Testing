# Rapport de performances

Projet 12 — GÜDLFT · mesure de charge avec Locust.

## Outillage et paramètres de la campagne

| Paramètre | Valeur |
|---|---|
| Outil | Locust 2.46.3 |
| Scénario | `tests/performance_tests/locustfile.py` |
| Hôte cible | `http://127.0.0.1:5000` (serveur Flask local) |
| Utilisateurs simultanés | **6** (valeur imposée par les spécifications) |
| Temps d'attente entre deux actions | 1 à 2 secondes, aléatoire |
| Date | 27/08/2026, 08:52 |
| Durée | 57 secondes |
| Requêtes émises | 223 |

Les six utilisateurs simulés sont **six sessions simultanées**, pas six comptes distincts :
ce qui est mesuré est la capacité du serveur à traiter des requêtes concurrentes.

## Résultats par route

| Route | Requêtes | Échecs | Médiane | Moyenne | Maximum |
|---|---|---|---|---|---|
| `POST /showSummary` | 55 | 0 | 5 ms | 4,6 ms | 19 ms |
| `GET /book/<compétition>/<club>` | 58 | 0 | 4 ms | 4,6 ms | 18 ms |
| `POST /purchasePlaces` | 54 | 0 | 4 ms | 4,6 ms | 9 ms |
| `GET /pointsBoard` | 56 | 0 | 4 ms | 4,0 ms | 5 ms |
| **Ensemble** | **223** | **0** | **4 ms** | 4,4 ms | 19 ms |

Percentiles agrégés : p50 = 4 ms · p90 = 5 ms · p95 = 8 ms · p99 = 18 ms.

## Face aux seuils exigés

| Exigence des spécifications | Seuil | Médiane | Pire cas | Verdict |
|---|---|---|---|---|
| Récupérer la liste des compétitions | < 5 000 ms | 5 ms | 19 ms | ✅ 263× sous le seuil au pire |
| Mettre à jour le total de points | < 2 000 ms | 4 ms | 9 ms | ✅ 222× sous le seuil au pire |

Les deux exigences sont satisfaites **y compris sur la requête la plus lente mesurée**. C'est le
maximum, et non la moyenne, qui détermine si un utilisateur a attendu.

Aucune erreur serveur sur 223 requêtes.

## Interprétation

Les percentiles importent davantage que la moyenne : une moyenne rassurante peut masquer des
pics. Ici, p99 = 18 ms signifie que même le centième le plus lent des requêtes reste très
au-dessous des seuils.

L'application ne présente **aucun défaut de performance grossier** : pas de requête bloquante,
pas de dégradation sous six utilisateurs concurrents. Ce résultat est cohérent avec
l'architecture — les données sont chargées une fois en mémoire au démarrage, aucun accès disque
ni base de données n'intervient pendant le traitement d'une requête.

## Limites méthodologiques

Ces chiffres prouvent l'absence de défaut grossier, **pas** la capacité à supporter une charge
réelle. Quatre réserves à retenir :

- **Locust ne compte comme échec que les erreurs HTTP.** Un refus métier — points insuffisants,
  plafond de 12 places atteint — renvoie un `200 OK` avec un message : pour Locust, c'est un
  succès. La justesse du comportement est vérifiée par les 56 tests pytest, pas ici.

- **La mesure du seuil « 2 secondes » est légèrement optimiste.** Simply Lift dispose de 13
  points et le plafond de 12 places s'applique : sur les 54 requêtes d'achat, une douzaine
  seulement ont abouti, les autres ont été refusées. Or le chemin du refus est plus court, il
  sort avant d'écrire dans les données.

- **Le serveur et l'injecteur tournent sur la même machine**, en local. Aucune latence réseau
  n'est prise en compte.

- **Le jeu de données est minuscule** : trois clubs et quatre compétitions dans des fichiers
  JSON. Les temps mesurés ne préjugent en rien du comportement avec plusieurs milliers
  d'enregistrements.

## Reproduire la campagne

Deux terminaux. Redémarrer le serveur avant chaque campagne, afin de repartir des soldes de
points d'origine.

```powershell
python -m flask --app server run
```

```powershell
python -m locust -f tests/performance_tests/locustfile.py --host http://127.0.0.1:5000
```

Puis ouvrir http://localhost:8089, saisir **6 utilisateurs**, et lancer.

Version sans interface, pour une mesure reproductible :

```powershell
python -m locust -f tests/performance_tests/locustfile.py --host http://127.0.0.1:5000 --headless -u 6 -r 6 -t 60s
```
