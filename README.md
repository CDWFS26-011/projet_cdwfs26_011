# Distance Calculator – Documentation Développeur

## Présentation

Application web Flask de calcul de distance euclidienne entre deux points d'un plan 2D.
Formule : `distance(AB) = sqrt((Bx-Ax)² + (By-Ay)²)` (théorème de Pythagore).

## Architecture

```
projet/
├── app.py                   # Application Flask (routes HTML + API REST)
├── templates/
│   └── index.html           # Interface utilisateur
├── test_app.py              # Suite de tests pytest (19 tests)
├── openapi.yaml             # Documentation API OpenAPI 3.0
├── questions.md             # Réponses au questionnaire d'examen
├── .flake8                  # Configuration analyse statique
├── rapport_flake8_avant.txt # Dette technique initiale (17 violations)
├── rapport_flake8_apres.txt # Dette technique après audit
├── couverture_avant.txt     # Couverture initiale (0%)
├── couverture_apres.txt     # Couverture finale (100%)
└── bruno_collection/        # Collection de tests API Bruno
```

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python 3.12 + Flask |
| Gestion dépendances | uv |
| Tests | pytest + pytest-cov |
| Qualité SAST | flake8 |
| API doc | OpenAPI 3.0 |
| Test API | Bruno |

## Installation

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
git clone <url-repo>
cd projet
uv add flask pytest pytest-cov flake8 requests
```

## Lancement

```bash
uv run flask --app app run
# Accès : http://localhost:5000
```

## Interface utilisateur

1. Ouvrir `http://localhost:5000`
2. Saisir les coordonnées du point A (format : `x,y` — ex : `2,5`)
3. Saisir les coordonnées du point B (format : `x,y` — ex : `1,6`)
4. Cliquer sur **Calculer**
5. Le résultat s'affiche avec l'historique

## Tests

```bash
# Tous les tests avec couverture
uv run pytest test_app.py -v --cov=app --cov-report=term-missing

# Rapport HTML interactif
uv run pytest test_app.py --cov=app --cov-report=html
# Ouvrir htmlcov/index.html dans un navigateur
```

### Résultats

| État initial | Après audit |
|-------------|-------------|
| 0 test | 19 tests |
| 0% couverture | 100% couverture |

## Qualité / SAST (flake8)

```bash
# Analyse statique
uv run flake8 app.py --statistics --count

# Avec config .flake8
uv run flake8 app.py
```

### Violations identifiées dans le code original (17 au total)

| Code | Occurrences | Description |
|------|-------------|-------------|
| E302 | 4 | 2 lignes vides manquantes entre fonctions |
| E501 | 5 | Lignes trop longues (>79 chars) |
| E115 | 2 | Bloc indenté attendu après commentaire |
| E222 | 2 | Espaces multiples après opérateur |
| W291 | 2 | Espaces en fin de ligne |
| W292 | 1 | Pas de newline en fin de fichier |
| W293 | 1 | Ligne vide contenant des espaces |

### Bugs critiques détectés (hors flake8)

- `print(...)` placé après un `return` → dead code, jamais exécuté
- `/api/distance` n'alimente pas l'historique `distances[]`
- Route `/api/distance` accepte GET et PUT (non REST)
- Aucune gestion d'erreur (crash si JSON malformé)

## API REST

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api` | Point d'entrée API |
| POST | `/api/distance` | Calcule une distance |
| GET | `/api/distances` | Liste les calculs effectués |

Voir `openapi.yaml` pour la documentation complète.
Voir `bruno_collection/` pour les requêtes de test.

## Évolutions prévues

- Formule de Haversine pour distances planétaires
- Persistance en base de données
- Authentification API
- Versioning `/api/v1/`