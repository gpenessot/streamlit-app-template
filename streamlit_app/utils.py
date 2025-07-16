import streamlit as st
import pandas as pd
import os

def describe_data(df):
    """Affiche des informations de base sur les données"""
    st.write(f"Dimensions: {df.shape[0]} lignes, {df.shape[1]} colonnes")
    
    # Types de données
    st.write("Types de données:")
    st.write(df.dtypes)
    
    # Valeurs manquantes
    missing = df.isna().sum()
    if missing.sum() > 0:
        st.write("Valeurs manquantes:")
        st.write(missing[missing > 0])


def prepare_dataframe_for_display(df):
    """
    Prépare un DataFrame pour l'affichage dans Streamlit en corrigeant
    les problèmes de compatibilité avec Arrow.
    """
    if df is None:
        return None
        
    # Créer une copie pour éviter de modifier l'original
    display_df = df.copy()
    
    # Convertir explicitement les colonnes problématiques
    for col in display_df.columns:
        # Vérifier si le type est Int64, Int32, etc. (nullable integer types)
        col_type_str = str(display_df[col].dtype)
        if col_type_str in ['Int64', 'Int32', 'Int16', 'Int8']:
            # Conversion explicite vers int64 standard
            display_df[col] = display_df[col].astype('int64')
        elif col_type_str in ['Float64', 'Float32']:
            # Conversion explicite vers float64 standard
            display_df[col] = display_df[col].astype('float64')
        
        # Gérer les types object qui pourraient causer des problèmes
        elif display_df[col].dtype == 'object':
            # Essayez de convertir en string si possible
            try:
                display_df[col] = display_df[col].astype('str')
            except:
                pass
    
    return display_df


def setup_sidebar_header():
    """Configure le header de la sidebar avec logo et titre pour toutes les pages"""
    import base64
    
    # Logo et titre dans le background du menu
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images", "logo.png")
    
    if os.path.exists(logo_path):
        # Convertir l'image en base64
        with open(logo_path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        
        st.markdown(
            f"""
            <style>
                [data-testid="stSidebarNav"] {{
                    background-image: url(data:image/png;base64,{encoded});
                    background-repeat: no-repeat;
                    padding-top: 200px;
                    background-position: center 20px;
                    background-size: 150px;
                }}
                [data-testid="stSidebarNav"]::before {{
                    content: "Streamlit App Template";
                    display: block;
                    text-align: center;
                    font-family: var(--font-title);
                    font-weight: 600;
                    color: var(--text-primary);
                    font-size: 1.5rem;
                    margin-top: 10px;
                    margin-bottom: 2px;
                    background: linear-gradient(135deg, #9A6BFF 0%, #F254A4 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
