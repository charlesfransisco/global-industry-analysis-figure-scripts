# Global Industry Analysis - Figure Scripts

This repository contains two Python scripts used to generate selected figures for a Global Industry Analysis final report.

## Files

- `references/report_figures.py`  -> Generates World Bank macro charts and the correlation heatmap.

- `references/financial_ratio_scorecard.py` -> Generates the financial ratio scorecard.

## Output Figures

`report_figures.py` creates:

- `worldbank_gdp_growth_labeled.png`
- `worldbank_household_consumption_labeled.png`
- `worldbank_internet_usage_labeled.png`
- `correlation_heatmap.png`

EX:
<img width="697" height="578" alt="image" src="https://github.com/user-attachments/assets/a58d3ed3-23a3-4847-9338-62003040edf0" />
<img width="2621" height="1451" alt="worldbank_gdp_growth_labeled" src="https://github.com/user-attachments/assets/2f10990b-7100-4064-a064-e5ddea35a2c0" />
<img width="2612" height="1451" alt="worldbank_internet_usage_labeled" src="https://github.com/user-attachments/assets/14aceb0b-30db-45f0-823f-cffd648507e5" />
<img width="2648" height="1451" alt="worldbank_household_consumption_labeled" src="https://github.com/user-attachments/assets/18bdfd74-4b87-4f37-8416-858bf47b93c8" />




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

## License

This repository uses the MIT License for source code only. The license does not apply to TEJ data, World Bank data, course materials, or private datasets.
