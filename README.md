# global-industry-analysis
# Global Industry Analysis - Figure Scripts

This repository contains two Python scripts used to generate selected figures for a Global Industry Analysis final report.

## Files

- `references/report_figures.py`  
  Generates World Bank macro charts and the correlation heatmap.

- `references/financial_ratio_scorecard.py`  
  Generates the financial ratio scorecard.

## Output Figures

`report_figures.py` creates:

- `worldbank_gdp_growth_labeled.png`
- `worldbank_household_consumption_labeled.png`
- `worldbank_internet_usage_labeled.png`
- `correlation_heatmap.png`

`financial_ratio_scorecard.py` creates:

- `financial_ratio_scorecard.png`

## Required Data

The scripts require local Excel files:

- `raw_data/tej_financial_data.xlsx` TEJ Balance sheet and income statement items.
- `raw_data/worldbank_data.xlsx` is the World Bank macroeconomic data used for the macro environment analysis.
- `output_merged/final_merged_report.xlsx` Merged dataset combining TEJ financial data and World Bank macroeconomic data.

These data files are not included in this repository.

## Requirements

```bash
pip install pandas matplotlib seaborn openpyxl
