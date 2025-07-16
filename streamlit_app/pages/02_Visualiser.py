import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import add_logo

# Configuration de la page
st.set_page_config(page_title="Visualiser", page_icon="📊")

# Chargement des CSS
def load_css():
    import os
    css_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets", "css", "style.css")
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # CSS optionnel

load_css()
add_logo()

def clean_dataframe_for_plotly(df):
    """Nettoie un DataFrame pour qu'il soit compatible avec Plotly"""
    if df is None:
        return None
    
    # Créer une copie pour éviter de modifier l'original
    clean_df = df.copy()
    
    # Convertir les types nullable pandas vers des types standard
    for col in clean_df.columns:
        col_type_str = str(clean_df[col].dtype)
        if col_type_str in ['Int64', 'Int32', 'Int16', 'Int8']:
            clean_df[col] = clean_df[col].astype('int64')
        elif col_type_str in ['Float64', 'Float32']:
            clean_df[col] = clean_df[col].astype('float64')
        elif clean_df[col].dtype == 'object':
            try:
                clean_df[col] = clean_df[col].astype('str')
            except:
                pass
    
    return clean_df

st.markdown("""
<h1>📊 <span>Visualiser les Données</span></h1>
""", unsafe_allow_html=True)

# Vérifier si des données sont chargées
if "data" in st.session_state:
    df = clean_dataframe_for_plotly(st.session_state["data"])
    
    # Options de visualisation simples
    chart_type = st.selectbox(
        "Type de graphique",
        ["Barres", "Ligne", "Dispersion", "Histogramme"]
    )
    
    # Sélection des colonnes
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    
    if len(numeric_cols) > 0:
        y_axis = st.selectbox("Axe Y", numeric_cols)
        
        # Différents types de graphiques avec Plotly
        if chart_type == "Barres":
            if len(df) <= 100:  # Limiter pour la lisibilité
                # Créer un DataFrame avec index explicite pour éviter les conflits
                plot_df = df.reset_index()
                plot_df['row_index'] = plot_df.index
                
                fig = px.bar(
                    plot_df, 
                    x='row_index', 
                    y=y_axis,
                    title=f"Graphique en barres - {y_axis}",
                    template="plotly_white"
                )
                fig.update_layout(height=500, showlegend=False)
                fig.update_xaxes(title="Index")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Trop de données pour un graphique à barres lisible (>100 lignes)")
        
        elif chart_type == "Ligne":
            # Créer un DataFrame avec index explicite pour éviter les conflits
            plot_df = df.reset_index()
            plot_df['row_index'] = plot_df.index
            
            fig = px.line(
                plot_df, 
                x='row_index', 
                y=y_axis,
                title=f"Graphique en ligne - {y_axis}",
                template="plotly_white"
            )
            fig.update_layout(height=500, showlegend=False)
            fig.update_xaxes(title="Index")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Histogramme":
            fig = px.histogram(
                df, 
                x=y_axis,
                title=f"Histogramme - {y_axis}",
                template="plotly_white"
            )
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Dispersion":
            if len(numeric_cols) >= 2:
                # S'assurer que l'axe X est différent de l'axe Y par défaut
                default_x_index = 0 if y_axis != numeric_cols[0] else 1
                x_axis = st.selectbox("Axe X", numeric_cols, index=default_x_index)
                
                # Vérifier que x et y sont différents
                if x_axis == y_axis:
                    st.warning("⚠️ Veuillez sélectionner des axes différents pour créer un graphique significatif.")
                else:
                    fig = px.scatter(
                        df, 
                        x=x_axis, 
                        y=y_axis,
                        title=f"Dispersion - {y_axis} vs {x_axis}",
                        template="plotly_white"
                    )
                    fig.update_layout(height=500, showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Besoin d'au moins 2 colonnes numériques")
    else:
        st.warning("Aucune colonne numérique détectée")
else:
    st.warning("Aucune donnée chargée. Retournez à la page d'accueil.")
