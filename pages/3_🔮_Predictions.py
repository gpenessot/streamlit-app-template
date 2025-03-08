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
st.set_page_config(page_title="Prédictions", page_icon="🔮", layout="wide")

# Chargement des styles CSS personnalisés
with open("assets/css/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Titre de la page
st.title("🔮 Prédictions & Estimations")
st.markdown("Projections simples basées sur vos données historiques.")


# Chargement et mise en cache des données
@st.cache_data
def get_data():
    return load_data("data/sales_data.parquet")


df = get_data()

# Sidebar pour les filtres
st.sidebar.header("Période d'Analyse")

# Filtres pour la période de référence
ref_start_date, ref_end_date = st.sidebar.date_input(
    "Sélectionner une période de référence",
    value=(df["date"].min().date(), df["date"].max().date()),
    key="date_range_pred",
)

# Conversion des dates en datetime pour la compatibilité
ref_start_datetime = pd.to_datetime(ref_start_date)
ref_end_datetime = pd.to_datetime(ref_end_date)

# Filtre pour les catégories
all_categories = df["category"].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Sélectionner des catégories",
    options=all_categories,
    default=all_categories,
    key="categories_pred",
)

# Application des filtres
filtered_df = df[
    (df["date"] >= ref_start_datetime)
    & (df["date"] <= ref_end_datetime)
    & (df["category"].isin(selected_categories))
]


# --------- SECTION 1: PROJECTIONS SIMPLES ---------
st.header("Projections de Ventes")

# Agrégation des données mensuelles
filtered_df["year_month"] = filtered_df["date"].dt.strftime("%Y-%m")
monthly_sales = (
    filtered_df.groupby("year_month")
    .agg(sales=("sales", "sum"), date=("date", "min"))
    .reset_index()
)
monthly_sales = monthly_sales.sort_values("date")

# Affichage des données historiques
fig1 = px.line(
    monthly_sales,
    x="date",
    y="sales",
    markers=True,
    title="Ventes Mensuelles Historiques",
    labels={"sales": "Ventes (€)", "date": "Mois"},
    template=config.PLOT_CONFIG["template"],
    color_discrete_sequence=[config.COLORS["primary"]],
)

fig1.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=50, b=30),
    xaxis_title="",
    yaxis_title="Ventes (€)",
)

st.plotly_chart(fig1, use_container_width=True)

# Paramètres de projection
st.subheader("Paramètres de Projection")

col1, col2 = st.columns(2)

with col1:
    num_months = st.slider(
        "Nombre de mois à projeter",
        min_value=1,
        max_value=12,
        value=6,
        step=1,
        key="num_months",
    )

with col2:
    growth_rate = st.slider(
        "Taux de croissance mensuel (%)",
        min_value=-10.0,
        max_value=10.0,
        value=2.0,
        step=0.5,
        key="growth_rate",
    )

# Génération des projections
if len(monthly_sales) > 0:
    last_date = monthly_sales["date"].iloc[-1]
    last_sales = monthly_sales["sales"].iloc[-1]

    projection_dates = []
    projection_sales = []

    # Calcul des projections avec taux de croissance
    for i in range(1, num_months + 1):
        next_date = last_date + pd.DateOffset(months=i)
        next_sales = last_sales * (1 + growth_rate / 100) ** i

        projection_dates.append(next_date)
        projection_sales.append(next_sales)

    # Création du DataFrame de projection
    projections_df = pd.DataFrame(
        {"date": projection_dates, "sales": projection_sales, "type": "Projection"}
    )

    # Combinaison avec les données historiques
    historical_df = monthly_sales[["date", "sales"]].copy()
    historical_df["type"] = "Historique"

    combined_df = pd.concat([historical_df, projections_df])

    # Affichage des projections
    fig2 = px.line(
        combined_df,
        x="date",
        y="sales",
        color="type",
        markers=True,
        title="Projections de Ventes",
        labels={"sales": "Ventes (€)", "date": "Mois", "type": "Type de données"},
        template=config.PLOT_CONFIG["template"],
        color_discrete_map={
            "Historique": config.COLORS["primary"],
            "Projection": config.COLORS["secondary"],
        },
    )

    fig2.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis_title="",
        yaxis_title="Ventes (€)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Option pour télécharger les projections
    parquet_buffer = projections_df.to_parquet(index=False)
    st.download_button(
        label="Télécharger les projections (Parquet)",
        data=parquet_buffer,
        file_name="projections_ventes.parquet",
        mime="application/octet-stream",
    )


