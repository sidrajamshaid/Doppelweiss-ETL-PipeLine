import pandas as pd

def zeit_in_sekunden(zeit_str):
    try:
        h, m, s = map(int, str(zeit_str).split(':'))
        return h * 3600 + m * 60 + s
    except:
        return 0

def sekunden_in_zeit(sekunden):
    if pd.isna(sekunden) or sekunden < 0:
        return "0:00:00"
    h = int(sekunden // 3600)
    m = int((sekunden % 3600) // 60)
    s = int(sekunden % 60)
    return f"{h}:{m:02d}:{s:02d}"

def prepare_gold_layer(silver_df):
    df = silver_df.copy()
    df['Datum'] = pd.to_datetime(df['Datum'], errors='coerce')

    # Clean numeric columns
    num_cols = ["Anr./h", "Kontakte abg./h", "Positiv%", "Pos./h", "Gesprächzeit/Arbeitszeit (%)"]
    for col in num_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .str.replace("%", "", regex=False)
            .replace("nan", "0")
            .astype(float)
        )

    int_cols = ["Anrufe Anzahl", "Kontakte abgeschlossen", "Positiv"]
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Arbeitszeit Tagesdifferenz
    df['Arbeitszeit_sec'] = df['Arbeitszeit'].apply(zeit_in_sekunden)
    df = df.sort_values(['Premium Kontakter', 'Kampagne', 'Datum'])
    df['Arbeitszeit_diff_sec'] = df.groupby(['Premium Kontakter', 'Kampagne'])['Arbeitszeit_sec'].diff()
    df['Arbeitszeit_Vortag'] = df['Arbeitszeit_diff_sec'].apply(sekunden_in_zeit)
    df = df.drop(columns=['Arbeitszeit_sec', 'Arbeitszeit_diff_sec'])

    # Anrufe Anzahl Tagesdifferenz
    df['Anrufe_Vortag'] = df.groupby(['Premium Kontakter', 'Kampagne'])['Anrufe Anzahl'].diff().fillna(0).astype(int)

    # Kontakte abgeschlossen Tagesdifferenz
    df['Kontakte abgeschlossen_Vortag'] = df.groupby(['Premium Kontakter', 'Kampagne'])['Kontakte abgeschlossen'].diff().fillna(0).astype(int)

    # Positiv Tagesdifferenz
    df['Positiv_Vortag'] = df.groupby(['Premium Kontakter', 'Kampagne'])['Positiv'].diff().fillna(0).astype(int)

    # Gesprächzeit Tagesdifferenz
    df['Gesprächzeit_sec'] = df['Gesprächzeit'].apply(zeit_in_sekunden)
    df['Gesprächzeit_diff_sec'] = df.groupby(['Premium Kontakter', 'Kampagne'])['Gesprächzeit_sec'].diff()
    df['Gesprächzeit_Vortag'] = df['Gesprächzeit_diff_sec'].apply(sekunden_in_zeit)
    df = df.drop(columns=['Gesprächzeit_sec', 'Gesprächzeit_diff_sec'])

    # Final type corrections for Power BI
    df['Premium Kontakter'] = df['Premium Kontakter'].astype(str)
    df['Kampagne'] = df['Kampagne'].astype(str)
    df['Arbeitszeit'] = df['Arbeitszeit'].astype(str)
    df['Gesprächzeit'] = df['Gesprächzeit'].astype(str)
    float_cols = ['Anr./h', 'Kontakte abg./h', 'Positiv%', 'Pos./h', 'Gesprächzeit/Arbeitszeit (%)']
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).round(2).astype(float)
    if 'Arbeitszeit_Vortag' in df.columns:
        df['Arbeitszeit_Vortag'] = df['Arbeitszeit_Vortag'].astype(str)
    if 'Anrufe_Vortag' in df.columns:
        df['Anrufe_Vortag'] = pd.to_numeric(df['Anrufe_Vortag'], errors='coerce').fillna(0).astype(int)
    if 'Kontakte abgeschlossen_Vortag' in df.columns:
        df['Kontakte abgeschlossen_Vortag'] = pd.to_numeric(df['Kontakte abgeschlossen_Vortag'], errors='coerce').fillna(0).astype(int)
    if 'Positiv_Vortag' in df.columns:
        df['Positiv_Vortag'] = pd.to_numeric(df['Positiv_Vortag'], errors='coerce').fillna(0).astype(int)
    if 'Gesprächzeit_Vortag' in df.columns:
        df['Gesprächzeit_Vortag'] = df['Gesprächzeit_Vortag'].astype(str)

    return df