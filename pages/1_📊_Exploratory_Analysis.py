import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Ajout du chemin racine au path pour pouvoir importer utils et config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from utils import load_data

# Configuration de la page
st.set_page_config(page_title="Analyse Exploratoire", page_icon="📊", layout="wide")

# Chargement des styles CSS personnalisés
with open("assets/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Titre de la page
st.title("📊 Analyse Exploratoire des Données")
st.markdown(
    "Explorez vos données de ventes pour découvrir des tendances et des insights."
)


# Chargement et mise en cache des données
@st.cache_data
def get_data():
    return load_data("data/sales_data.parquet")


df = get_data()

# Sidebar pour les filtres
st.sidebar.header("Filtres d'Analyse")

# Filtres pour la période
start_date, end_date = st.sidebar.date_input(
    "Sélectionner une période",
    value=(df["date"].min().date(), df["date"].max().date()),
    key="date_range_explore",
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
    key="categories_explore",
)

# Application des filtres
filtered_df = df[
    (df["date"] >= start_datetime)
    & (df["date"] <= end_datetime)
    & (df["category"].isin(selected_categories))
]

# --------- SECTION 1: VUE D'ENSEMBLE DES DONNÉES ---------
st.header("Vue d'ensemble des données")

# Affichage des métriques clés dans des colonnes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total des Ventes", f"{filtered_df['sales'].sum():,.2f} €")

with col2:
    st.metric("Panier Moyen", f"{filtered_df['sales'].mean():.2f} €")

with col3:
    st.metric("Nombre de Transactions", f"{len(filtered_df):,}")

with col4:
    st.metric("Clients Uniques", f"{filtered_df['customer_id'].nunique():,}")

# Aperçu des données filtrées
with st.expander("Aperçu des données"):
    st.dataframe(filtered_df.head(10), use_container_width=True)


# --------- SECTION 2: ANALYSE DES VENTES PAR CATÉGORIE ---------
st.header("Analyse des ventes par catégorie")

# Calcul des ventes par catégorie
sales_by_category = filtered_df.groupby("category")["sales"].sum().reset_index()
sales_by_category = sales_by_category.sort_values("sales", ascending=False)

# Visualisation des ventes par catégorie avec un graphique en barres
fig1 = px.bar(
    sales_by_category,
    x="category",
    y="sales",
    color="category",
    labels={"sales": "Ventes (€)", "category": "Catégorie"},
    template=config.PLOT_CONFIG["template"],
    color_discrete_sequence=config.PLOT_CONFIG["color_discrete_sequence"],
)

fig1.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=30),
    showlegend=False,
    xaxis_title="",
    yaxis_title="Ventes (€)",
)

st.plotly_chart(fig1, use_container_width=True)


# --------- SECTION 3: ANALYSE TEMPORELLE ---------
st.header("Analyse temporelle")

# Préparation des données temporelles
filtered_df["month_year"] = filtered_df["date"].dt.strftime("%Y-%m")
filtered_df["day_of_week"] = filtered_df["date"].dt.day_name()

# Options d'analyse temporelle
time_options = ["Évolution mensuelle", "Répartition par jour de semaine"]
selected_time_analysis = st.radio(
    "Choisir une analyse temporelle:", time_options, horizontal=True
)

if selected_time_analysis == "Évolution mensuelle":
    # Agrégation par mois
    monthly_sales = (
        filtered_df.groupby("month_year")
        .agg(
            {
                "sales": "sum",
                "date": "min",  # Pour avoir une date à afficher sur l'axe x
            }
        )
        .reset_index()
    )

    monthly_sales = monthly_sales.sort_values("date")

    # Visualisation de l'évolution mensuelle
    fig2 = px.line(
        monthly_sales,
        x="date",
        y="sales",
        markers=True,
        labels={"sales": "Ventes (€)", "date": "Mois"},
        template=config.PLOT_CONFIG["template"],
        color_discrete_sequence=[config.COLORS["primary"]],
    )

    fig2.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=30),
        xaxis_title="",
        yaxis_title="Ventes (€)",
    )

    st.plotly_chart(fig2, use_container_width=True)

else:  # Répartition par jour de semaine
    # Ordre des jours de la semaine
    days_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    # Agrégation par jour de la semaine
    daily_sales = filtered_df.groupby("day_of_week")["sales"].sum().reset_index()
    daily_sales["day_of_week"] = pd.Categorical(
        daily_sales["day_of_week"], categories=days_order
    )
    daily_sales = daily_sales.sort_values("day_of_week")

    # Visualisation des ventes par jour de semaine
    fig3 = px.bar(
        daily_sales,
        x="day_of_week",
        y="sales",
        labels={"sales": "Ventes (€)", "day_of_week": "Jour de la semaine"},
        template=config.PLOT_CONFIG["template"],
        color_discrete_sequence=[config.COLORS["primary"]],
    )

    fig3.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=20, b=30),
        xaxis_title="",
        yaxis_title="Ventes (€)",
    )

    st.plotly_chart(fig3, use_container_width=True)


# --------- SECTION 4: ANALYSE CLIENT SIMPLIFIÉE ---------
st.header("Analyse client")

# Calcul des métriques par client
customer_metrics = (
    filtered_df.groupby("customer_id")
    .agg(
        nb_transactions=("sales", "count"),
        total_spend=("sales", "sum"),
        avg_basket=("sales", "mean"),
    )
    .reset_index()
)

# Distribution des dépenses par client
fig4 = px.histogram(
    customer_metrics,
    x="total_spend",
    nbins=30,
    labels={"total_spend": "Dépenses Totales (€)", "count": "Nombre de Clients"},
    template=config.PLOT_CONFIG["template"],
    color_discrete_sequence=[config.COLORS["primary"]],
)

fig4.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=30),
    xaxis_title="Dépenses Totales (€)",
    yaxis_title="Nombre de Clients",
)

st.plotly_chart(fig4, use_container_width=True)

# Option pour explorer les données clients
if st.checkbox("Explorer les données client détaillées"):
    st.dataframe(
        customer_metrics.sort_values("total_spend", ascending=False),
        column_config={
            "customer_id": st.column_config.NumberColumn("ID Client"),
            "nb_transactions": st.column_config.NumberColumn("Nb Transactions"),
            "total_spend": st.column_config.NumberColumn(
                "Dépenses Totales (€)", format="%.2f €"
            ),
            "avg_basket": st.column_config.NumberColumn(
                "Panier Moyen (€)", format="%.2f €"
            ),
        },
        hide_index=True,
        use_container_width=True,
    )
