import pandas as pd


def profile_dataframe(df, name='jeu de données', max_cardinality=25):
    print(f'--- {name} ---')
    print(f'Dimensions : {df.shape[0]} lignes, {df.shape[1]} colonnes')
    print(f'Empreinte mémoire : {df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB')

    print(f'Doublons stricts : {df.duplicated().sum()}')

    profile = pd.DataFrame({
        'type': df.dtypes,
        'missing': df.isna().sum(),
        'missing_rate': (df.isna().mean() * 100).round(2),
        'cardinality': df.nunique()
    })

    print('\n--- profil par colonne ---')
    print(profile)

    print('\n--- statistiques descriptives des colonnes numériques ---')
    print(df.describe().round(2))

    print('\n--- répartition des modalités pour les colonnes texte ---')
    for column in df.select_dtypes(include='object').columns:
        cardinality = df[column].nunique()

        if cardinality <= max_cardinality:
            print(f'\n  {column} ({cardinality} modalités) :')
            print(df[column].value_counts(dropna=False))