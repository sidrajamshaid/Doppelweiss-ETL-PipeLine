# SILVER LAYER: Clean and merge extracted data

import pandas as pd

def clean_and_merge_bronze_data(bronze_dfs):
    silver_dfs = []
    for date_str, df_list in bronze_dfs.items():
        for df in df_list:
            df = df[df["Zeitraum"] != "Gesamt:"]
            df = df.drop(["Zeitraum", "Berichtsbeginn", "Berichtsende", "Premium_Kontakter_Liste"], axis=1)
            df["Premium Kontakter"] = df["Premium Kontakter"].replace('', pd.NA).ffill()
            df.insert(0, 'Datum', date_str)
            silver_dfs.append(df)

    if silver_dfs:
        silver_df = pd.concat(silver_dfs, ignore_index=True)
        silver_df.columns = silver_dfs[0].columns
    else:
        silver_df = pd.DataFrame()

    return silver_df