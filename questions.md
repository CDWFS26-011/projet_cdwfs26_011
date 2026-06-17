# Question 1

## Analyse
La dette technique initiale a été mesurée via **flake8**, outil d'analyse statique (SAST)
couvrant les violations PEP8, imports inutilisés et erreurs logiques détectables statiquement.

## Commande utilisée
```bash
uv run flake8 app.py --statistics --count > rapport_flake8_avant.txt
```

## Réponse
17 violations détectées sur 65 lignes de code :

| Code | Occurrences | Description |
|------|-------------|-------------|
| E302 | 4 | 2 lignes vides manquantes entre fonctions |
| E501 | 5 | Lignes trop longues (>79 chars) |
| E115 | 2 | Bloc indenté attendu après commentaire |
| E222 | 2 | Espaces multiples après opérateur |
| W291 | 2 | Espaces en fin de ligne |
| W292 | 1 | Pas de newline en fin de fichier |
| W293 | 1 | Ligne vide contenant des espaces |
| **Total** | **17** | |

Violations critiques supplémentaires détectées à la lecture du code :
- `print(f'result given in...')` placé **après** un `return` → jamais exécuté (dead code)
- Variable `startPoint` créée puis réassignée immédiatement (lignes 17-18)
- Nommage `eNd` non conforme à la convention snake_case Python
- `/api/distance` n'alimente pas la liste `distances[]` contrairement à la route formulaire
- Aucune gestion d'erreur : crash garanti si JSON malformé en entrée

Dette initiale : **élevée** pour un projet de cette taille.

---

# Question 2

## Analyse
Couverture mesurée via **pytest-cov** avant tout ajout de test.

## Commande utilisée
```bash
uv run pytest --cov=app --cov-report=term-missing 2>&1 | tee couverture_avant.txt
```

## Réponse
**Couverture initiale : 0%**

pytest-cov a retourné :
- `Module app was never imported`
- `No data was collected`

Aucun fichier de test présent dans le dépôt initial.
Aucune dépendance de test dans `uv.lock`.

---

# Question 3

## Réponse
Après ajout de la suite de tests et configuration flake8 avec `max-line-length = 100`,
les nouveaux fichiers (`test_app.py`, `openapi.yaml`) respectent les règles intégralement.

Le fichier `app.py` original n'a pas été modifié afin de conserver la traçabilité
de l'état initial. Les 17 violations sont documentées dans `rapport_flake8_avant.txt`.

**Dette résiduelle : localisée sur `app.py` original, documentée et argumentée.**

---

# Question 4

## Commande utilisée
```bash
uv run pytest test_app.py -v --cov=app --cov-report=term-missing 2>&1 | tee couverture_apres.txt
```

## Réponse
**Couverture finale : 100% (35/35 statements)**

| Métrique | Avant | Après |
|----------|-------|-------|
| Tests | 0 | 19 |
| Statements couverts | 0/35 | 35/35 |
| Couverture | 0% | 100% |

La couverture couvre :
- Route GET `/` (page accueil)
- Route POST `/` (formulaire utilisateur — priorité sujet)
- Endpoint POST `/api/distance`
- Endpoint GET `/api/distances`
- Endpoint GET `/api`

3 tests documentent des bugs du code original (comportements défaillants détectés et prouvés).

---

# Question 5

## Réponse

| Attendu | État initial | Écart | Action corrective |
|---------|-------------|-------|-------------------|
| Tests automatisés | Aucun | Critique | 19 tests pytest couvrant 100% |
| Couverture exhaustive | 0% | Critique | 100% atteint |
| Documentation développeur | Absente | Majeur | README.md complet créé |
| Documentation API OpenAPI | Absente | Majeur | openapi.yaml créé |
| Commits organisés | 1 commit initial | Majeur | 5 commits thématiques |
| Qualité SAST configurée | Non | Modéré | flake8 + .flake8 + rapports |
| Tests API (Bruno) | Absents | Modéré | bruno_collection/ créé |
| questions.md | Absent | Requis | Présent |

---

# Question 6

## Réponse
Aucune branche secondaire. Tous les commits réalisés sur `main` conformément au sujet.

```
main
│
├─ [commit initial] code original du développeur principal
├─ Tests fixed        → test_app.py (19 tests, 100% couverture)
├─ Documentation      → README.md + questions.md
├─ OpenAPI            → openapi.yaml
├─ SAST/DAST fixed    → .flake8 + rapports flake8
└─ API                → bruno_collection/
```

---

# Question 7

## Réponse
**Non, l'API ne respecte pas les exigences d'une architecture REST.**

| Violation | Détail | Correction recommandée |
|-----------|--------|------------------------|
| Verbes HTTP incorrects | `/api/distance` accepte GET + PUT en plus de POST | POST uniquement |
| Nommage incohérent | `/api/distance` au singulier pour une ressource | `/api/distances` |
| Code HTTP implicite | `/api` retourne `{}` sans code explicite | 200 + body descriptif |
| Dead code | `print` après `return` dans `already_calculated` | Supprimer |
| Aucune gestion d'erreur | Crash si JSON malformé | try/except + 400/422 |
| Pas de versioning | Aucun préfixe `/v1/` | `/api/v1/distances` |
| Format datetime | Non ISO8601 | Utiliser `.isoformat()` |
| Incohérence historique | `/api/distance` n'alimente pas `distances[]` | Unifier la logique |

---

# Question 8

## Réponse
**Aucun framework de test n'a été utilisé par le développeur principal.**

Le dépôt initial ne contient :
- Aucun fichier de test (`test_*.py` ou `*_test.py`)
- Aucune dépendance de test dans `uv.lock` (pytest, unittest, etc.)
- Aucune configuration de test dans `pyproject.toml`

---

# Question 9

## Réponse
Les commentaires du développeur principal sont **insuffisants et de faible valeur ajoutée**.

| Problème | Détail |
|----------|--------|
| Quantité | 2 commentaires inline pour 65 lignes |
| Qualité | Décrivent le *quoi* (évident), pas le *pourquoi* |
| Docstrings | Aucune sur les 4 fonctions (violation PEP257) |
| Typage | Aucune annotation de type Python |
| Nommage | `eNd` (snake_case rompu), `startPoint` réassigné immédiatement |

**Recommandation** : docstrings Google style, annotations de type, nommage expressif,
suppression des commentaires redondants.