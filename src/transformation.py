
import pandas as pd


def scale_minmax(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(0.0, index=series.index, name=series.name)

    return (series - minimum) / (maximum - minimum)


def scale_zscore(series):
    mean = series.mean()
    std = series.std()

    if pd.isna(std) or std == 0:
        return pd.Series(0.0, index=series.index, name=series.name)

    return (series - mean) / std


def prepare_features(df, products):
    result = df.copy()

    if "categorie" not in result.columns or "cout_achat" not in result.columns:
        result = result.merge(products, on="id_produit", how="left")

    result["montant_net"] = result["montant"] * (
        1 - result["remise_pct"] / 100
    )

    result["panier_moyen_client"] = (
        result.groupby("id_client")["montant_net"].transform("mean")
    )

    result["commande_non_aboutie"] = (
        result["statut"]
        .str.lower()
        .isin(["annulee", "annulée", "echec", "échouée"])
        .astype(int)
    )

    medianes = result.groupby("categorie")["prix_unitaire"].transform("median")
    result["ecart_prix_median"] = result["prix_unitaire"] - medianes

    colonnes_cat = [
        col
        for col in ["canal", "statut", "categorie", "sous_categorie"]
        if col in result.columns
    ]

    result = pd.get_dummies(result, columns=colonnes_cat, dtype=int)
    result["montant"] = scale_zscore(result["montant"])

    return result
