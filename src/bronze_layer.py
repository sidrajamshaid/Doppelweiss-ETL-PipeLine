# BRONZE LAYER: Extract raw tables and metadata from PDFs

import pdfplumber
import pandas as pd
import re
import os

pdf_folder = "abc"
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
columns = [
    "Zeitraum", "Premium Kontakter", "Kampagne", "Arbeitszeit", "Anrufe Anzahl",
    "Anr./h", "Kontakte abgeschlossen", "Kontakte abg./h", "Positiv", "Positiv%",
    "Pos./h", "Gesprächzeit", "Gesprächzeit/Arbeitszeit (%)"
]
bronze_dfs = {}

for pdf_file in pdf_files:
    pdf_path = os.path.join(pdf_folder, pdf_file)
    match = re.search(r'(\\d{2}\\.\\d{2}\\.\\d{4})|(\\d{4}-\\d{2}-\\d{2})', pdf_file)
    date_str = match.group(0) if match else None
    if date_str is None:
        print(f"WARNING: No date found in filename: {pdf_file}")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        table = page.extract_table()
        if table is None or len(table) <= 1:
            continue
        # Extract metadata
        start = re.search(r'Beginn\\s+([\\d\\.: ]+)', text)
        end = re.search(r'Ende:\\s+([\\d\\.: ]+)', text)
        kontakter = re.search(r'Premium\\s+Kontakter:\\s*\\{(.*?)\\}', text, re.DOTALL)
        start_val = start.group(1).strip() if start else None
        end_val = end.group(1).strip() if end else None
        kontakter_list = kontakter.group(1).replace('\\n', ' ').strip() if kontakter else None
        # Pad rows and add metadata
        rows = []
        for row in table:
            padded = row + [None] * (len(columns) - len(row))
            rows.append(padded + [start_val, end_val, kontakter_list])
        all_columns = columns + ["Berichtsbeginn", "Berichtsende", "Premium_Kontakter_Liste"]
        df = pd.DataFrame(rows, columns=all_columns)
        if date_str not in bronze_dfs:
            bronze_dfs[date_str] = []
        bronze_dfs[date_str].append(df)