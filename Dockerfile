# Utiliser l'image officielle Python
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copier tous les fichiers nécessaires pour le build
COPY pyproject.toml uv.lock ./
COPY streamlit_app/ ./streamlit_app/

# Installer les dépendances
RUN uv sync --frozen --no-cache

# Copier le reste du code source
COPY . .

# Exposer le port Streamlit
EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Commande par défaut
CMD ["uv", "run", "streamlit", "run", "streamlit_app/Home.py", "--server.port=8501", "--server.address=0.0.0.0"]