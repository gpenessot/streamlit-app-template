# streamlit-app-template

Un framework minimaliste mais complet pour développer rapidement des applications data avec Streamlit.

## Structure

- `.streamlit/` - Configuration de Streamlit
- `assets/` - Ressources statiques (CSS, images)
- `data/` - Dossier pour stocker les données
- `models/` - Dossier pour les modèles ML
- `streamlit_app/` - Application Streamlit
  - `Home.py` - Page d'accueil
  - `pages/` - Pages supplémentaires
  - `data_loader.py` - Chargement des données
  - `utils.py` - Fonctions utilitaires
  - `visualizations.py` - Graphiques et visualisations
- `pyproject.toml` - Configuration du projet et dépendances

## Mise en route

### Méthode 1: Développement local avec uv

1. Cloner le dépôt
2. Installer [uv](https://docs.astral.sh/uv/) si ce n'est pas déjà fait
3. Installer les dépendances: `uv sync`
4. Lancer l'application: `uv run streamlit run streamlit_app/Home.py`

### Méthode 2: Avec Docker

1. Cloner le dépôt
2. Lancer avec Docker Compose: `docker-compose up`
3. Accéder à l'application sur http://localhost:8501

### Méthode 3: Développement avec Docker (hot reload)

1. Lancer le service de développement: `docker-compose --profile dev up streamlit-dev`
2. Accéder à l'application sur http://localhost:8502
3. Les modifications de code sont automatiquement rechargées

## Développement

### Qualité du code

- Linting: `uv run ruff check .`
- Formatage: `uv run ruff format .`
- Tests: `uv run pytest`

### CI/CD

Le projet inclut une pipeline GitHub Actions qui:
- Vérifie le code avec ruff
- Exécute les tests
- S'exécute sur chaque push et pull request

### Déploiement

#### HuggingFace Spaces

Le projet est prêt pour le déploiement sur HuggingFace Spaces grâce à la conteneurisation Docker.

#### Docker

- **Build**: `docker build -t streamlit-app .`
- **Run**: `docker run -p 8501:8501 streamlit-app`
- **Compose**: `docker-compose up` (production) ou `docker-compose --profile dev up` (développement)

## Personnalisation

Ce framework est conçu pour être facilement étendu:

- Ajoutez vos propres fonctions dans `streamlit_app/`
- Créez de nouvelles pages dans `streamlit_app/pages/`
- Personnalisez le thème dans `.streamlit/config.toml`
- Modifiez les styles dans `assets/css/style.css`