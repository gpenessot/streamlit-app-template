import pandas as pd
import plotly.express as px
import streamlit as st

from utils import load_data

# Configuration de la page
st.set_page_config(
    page_title="Data Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Chargement des styles CSS personnalisés
with open("assets/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Titre principal
st.title("🚀 Data Analytics Dashboard")
st.markdown("### Bienvenue dans votre tableau de bord d'analyse de données")

# Sidebar pour les filtres généraux
st.sidebar.header("Filtres Globaux")
st.sidebar.info("Ces filtres s'appliquent à toutes les pages de l'application.")


# Chargement et mise en cache des données
@st.cache_data
def get_data():
    return load_data("data/sales_data.parquet")


df = get_data()

# Filtres pour la période
start_date, end_date = st.sidebar.date_input(
    "Sélectionner une période",
    value=(df["date"].min().date(), df["date"].max().date()),
    key="date_range_home",
)

# Conversion des dates en datetime pour la compatibilité
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Filtre pour les catégories
all_categories = df["category"].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Sélectionner des catégories",
    options=all_categories,
    default=all_categories,
    key="categories_home",
)

# Application des filtres
filtered_df = df[
    (df["date"] >= start_datetime)
    & (df["date"] <= end_datetime)
    & (df["category"].isin(selected_categories))
]

# Affichage des indicateurs principaux
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = filtered_df["sales"].sum()
    st.metric(
        "Total des Ventes",
        f"{total_sales:,.2f} €",
        delta=f"{total_sales / df['sales'].sum():.1%} du total",
    )

with col2:
    avg_ticket = filtered_df["sales"].mean()
    st.metric("Panier Moyen", f"{avg_ticket:.2f} €")

with col3:
    total_customers = filtered_df["customer_id"].nunique()
    st.metric("Clients Uniques", f"{total_customers:,}")

with col4:
    categories_count = filtered_df["category"].nunique()
    st.metric("Catégories", f"{categories_count}")

# Graphique principal - Évolution des ventes
st.subheader("Évolution des Ventes")
sales_over_time = (
    filtered_df.groupby(filtered_df["date"].dt.to_period("M"))
    .agg({"sales": "sum"})
    .reset_index()
)
sales_over_time["date"] = sales_over_time["date"].dt.to_timestamp()

fig = px.line(
    sales_over_time,
    x="date",
    y="sales",
    title="Ventes Mensuelles",
    labels={"sales": "Ventes (€)", "date": "Mois"},
    template="plotly_white",
)
fig.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=40, b=20),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig, use_container_width=True)

# Aperçu des données
with st.expander("Aperçu des données"):
    st.dataframe(filtered_df.head(50), use_container_width=True)

    # Option pour télécharger les données filtrées
    parquet_buffer = filtered_df.to_parquet(index=False)
    st.download_button(
        label="Télécharger les données filtrées (Parquet)",
        data=parquet_buffer,
        file_name="donnees_filtrees.parquet",
        mime="application/octet-stream",
    )
