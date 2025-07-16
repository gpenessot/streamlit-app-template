import streamlit as st
import pandas as pd
import os

# Configuration de la page - DOIT ÊTRE EN PREMIER
st.set_page_config(
    page_title="Streamlit App Template",
    page_icon="📊",
    layout="wide",
)

# Imports après la configuration
from data_loader import load_data
from visualizations import plot_simple_chart
from utils import prepare_dataframe_for_display, add_logo

# Chargement des CSS
def load_css():
    import os
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "css", "style.css")
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # CSS optionnel

load_css()
add_logo()

# Sidebar avec chargement de données pour Home uniquement
with st.sidebar:
    # Chargement de données
    uploaded_file = st.file_uploader("Charger des données", type=["csv", "xlsx"])
    
    if uploaded_file:
        df = load_data(uploaded_file)
        st.session_state["data"] = df
        st.success(f"Données chargées: {df.shape[0]} lignes")
    else:
        # Exemple de données
        if st.button("Charger données d'exemple"):
            import numpy as np
            from datetime import datetime, timedelta
            
            # Créer un dataset de ventes e-commerce réaliste
            np.random.seed(42)
            n_samples = 1000
            
            # Générer des dates sur les 2 dernières années
            start_date = datetime.now() - timedelta(days=730)
            dates = [start_date + timedelta(days=int(i)) for i in np.random.randint(0, 730, n_samples)]
            
            # Catégories de produits
            categories = ["Electronics", "Fashion", "Home", "Sports", "Books", "Beauty", "Toys"]
            category_weights = [0.25, 0.20, 0.15, 0.12, 0.10, 0.10, 0.08]
            
            # Régions
            regions = ["North America", "Europe", "Asia", "South America", "Africa", "Oceania"]
            region_weights = [0.35, 0.25, 0.20, 0.10, 0.06, 0.04]
            
            # Générer les données
            df = pd.DataFrame({
                "date": dates,
                "category": np.random.choice(categories, n_samples, p=category_weights),
                "region": np.random.choice(regions, n_samples, p=region_weights),
                "price": np.random.lognormal(3, 0.8, n_samples).round(2),
                "quantity": np.random.poisson(2, n_samples) + 1,
                "customer_age": np.random.normal(35, 12, n_samples).astype(int).clip(18, 80),
                "discount_rate": np.random.beta(2, 8, n_samples).round(3),
                "shipping_cost": np.random.gamma(2, 5, n_samples).round(2),
                "customer_satisfaction": np.random.normal(4.2, 0.6, n_samples).round(1).clip(1, 5),
                "is_premium": np.random.choice([True, False], n_samples, p=[0.3, 0.7])
            })
            
            # Calculer le total des ventes
            df["total_sales"] = (df["price"] * df["quantity"] * (1 - df["discount_rate"])).round(2)
            
            # Ajouter des variations saisonnières
            df["month"] = pd.to_datetime(df["date"]).dt.month
            df["is_weekend"] = pd.to_datetime(df["date"]).dt.dayofweek >= 5
            
            # Convertir les types
            df = df.astype({
                "category": "str",
                "region": "str", 
                "price": "float64",
                "quantity": "int64",
                "customer_age": "int64",
                "discount_rate": "float64",
                "shipping_cost": "float64",
                "customer_satisfaction": "float64",
                "total_sales": "float64",
                "month": "int64",
                "is_premium": "bool",
                "is_weekend": "bool"
            })
            
            st.session_state["data"] = df
            st.success(f"Données d'exemple chargées! {len(df)} transactions e-commerce")

# Corps principal
st.markdown("""
<h1><span>Bienvenue dans Streamlit App Template</span></h1>
""", unsafe_allow_html=True)

# Vérifier si des données sont chargées
if "data" in st.session_state:
    df = st.session_state["data"]
    
    # Afficher aperçu des données
    st.subheader("Aperçu des données")
    st.dataframe(prepare_dataframe_for_display(df.head()))
    
    # Visualisation simple
    st.subheader("Visualisation simple")
    plot_simple_chart(df)
else:
    st.info("👈 Veuillez charger des données via la barre latérale pour commencer")
