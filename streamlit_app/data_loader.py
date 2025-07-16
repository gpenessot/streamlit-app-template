import pandas as pd
import streamlit as st

@st.cache_data
def load_data(file):
    """
    Charge les données depuis différents formats.
    Supporte CSV et Excel.
    """
    file_name = file.name.lower()
    
    try:
        if file_name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file_name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            st.error(f"Format non supporté: {file_name}")
            return None
        
        # Convertir les types problématiques pour Arrow
        for col in df.columns:
            col_type_str = str(df[col].dtype)
            if col_type_str in ['Int64', 'Int32', 'Int16', 'Int8']:
                df[col] = df[col].astype('int64')
            elif col_type_str in ['Float64', 'Float32']:
                df[col] = df[col].astype('float64')
            elif df[col].dtype == 'object':
                try:
                    df[col] = df[col].astype('str')
                except:
                    pass
            
        return df
    except Exception as e:
        st.error(f"Erreur: {e}")
        return None
