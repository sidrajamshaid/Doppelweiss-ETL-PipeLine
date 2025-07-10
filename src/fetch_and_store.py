import imaplib
import email
from email.header import decode_header
import os
import re
import pdfplumber
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

USERNAME = "@gmail.com"
PASSWORD = "-----"
PDF_FOLDER = "pdf_inbox"
OUTPUT_FOLDER = "outputs"
DB_URL = "postgresql+psycopg2://sidra:sidra@localhost/pdf_reports"

os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clean_filename(text):
    return "".join(c for c in text if c.isalnum() or c in (" ", ".", "_", "-")).rstrip()

def fetch_latest_pdf():
    print(" Connecting to Gmail...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(USERNAME, PASSWORD)
    mail.select("inbox")
    status, messages = mail.search(None, 'UNSEEN')
    mail_ids = messages[0].split()
    print(f" Unread emails found: {len(mail_ids)}")
    for num in reversed(mail_ids):
        _, data = mail.fetch(num, "(RFC822)")
        message = email.message_from_bytes(data[0][1])
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition") or "")
            filename = part.get_filename()
            if (content_type == "application/pdf") or ("attachment" in content_disposition.lower()):
                if filename:
                    decoded_name = decode_header(filename)[0][0]
                    if isinstance(decoded_name, bytes):
                        decoded_name = decoded_name.decode("latin1")
                    decoded_name = clean_filename(decoded_name)
                    file_path = os.path.join(PDF_FOLDER, decoded_name)
                    with open(file_path, "wb") as f:
                        f.write(part.get_payload(decode=True))
                    print(f" PDF saved to: {file_path}")
                    mail.logout()
                    return file_path
    mail.logout()
    print(" No unread email with PDF found.")
    return None

def extract_and_store(pdf_path):
    print(f"📄 Using latest saved PDF: {pdf_path}")
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        table_data = page.extract_table()
    header_start = re.search(r'Beginn\s+([\d\.:\s]+)', text)
    header_end = re.search(r'Ende:\s+([\d\.:\s]+)', text)
    kontakter_match = re.search(r'Premium Kontakter:\s*\{(.+?)\}', text)
    berichtsbeginn = header_start.group(1).strip() if header_start else None
    berichtsende = header_end.group(1).strip() if header_end else None
    kontakter_liste = kontakter_match.group(1).strip() if kontakter_match else None
    columns = [
        "Zeitraum", "Premium Kontakter", "Kampagne", "Arbeitszeit", "Anrufe Anzahl",
        "Anr./h", "Kontakte abgeschlossen", "Kontakte abg./h", "Positiv", "Positiv%",
        "Pos./h", "Gesprächzeit", "Gesprächzeit/Arbeitszeit (%)"
    ]
    data_rows = []
    for row in table_data:
        if row and any(str(cell).strip() for cell in row):
            padded = row + [None] * (13 - len(row))
            data_rows.append(padded + [berichtsbeginn, berichtsende, kontakter_liste])
    full_columns = columns + ["Berichtsbeginn", "Berichtsende", "Premium_Kontakter_Liste"]
    df = pd.DataFrame(data_rows, columns=full_columns)
    today_str = datetime.now().strftime("%Y-%m-%d")
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_dir = os.path.join(OUTPUT_FOLDER, today_str)
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, base_name + ".csv")
    xlsx_path = os.path.join(output_dir, base_name + ".xlsx")
    df.to_csv(csv_path, index=False)
    df.to_excel(xlsx_path, index=False)
    print(f" CSV saved to: {csv_path}")
    print(f" Excel saved to: {xlsx_path}")
    try:
        engine = create_engine(DB_URL)
        df.to_sql("pdf_report_data", engine, if_exists="replace", index=False)
        print(" Data inserted into PostgreSQL table successfully.")
    except Exception as e:
        print(" PostgreSQL insert failed:", e)

if __name__ == "__main__":
    pdf_path = fetch_latest_pdf()
    if pdf_path:
        extract_and_store(pdf_path)
    else:
        print(" Workflow stopped due to missing PDF.")