# Point d'entrée pour HuggingFace Spaces
# Ce fichier redirige vers le fichier principal de l'application
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app/Home.py", "--server.port=7860", "--server.address=0.0.0.0"])