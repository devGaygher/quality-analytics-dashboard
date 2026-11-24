# Quality Analytics | Non-Conformity Management

[Português](README.md)

**Excel · Power Pivot · DAX · Python · ETL · Data Quality**

## Background and contribution

I developed a non-conformity monitoring solution from scratch while working as a quality analyst in the food industry. The business challenge was to turn unstructured operational records into actionable management information. My work included data extraction, cleaning, validation, KPI development, dashboard creation, deviation analysis and process documentation. Python automation was developed with AI assistance and human review of the results.

This portfolio edition preserves the original workbook structure, including its layout, charts, pivot tables, slicers and Power Pivot model. Operational records were replaced with synthetic data, navigation macros were replaced with internal hyperlinks, and the script and documentation were adapted for demonstration.

## Workflow

Simulated Trello export → Python ETL → five-field cleaned dataset → sector and non-conformity classification → Excel source table → Power Pivot / DAX → dashboard.

## Dataset and analysis

529 fictional records from 2025, six fictional stores (L01–L06), six categories, 14 sectors and 23 non-conformity types. All displayed results are illustrative. The dashboard supports occurrence counts, time trends, category and sector comparisons, and recurring product issues. Occurrence counts are not defect rates because production volume is unavailable. The original measure named `Qtd Distinta` uses COUNT(ID), not DISTINCTCOUNT; the results coincide for unique IDs.

## Run locally

Python 3.10+; desktop Excel for Windows with Power Pivot for dashboard exploration and refresh.

```bash
python -m pip install -r requirements.txt
python scripts/processar_nc.py data/raw/trello_export_synthetic.csv data/processed/non_conformities_clean.xlsx
python -m unittest discover -s tests -v
```

The ETL accepts CSV or XLSX, filters the simulated current-month list, parses dates, stores and products, normalizes text and extracts categories. Missing years default to 2025 for this demonstration. Sector and NC classification are separate steps; the fully classified sample is included in `data/processed/dashboard_input.xlsx`. Open `dashboard/quality_dashboard.xlsx` to explore the original adapted dashboard. See the [user guide](docs/user_guide.md).

## Privacy and limitations

Distributed tabular records are synthetic. Structural checks do not certify all contents of the binary Power Pivot model. Desktop validation, confidentiality review and authorization to disclose the solution are required before public release. No unsupported business-impact metrics are claimed.

## Author

Rafael Gaygher — [LinkedIn](https://www.linkedin.com/in/rafael-gaygher/) · [GitHub](https://github.com/devGaygher)
