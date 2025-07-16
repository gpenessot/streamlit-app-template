import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

def plot_simple_chart(df):
    """
    Crée une visualisation simple des données avec Plotly
    """
    # Nettoyer le DataFrame pour Plotly
    df = clean_dataframe_for_plotly(df)
    
    # Sélectionner colonnes numériques
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    
    if len(numeric_cols) >= 2:
        # Sélecteurs en haut, partagés
        col1, col2 = st.columns(2)
        with col1:
            x = st.selectbox("Axe X", numeric_cols, index=0)
        with col2:
            y = st.selectbox("Axe Y", numeric_cols, index=min(1, len(numeric_cols)-1))
        
        # Vérifier que x et y sont différents
        if x == y:
            st.warning("⚠️ Veuillez sélectionner des axes différents pour créer un graphique significatif.")
            return
        
        # Graphique en pleine largeur
        st.markdown("**Graphique**")
        
        # Créer le graphique scatter avec Plotly
        fig = px.scatter(
            df, 
            x=x, 
            y=y,
            title=f"{y} vs {x}",
            template="plotly_white"
        )
        
        # Personnaliser le graphique
        fig.update_layout(
            height=500,
            showlegend=False,
            title_font_size=16,
            title_x=0.5
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiques sous le graphique
        st.markdown("**Statistiques**")
        st.dataframe(df[[x, y]].describe())
    else:
        st.warning("Pas assez de colonnes numériques pour créer un graphique")
