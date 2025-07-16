import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import describe_data, setup_sidebar_header

# Configuration de la page
st.set_page_config(page_title="Explorer", page_icon="🔍")

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
setup_sidebar_header()

st.markdown("""
<h1>🔍 <span>Explorer les Données</span></h1>
""", unsafe_allow_html=True)

# Vérifier si des données sont chargées
if "data" in st.session_state:
    df = st.session_state["data"]
    
    # Description des données
    with st.expander("📊 Statistiques générales", expanded=True):
        describe_data(df)
        st.dataframe(df.describe())
    
    # Filtres avancés
    st.subheader("🔍 Filtres avancés")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Filtres pour les variables catégorielles
        categorical_cols = df.select_dtypes(include=['object', 'bool']).columns
        
        if len(categorical_cols) > 0:
            st.markdown("**Filtres catégoriels**")
            filters = {}
            
            for col in categorical_cols:
                if col not in ['date']:  # Exclure les colonnes de dates
                    unique_vals = df[col].unique()
                    if len(unique_vals) <= 20:  # Limiter aux colonnes avec peu de valeurs uniques
                        selected_vals = st.multiselect(
                            f"{col.replace('_', ' ').title()}",
                            unique_vals,
                            default=unique_vals,
                            key=f"filter_{col}"
                        )
                        filters[col] = selected_vals
    
    with col2:
        # Filtres pour les variables numériques
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        if len(numeric_cols) > 0:
            st.markdown("**Filtres numériques**")
            numeric_filters = {}
            
            for col in numeric_cols:
                if col not in ['month']:  # Traiter le mois séparément
                    min_val = float(df[col].min())
                    max_val = float(df[col].max())
                    
                    if min_val != max_val:
                        selected_range = st.slider(
                            f"{col.replace('_', ' ').title()}",
                            min_val,
                            max_val,
                            (min_val, max_val),
                            key=f"slider_{col}"
                        )
                        numeric_filters[col] = selected_range
    
    # Filtres spéciaux
    st.markdown("**Filtres spéciaux**")
    col3, col4 = st.columns(2)
    
    with col3:
        # Filtre par période si date disponible
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            min_date = df['date'].min().date()
            max_date = df['date'].max().date()
            
            date_range = st.date_input(
                "Période",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="date_filter"
            )
    
    with col4:
        # Filtre par mois si disponible
        if 'month' in df.columns:
            months = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", 
                     "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]
            selected_months = st.multiselect(
                "Mois",
                range(1, 13),
                default=range(1, 13),
                format_func=lambda x: months[x-1],
                key="month_filter"
            )
    
    # Appliquer les filtres
    filtered_df = df.copy()
    
    # Filtres catégoriels
    if 'filters' in locals():
        for col, values in filters.items():
            if values:
                filtered_df = filtered_df[filtered_df[col].isin(values)]
    
    # Filtres numériques
    if 'numeric_filters' in locals():
        for col, (min_val, max_val) in numeric_filters.items():
            filtered_df = filtered_df[
                (filtered_df[col] >= min_val) & (filtered_df[col] <= max_val)
            ]
    
    # Filtre par date
    if 'date_range' in locals() and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['date'].dt.date >= start_date) & 
            (filtered_df['date'].dt.date <= end_date)
        ]
    
    # Filtre par mois
    if 'selected_months' in locals():
        filtered_df = filtered_df[filtered_df['month'].isin(selected_months)]
    
    # Affichage des résultats
    st.subheader(f"📋 Données filtrées ({len(filtered_df)} lignes)")
    
    if len(filtered_df) > 0:
        # Statistiques du dataset filtré
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Nombre de lignes", len(filtered_df))
        
        with col2:
            if 'total_sales' in filtered_df.columns:
                st.metric("Total des ventes", f"${filtered_df['total_sales'].sum():,.2f}")
        
        with col3:
            if 'customer_satisfaction' in filtered_df.columns:
                st.metric("Satisfaction moyenne", f"{filtered_df['customer_satisfaction'].mean():.1f}/5")
        
        with col4:
            if 'quantity' in filtered_df.columns:
                st.metric("Quantité totale", f"{filtered_df['quantity'].sum():,}")
        
        # Tableau des données
        st.dataframe(filtered_df)
        
        # Option de téléchargement
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les données filtrées (CSV)",
            data=csv,
            file_name='donnees_filtrees.csv',
            mime='text/csv'
        )
    else:
        st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
        
else:
    st.warning("Aucune donnée chargée. Retournez à la page d'accueil.")