# --------- SECTION 2: PRÉVISIONS PAR CATÉGORIE ---------
st.header("Prévisions par Catégorie")

# Agrégation des données par catégorie
category_sales = filtered_df.groupby("category")["sales"].sum().reset_index()
category_sales = category_sales.sort_values("sales", ascending=False)

# Calculer la part de marché de chaque catégorie
total_sales = category_sales["sales"].sum()
category_sales["market_share"] = (category_sales["sales"] / total_sales * 100).round(2)

# Affichage du tableau des parts de marché
st.dataframe(
    category_sales,
    column_config={
        "category": st.column_config.TextColumn("Catégorie"),
        "sales": st.column_config.NumberColumn("Ventes (€)", format="%.2f €"),
        "market_share": st.column_config.NumberColumn(
            "Part de Marché (%)", format="%.2f%%"
        ),
    },
    hide_index=True,
    use_container_width=True,
)

# Simulation de croissance par catégorie
st.subheader("Simulation de Croissance par Catégorie")

# Sélection des catégories à projeter
categories_to_project = st.multiselect(
    "Sélectionner des catégories à simuler",
    options=category_sales["category"].tolist(),
    default=category_sales["category"].head(3).tolist(),
    key="categories_to_project",
)

if categories_to_project:
    # Taux de croissance par catégorie
    growth_rates = {}
    cols = st.columns(min(3, len(categories_to_project)))

    for i, category in enumerate(categories_to_project):
        with cols[i % 3]:
            growth_rates[category] = st.slider(
                f"Croissance pour {category} (%)",
                min_value=-20.0,
                max_value=50.0,
                value=5.0,
                step=0.5,
                key=f"growth_{category}",
            )

    # Filtrer les catégories sélectionnées
    selected_categories_df = category_sales[
        category_sales["category"].isin(categories_to_project)
    ].copy()

    # Appliquer les taux de croissance pour obtenir les valeurs projetées
    selected_categories_df["projected_sales"] = selected_categories_df.apply(
        lambda x: x["sales"] * (1 + growth_rates[x["category"]] / 100), axis=1
    )

    # Préparer les données pour la visualisation comparative
    comparison_data = []

    for _, row in selected_categories_df.iterrows():
        # Données actuelles
        comparison_data.append(
            {"category": row["category"], "sales": row["sales"], "type": "Actuel"}
        )

        # Données projetées
        comparison_data.append(
            {
                "category": row["category"],
                "sales": row["projected_sales"],
                "type": "Projeté",
            }
        )

    comparison_df = pd.DataFrame(comparison_data)

    # Création du graphique comparatif
    fig3 = px.bar(
        comparison_df,
        x="category",
        y="sales",
        color="type",
        barmode="group",
        title="Comparaison des Ventes Actuelles et Projetées par Catégorie",
        labels={
            "sales": "Ventes (€)",
            "category": "Catégorie",
            "type": "Type de données",
        },
        template=config.PLOT_CONFIG["template"],
        color_discrete_map={
            "Actuel": config.COLORS["primary"],
            "Projeté": config.COLORS["secondary"],
        },
    )

    fig3.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=30),
        xaxis_title="",
        yaxis_title="Ventes (€)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    st.plotly_chart(fig3, use_container_width=True)

    # Tableau récapitulatif
    comparison_summary = selected_categories_df[
        ["category", "sales", "projected_sales"]
    ].copy()
    comparison_summary["variation"] = (
        comparison_summary["projected_sales"] - comparison_summary["sales"]
    ).round(2)
    comparison_summary["variation_percent"] = (
        (comparison_summary["projected_sales"] / comparison_summary["sales"] - 1) * 100
    ).round(2)

    st.dataframe(
        comparison_summary,
        column_config={
            "category": st.column_config.TextColumn("Catégorie"),
            "sales": st.column_config.NumberColumn(
                "Ventes Actuelles (€)", format="%.2f €"
            ),
            "projected_sales": st.column_config.NumberColumn(
                "Ventes Projetées (€)", format="%.2f €"
            ),
            "variation": st.column_config.NumberColumn(
                "Variation (€)", format="%.2f €"
            ),
            "variation_percent": st.column_config.NumberColumn(
                "Variation (%)", format="%.2f%%"
            ),
        },
        hide_index=True,
        use_container_width=True,
    )
