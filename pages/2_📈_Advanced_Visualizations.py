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
st.set_page_config(page_title="Visualisations Avancées", page_icon="📈", layout="wide")

# Chargement des styles CSS personnalisés
with open("assets/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Titre de la page
st.title("📈 Visualisations Avancées")
st.markdown(
    "Découvrez d'autres types de visualisations pour analyser vos données de ventes."
)


# Chargement et mise en cache des données
@st.cache_data
def get_data():
    return load_data("data/sales_data.parquet")


df = get_data()

# Sidebar pour les filtres
st.sidebar.header("Filtres de Visualisation")

# Filtres pour la période
start_date, end_date = st.sidebar.date_input(
    "Sélectionner une période",
    value=(df["date"].min().date(), df["date"].max().date()),
    key="date_range_viz",
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
    key="categories_viz",
)

# Application des filtres
filtered_df = df[
    (df["date"] >= start_datetime)
    & (df["date"] <= end_datetime)
    & (df["category"].isin(selected_categories))
]

# Préparation des données temporelles
filtered_df["month"] = filtered_df["date"].dt.month_name()
filtered_df["year"] = filtered_df["date"].dt.year
filtered_df["day_of_week"] = filtered_df["date"].dt.day_name()


# --------- SECTION 1: CARTE DE CHALEUR ---------
st.header("Carte de Chaleur des Ventes")

# Options pour la carte de chaleur
heatmap_options = ["Jour de semaine vs Catégorie", "Mois vs Catégorie"]
selected_heatmap = st.radio(
    "Choisir un type de carte de chaleur:", heatmap_options, horizontal=True
)

if selected_heatmap == "Jour de semaine vs Catégorie":
    # Agrégation par jour de semaine et catégorie
    heatmap_data = (
        filtered_df.groupby(["day_of_week", "category"])["sales"].sum().reset_index()
    )

    # Création du pivot pour la heatmap
    heatmap_pivot = heatmap_data.pivot(
        index="day_of_week", columns="category", values="sales"
    )

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
    heatmap_pivot = heatmap_pivot.reindex(days_order)

    # Création de la heatmap
    fig1 = px.imshow(
        heatmap_pivot.values,
        labels=dict(x="Catégorie", y="Jour de la semaine", color="Ventes (€)"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        color_continuous_scale="Blues",
        aspect="auto",
    )

    fig1.update_layout(height=450, margin=dict(l=20, r=20, t=20, b=30))

    st.plotly_chart(fig1, use_container_width=True)

else:  # Mois vs Catégorie
    # Agrégation par mois et catégorie
    heatmap_data = (
        filtered_df.groupby(["month", "category"])["sales"].sum().reset_index()
    )

    # Création du pivot pour la heatmap
    heatmap_pivot = heatmap_data.pivot(
        index="month", columns="category", values="sales"
    )

    # Ordre des mois
    months_order = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    heatmap_pivot = heatmap_pivot.reindex(months_order)

    # Création de la heatmap
    fig1 = px.imshow(
        heatmap_pivot.values,
        labels=dict(x="Catégorie", y="Mois", color="Ventes (€)"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        color_continuous_scale="Blues",
        aspect="auto",
    )

    fig1.update_layout(height=450, margin=dict(l=20, r=20, t=20, b=30))

    st.plotly_chart(fig1, use_container_width=True)


# --------- SECTION 2: VISUALISATION HIÉRARCHIQUE ---------
st.header("Visualisation Hiérarchique des Ventes")

# Options pour la visualisation hiérarchique
hierarchy_options = ["Treemap", "Sunburst"]
selected_hierarchy = st.radio(
    "Choisir un type de visualisation:", hierarchy_options, horizontal=True
)

# Agrégation des données par catégorie et année-mois
filtered_df["year_month"] = filtered_df["date"].dt.strftime("%Y-%m")
hierarchy_data = (
    filtered_df.groupby(["category", "year_month"])["sales"].sum().reset_index()
)

if selected_hierarchy == "Treemap":
    # Création du treemap
    fig2 = px.treemap(
        hierarchy_data,
        path=["category", "year_month"],
        values="sales",
        color="sales",
        color_continuous_scale="Blues",
        title="Répartition des Ventes par Catégorie et Période",
    )

    fig2.update_layout(height=500, margin=dict(l=20, r=20, t=30, b=30))

    st.plotly_chart(fig2, use_container_width=True)

else:  # Sunburst
    # Création du sunburst
    fig2 = px.sunburst(
        hierarchy_data,
        path=["category", "year_month"],
        values="sales",
        color="sales",
        color_continuous_scale="Blues",
        title="Répartition des Ventes par Catégorie et Période",
    )

    fig2.update_layout(height=500, margin=dict(l=20, r=20, t=30, b=30))

    st.plotly_chart(fig2, use_container_width=True)


# --------- SECTION 3: ANALYSE COMPARATIVE ---------
st.header("Analyse Comparative")

# Sélection de deux périodes à comparer
st.markdown("### Comparaison de deux périodes")

col1, col2 = st.columns(2)

with col1:
    period1_start = st.date_input(
        "Période 1 - Début", value=df["date"].min().date(), key="period1_start"
    )
    period1_end = st.date_input(
        "Période 1 - Fin",
        value=(df["date"].min() + pd.Timedelta(days=90)).date(),
        key="period1_end",
    )

with col2:
    period2_start = st.date_input(
        "Période 2 - Début",
        value=(df["date"].max() - pd.Timedelta(days=90)).date(),
        key="period2_start",
    )
    period2_end = st.date_input(
        "Période 2 - Fin", value=df["date"].max().date(), key="period2_end"
    )

# Conversion en datetime
period1_start_dt = pd.to_datetime(period1_start)
period1_end_dt = pd.to_datetime(period1_end)
period2_start_dt = pd.to_datetime(period2_start)
period2_end_dt = pd.to_datetime(period2_end)

# Filtrer les données pour chaque période
period1_df = df[
    (df["date"] >= period1_start_dt)
    & (df["date"] <= period1_end_dt)
    & (df["category"].isin(selected_categories))
]

period2_df = df[
    (df["date"] >= period2_start_dt)
    & (df["date"] <= period2_end_dt)
    & (df["category"].isin(selected_categories))
]

# Agrégation par catégorie pour chaque période
period1_cat = period1_df.groupby("category")["sales"].sum().reset_index()
period1_cat["period"] = (
    f"Période 1 ({period1_start.strftime('%d/%m/%Y')} - {period1_end.strftime('%d/%m/%Y')})"
)

period2_cat = period2_df.groupby("category")["sales"].sum().reset_index()
period2_cat["period"] = (
    f"Période 2 ({period2_start.strftime('%d/%m/%Y')} - {period2_end.strftime('%d/%m/%Y')})"
)

# Combinaison des données
combined_cat = pd.concat([period1_cat, period2_cat])

# Création du graphique comparatif
fig3 = px.bar(
    combined_cat,
    x="category",
    y="sales",
    color="period",
    barmode="group",
    labels={"sales": "Ventes (€)", "category": "Catégorie", "period": "Période"},
    template=config.PLOT_CONFIG["template"],
    color_discrete_sequence=[config.COLORS["primary"], config.COLORS["secondary"]],
)

fig3.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=30),
    xaxis_title="",
    yaxis_title="Ventes (€)",
)

st.plotly_chart(fig3, use_container_width=True)

# Affichage du pourcentage de variation
if st.checkbox("Afficher le pourcentage de variation"):
    # Calcul des variations
    variation_df = pd.merge(
        period1_cat[["category", "sales"]],
        period2_cat[["category", "sales"]],
        on="category",
        suffixes=("_period1", "_period2"),
    )

    variation_df["variation_absolue"] = (
        variation_df["sales_period2"] - variation_df["sales_period1"]
    )
    variation_df["variation_pourcentage"] = (
        variation_df["variation_absolue"] / variation_df["sales_period1"] * 100
    ).round(2)

    # Mise en forme pour l'affichage
    variation_display = variation_df[
        [
            "category",
            "sales_period1",
            "sales_period2",
            "variation_absolue",
            "variation_pourcentage",
        ]
    ]

    st.dataframe(
        variation_display,
        column_config={
            "category": st.column_config.TextColumn("Catégorie"),
            "sales_period1": st.column_config.NumberColumn(
                "Ventes Période 1 (€)", format="%.2f €"
            ),
            "sales_period2": st.column_config.NumberColumn(
                "Ventes Période 2 (€)", format="%.2f €"
            ),
            "variation_absolue": st.column_config.NumberColumn(
                "Variation Absolue (€)", format="%.2f €"
            ),
            "variation_pourcentage": st.column_config.NumberColumn(
                "Variation (%)", format="%.2f%%"
            ),
        },
        hide_index=True,
        use_container_width=True,
    )
