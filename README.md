# AgriSurvey Analytics Pipeline

**End-to-end mixed-methods system for cleaning, analysing, mapping, and reporting agricultural survey data.**

This project demonstrates a complete data workflow used in real agricultural research and NGO settings. It takes raw SurveyCTO data, cleans it, performs quantitative analysis, creates interactive maps, supports qualitative coding (MAXQDA), and automatically generates a professional donor-ready report.

---

## Key Features

- Automated data cleaning and validation of SurveyCTO CSV exports
- Quantitative statistical analysis and publication-quality charts
- Interactive GPS mapping of farmers (Folium)
- Support for qualitative analysis using MAXQDA
- Automatic generation of a detailed Word report written for NGO managers and funders
- Optional automatic email delivery of the final report
- Includes the full farmer questionnaire used for data collection

---

## Tools & Technologies

- **Python**: pandas, numpy, matplotlib, seaborn, folium, python-docx
- **Qualitative Analysis**: MAXQDA
- **Spatial Analysis**: Folium (+ QGIS compatible)
- **Data Collection**: SurveyCTO-compatible questionnaire
- **IDE**: VS Code
- **Version Control**: Git & GitHub

---

## Project Structure

---

## Survey Questionnaire

The complete farmer questionnaire used to collect the data is available in the `docs/` folder:

**[Farmer_Survey_Questionnaire.docx](docs/Farmer_Survey_Questionnaire.docx)**

It covers:
- Farmer and household characteristics
- Farm size, crops, and soil type
- Agricultural practices (fertilizer, irrigation, cooperative membership, extension)
- Production and income
- Open-ended questions on challenges and new practices (later coded in MAXQDA)

---

## How to Run the Pipeline

1. Place your raw SurveyCTO CSV file in the `data/` folder
2. Run the scripts in order:

```bash
python scripts/01_clean_data.py
python scripts/02_quant_analysis.py
python scripts/03_create_map.py
python scripts/04_make_report.py
python scripts/05_send_email.py   # optional