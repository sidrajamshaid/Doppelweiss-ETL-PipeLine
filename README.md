# PoC Report Extractor for [Doppelweiss](https://www.doppelweiss.com/)

> **Automated PDF-to-Analytics Pipeline**
> _Developed for Doppelweiss (Germany)
>

---

## What is This?

**PoC Report Extractor** is a smart, automated pipeline that fetches PDF reports from your email, extracts and cleans the data, and loads it into a database—ready for dashboards in Grafana or Power BI.
No more manual copy-paste, no more errors, just instant insights!

---

##    Key Features

- 📧 **Automated Email Fetching**Securely connects to Gmail and downloads new PDF reports.
- 📄 **PDF Table Extraction**Reads tables and metadata (like report period, contact lists) from PDFs.
- 🧹 **Data Cleaning & Transformation**Standardizes numbers, converts times, and calculates daily changes.
- 💾 **Multi-format Output**Saves as CSV, Excel, and uploads to PostgreSQL for BI tools.
- 🧩 **Modular & Extensible**
  Each step is a separate script—easy to adapt for your needs.

---

## How It Works

**Workflow Overview:**

```
[Unread Email with PDF]
          │
          ▼
 [fetch_and_store.py]
          │
          ▼
[Extract Table & Metadata]
          │
          ▼
[Clean & Transform Data (gold_layer.py)]
          │
          ├──> [Save CSV/Excel]
          │
          └──> [Upload to PostgreSQL]
                          │
                          ▼
                [Grafana / Power BI]
```

---

## Project Structure

```plaintext
src/
├── fetch_and_store.py   # Fetches emails, extracts PDF tables, saves and uploads data
├── gold_layer.py        # Cleans and transforms data for analytics/BI
├── bronze_layer.py      # (Optional) Raw extraction logic
├── silver_layer.py      # (Optional) Intermediate cleaning logic
requirements.txt         # Python dependencies
README.md                # Project documentation
```

---

## Quick Start

1. **Clone the repo & install dependencies**

   ```bash
   git clone https://github.com/your-org/PoC_Report_Extractor.git
   cd PoC_Report_Extractor
   pip install -r requirements.txt
   ```
2. **Configure your credentials**Create a `.env` file (not tracked by git) with:

   ```
   GMAIL_USER=your_email@gmail.com
   GMAIL_PASS=your_app_password
   DB_URL=postgresql+psycopg2://user:password@host/dbname
   ```
3. **Run the pipeline**

   ```bash
   python src/fetch_and_store.py
   ```

   - Downloads the latest unread PDF from Gmail
   - Extracts and cleans the data
   - Saves CSV/Excel in `outputs/`
   - Uploads to PostgreSQL
4. **Connect your BI tool**
   Use Grafana or Power BI to visualize the `pdf_report_data` table in your database.

---

##   Business Value

- **Save Time:** No more manual data entry from PDF reports.
- **Reduce Errors:** Automated, consistent, and reliable data.
- **Ready for BI:** Instantly available for dashboards and analytics.
- **Adaptable:** Modular design for quick changes.

---

## Example Output

| Datum      | Premium Kontakter | Kampagne | Arbeitszeit | Anrufe Anzahl | ... |
| ---------- | ----------------- | -------- | ----------- | ------------- | --- |
| 2024-07-01 | Max Mustermann    | Sommer   | 01:30:00    | 25            | ... |
| 2024-07-02 | Max Mustermann    | Sommer   | 02:00:00    | 30            | ... |

---

## 
    Important Notes for Clients

- **Privacy & Security:**This repository is a demonstration and does **not** contain any real Doppelweiss data, confidential information, or personal credentials.All sensitive details (such as email addresses, passwords, and database access) must be provided by the client and stored securely—never committed to GitHub or shared publicly.
- **Repository Limitations:**Due to privacy and security policies, not all scripts, configurations, or data sources are included in this public repository. Some components may be provided privately or require client-specific setup.
- **Client Customization:**
  The pipeline is designed to be easily adapted for your organization’s needs. Please contact the maintainer for assistance with secure deployment, integration, or customization.

---

## Contact & Support

For questions, support, or customizations, please contact the project maintainer.

---

<details>
<summary>Click to see technical details</summary>

- **Python Version:** 3.8+
- **Dependencies:** pandas, pdfplumber, sqlalchemy, psycopg2-binary, openpyxl, imaplib, email, python-dotenv
- **Database:** PostgreSQL (tested with Grafana and Power BI)
- **Extensible:** Add new report formats or data sources with minimal code changes.

</details>

---

*Developed for Doppelweiss (Germany) as a proof-of-concept for automated report extraction and analytics integration.*

<style>#mermaid-1752134308852{font-family:sans-serif;font-size:16px;fill:#333;}#mermaid-1752134308852 .error-icon{fill:#552222;}#mermaid-1752134308852 .error-text{fill:#552222;stroke:#552222;}#mermaid-1752134308852 .edge-thickness-normal{stroke-width:2px;}#mermaid-1752134308852 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1752134308852 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1752134308852 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1752134308852 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1752134308852 .marker{fill:#333333;}#mermaid-1752134308852 .marker.cross{stroke:#333333;}#mermaid-1752134308852 svg{font-family:sans-serif;font-size:16px;}#mermaid-1752134308852 .label{font-family:sans-serif;color:#333;}#mermaid-1752134308852 .label text{fill:#333;}#mermaid-1752134308852 .node rect,#mermaid-1752134308852 .node circle,#mermaid-1752134308852 .node ellipse,#mermaid-1752134308852 .node polygon,#mermaid-1752134308852 .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-1752134308852 .node .label{text-align:center;}#mermaid-1752134308852 .node.clickable{cursor:pointer;}#mermaid-1752134308852 .arrowheadPath{fill:#333333;}#mermaid-1752134308852 .edgePath .path{stroke:#333333;stroke-width:1.5px;}#mermaid-1752134308852 .flowchart-link{stroke:#333333;fill:none;}#mermaid-1752134308852 .edgeLabel{background-color:#e8e8e8;text-align:center;}#mermaid-1752134308852 .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#mermaid-1752134308852 .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-1752134308852 .cluster text{fill:#333;}#mermaid-1752134308852 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:sans-serif;font-size:12px;background:hsl(80,100%,96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1752134308852:root{--mermaid-font-family:sans-serif;}#mermaid-1752134308852:root{--mermaid-alt-font-family:sans-serif;}#mermaid-1752134308852 flowchart-v2{fill:apa;}</style>
