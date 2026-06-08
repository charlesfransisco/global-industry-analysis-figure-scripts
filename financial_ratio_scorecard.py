from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent.parent
INPUT_PATH = PROJECT_DIR / "output_merged" / "final_merged_report.xlsx"
OUTPUT_DIR = PROJECT_DIR / "references"
COMPANY_ORDER = ["2949", "5321", "6870", "8454"]
COLUMNS = {
    "company": "證券代碼",
    "roe": "ROE_計算",
    "margin": "淨利率_Profit_Margin",
    "turnover": "資產週轉率_Asset_Turnover",
    "multiplier": "權益乘數_Equity_Multiplier",
}


def set_theme():
    plt.rcParams["font.sans-serif"] = [
        "Microsoft JhengHei",
        "Microsoft YaHei",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"


def check_columns(data):
    missing = [column for column in COLUMNS.values() if column not in data.columns]
    if missing:
        raise KeyError(f"Missing columns in final merged report: {', '.join(missing)}")


def load_summary():
    data = pd.read_excel(INPUT_PATH)
    data.columns = data.columns.str.strip()
    check_columns(data)
    metrics = pd.DataFrame(
        {
            "Company": data[COLUMNS["company"]].astype(str),
            "ROE": pd.to_numeric(data[COLUMNS["roe"]], errors="coerce"),
            "Net Profit Margin": pd.to_numeric(data[COLUMNS["margin"]], errors="coerce"),
            "Asset Turnover": pd.to_numeric(data[COLUMNS["turnover"]], errors="coerce"),
            "Equity Multiplier": pd.to_numeric(data[COLUMNS["multiplier"]], errors="coerce"),
        }
    )
    summary = metrics.groupby("Company", sort=True).mean(numeric_only=True)
    summary["Code"] = summary.index.str[:4]
    summary["Sort_Order"] = summary["Code"].map({code: idx for idx, code in enumerate(COMPANY_ORDER)})
    return summary.sort_values("Sort_Order").drop(columns=["Code", "Sort_Order"])


def build_cell_text(summary):
    rows = []
    for company, row in summary.iterrows():
        rows.append(
            [
                company,
                f"{row['ROE'] * 100:.1f}%",
                f"{row['Net Profit Margin'] * 100:.1f}%",
                f"{row['Asset Turnover']:.2f}x",
                f"{row['Equity Multiplier']:.2f}x",
            ]
        )
    return rows


def build_cell_colors(summary):
    best_roe = summary["ROE"].idxmax()
    best_margin = summary["Net Profit Margin"].idxmax()
    best_turnover = summary["Asset Turnover"].idxmax()
    highest_multiplier = summary["Equity Multiplier"].idxmax()

    colors = []
    for company in summary.index:
        base = "#eaf3fb" if company.startswith("2949") else "#f8fafc"
        row = [base, base, base, base, base]
        if company == best_roe:
            row[1] = "#d8f3dc"
        if company == best_margin:
            row[2] = "#d8f3dc"
        if company == best_turnover:
            row[3] = "#dbeafe"
        if company == highest_multiplier:
            row[4] = "#ffedd5"
        colors.append(row)
    return colors


def plot_scorecard(summary):
    set_theme()
    fig = plt.figure(figsize=(14.2, 8.0), dpi=180)
    fig.subplots_adjust(0, 0, 1, 1)

    title_color = "#0f172a"
    navy = "#19384d"
    slate = "#475569"

    fig.text(
        0.055,
        0.92,
        "Financial Ratio Scorecard (2021-2025 Average)",
        fontsize=25,
        weight="bold",
        color=title_color,
    )
    fig.text(
        0.055,
        0.865,
        "DuPont view: ROE = Net Profit Margin x Asset Turnover x Equity Multiplier",
        fontsize=13.5,
        color=slate,
    )
    fig.text(
        0.055,
        0.82,
        "ROE and net profit margin are percentages; asset turnover and equity multiplier are shown as multiples.",
        fontsize=11.5,
        color="#64748b",
    )

    axis = fig.add_axes([0.055, 0.19, 0.89, 0.56])
    axis.axis("off")

    columns = [
        "Company",
        "Avg ROE",
        "Net Profit\nMargin",
        "Asset\nTurnover",
        "Equity\nMultiplier",
    ]
    table = axis.table(
        cellText=build_cell_text(summary),
        cellColours=build_cell_colors(summary),
        colLabels=columns,
        cellLoc="center",
        colLoc="center",
        loc="upper left",
        bbox=[0, 0.02, 1, 0.92],
        colWidths=[0.28, 0.16, 0.20, 0.18, 0.18],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(15)
    table.scale(1, 1.75)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor("#d9e2ec")
        cell.set_linewidth(1.05)
        if row == 0:
            cell.set_facecolor(navy)
            cell.set_text_props(color="white", weight="bold", fontsize=14)
        elif col == 0:
            cell.set_text_props(color=title_color, weight="bold", ha="left")
        else:
            cell.set_text_props(color="#1f2937", fontsize=15)

    fig.text(
        0.055,
        0.105,
        "Source: TEJ company financial data; average calculated from 4 companies, 2021-2025.",
        fontsize=10.8,
        color="#64748b",
    )
    return fig


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = load_summary()
    fig = plot_scorecard(summary)
    output_path = OUTPUT_DIR / "financial_ratio_scorecard.png"
    fig.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"Saved: {output_path}")


if __name__ == "__main__":
    main()
