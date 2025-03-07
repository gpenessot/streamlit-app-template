import pandas as pd


def load_data(file_path):
    """Charge et prépare les données pour l'analyse"""
    # Détermine le format en fonction de l'extension
    if file_path.endswith(".parquet"):
        df = pd.read_parquet(file_path)
    else:
        df = pd.read_csv(file_path)

    # Conversion des colonnes de date si nécessaire
    if not pd.api.types.is_datetime64_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"])

    return df


def filter_dataframe(df, start_date=None, end_date=None, categories=None):
    """Filtre le DataFrame selon les critères spécifiés"""
    filtered_df = df.copy()

    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df["date"] >= start_date) & (filtered_df["date"] <= end_date)
        ]

    if categories and len(categories) > 0:
        filtered_df = filtered_df[filtered_df["category"].isin(categories)]

    return filtered_df
