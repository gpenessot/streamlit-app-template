# Streamlit App Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with Streamlit](https://img.shields.io/badge/Made%20with-Streamlit-FF4B4B.svg)](https://streamlit.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Un template moderne et structuré pour créer des applications d'analyse de données et de business intelligence avec Streamlit. Optimisé pour des données au format Parquet et utilisant Plotly pour des visualisations interactives.

## 🌟 Fonctionnalités

- **Structure multi-pages** pour une organisation claire et une navigation intuitive
- **Dashboard interactif** avec KPIs et visualisations dynamiques
- **Tableaux de bord thématiques** (exploration, visualisations avancées, prédictions)
- **Design responsif** optimisé avec des polices modernes (Poppins, Lato)
- **Support pour Parquet** - format optimisé pour l'analyse de données
- **Visualisations interactives** avec Plotly
- **Générateur de données** pour démonstration et tests

## 📂 Structure du projet

```
├── Home.py                # Page d'accueil (fichier principal)
├── config.py              # Configuration globale
├── utils.py               # Fonctions utilitaires
├── .streamlit/
│   └── config.toml        # Configuration Streamlit
├── assets/
│   ├── css/
│   │   └── style.css      # Styles CSS personnalisés
│   └── images/            # Images pour l'application
├── data/
│   └── sales_data.parquet # Données de ventes (générées)
├── models/
│   └── .gitkeep           # Dossier pour les modèles
└── pages/                 # Pages supplémentaires
    ├── 1_📊_Exploratory_Analysis.py
    ├── 2_📈_Advanced_Visualizations.py
    └── 3_🔮_Predictions.py
```

## ⚙️ Installation

### Prérequis

- Python 3.9 ou supérieur
- [uv](https://github.com/astral-sh/uv) (recommandé pour une installation rapide)

### Installation avec uv

```bash
# Cloner le dépôt
git clone https://github.com/yourusername/streamlit-app-template.git
cd streamlit-app-template

# Créer et activer un environnement virtuel avec uv
uv venv
source .venv/bin/activate  # Sur Windows: .venv\Scripts\activate

# Installer les dépendances avec uv
uv pip install -e .
```

## 📊 Utilisation

### Génération des données exemple

Options disponibles :
- `--samples` : Nombre de transactions à générer (défaut: 10000)
- `--start` : Date de début au format YYYY-MM-DD (défaut: 2022-01-01)
- `--end` : Date de fin au format YYYY-MM-DD (défaut: 2023-12-31)
- `--output` : Chemin où enregistrer le fichier (défaut: data/sales_data.csv)
- `--format` : Format de sortie ('csv' ou 'parquet')

### Lancement de l'application

```bash
streamlit run Home.py
```

L'application sera accessible à l'adresse `http://localhost:8501` par défaut.

## 📋 Pages de l'application

1. **Home (Dashboard principal)**
   - Vue d'ensemble des KPIs
   - Évolution des ventes
   - Filtres généraux applicables à toutes les pages

2. **Exploratory Analysis (Analyse exploratoire)**
   - Distribution des ventes par catégorie
   - Analyse temporelle (mensuelle, hebdomadaire)
   - Analyse client simplifiée

3. **Advanced Visualizations (Visualisations avancées)**
   - Carte de chaleur des ventes
   - Visualisations hiérarchiques (Treemap, Sunburst)
   - Analyse comparative entre périodes

4. **Predictions (Prédictions et Projections)**
   - Projections de ventes avec paramètres configurables
   - Simulation de croissance par catégorie
   - Téléchargement des projections au format Parquet

## 🧩 Dépendances principales

- streamlit
- pandas
- plotly
- numpy
- pyarrow (pour la prise en charge de Parquet)

## 💻 Développement

### Outils de développement

Ce projet utilise plusieurs outils pour maintenir la qualité du code :

- **pre-commit** : Vérifications automatiques avant chaque commit
- **ruff** : Linter et formateur pour Python
- **isort** : Tri des imports Python
- **uv** : Gestionnaire de paquets et d'environnements virtuels

### Configuration pre-commit

Les hooks pre-commit suivants sont configurés :

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.9.10
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black]
```

### Installation des hooks pre-commit

```bash
pip install pre-commit
pre-commit install
```

## 🚀 Personnalisation

Pour adapter ce template à vos besoins :

1. Remplacez les données exemple par vos propres données (format Parquet recommandé)
2. Modifiez les colonnes et métriques dans les scripts pour correspondre à vos données
3. Personnalisez les couleurs et le thème dans `.streamlit/config.toml`
4. Adaptez le style visuel dans `assets/css/style.css`

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE).

```
MIT License

Copyright (c) 2025 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
