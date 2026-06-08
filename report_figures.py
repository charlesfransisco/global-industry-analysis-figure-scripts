from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
RAW_DATA_DIR = PROJECT_DIR / "raw_data"
OUTPUT_DIR = SCRIPT_DIR

TEJ_PATH = RAW_DATA_DIR / "tej_financial_data.xlsx"
WORLDBANK_PATH = RAW_DATA_DIR / "worldbank_data.xlsx"

TEJ_COLUMNS = {
    "company": "證券代碼",
    "date": "年月",
    "revenue": "營業收入淨額",
    "assets": "資產總額",
    "equity": "股東權益總額",
    "net_income": "常續性稅後淨利",
}

YEAR_COLUMNS = [
    "2021 [YR2021]",
    "2022 [YR2022]",
    "2023 [YR2023]",
    "2024 [YR2024]",
    "2025 [YR2025]",
]

WORLDBANK_SERIES = {
    "GDP growth (annual %)": "GDP Growth",
    "Households and NPISHs Final consumption expenditure (current US$)": "Household Consumption",
    "Individuals using the Internet (% of population)": "Internet Usage",
}

ANALYSIS_COLUMNS = [
    "ROE",
    "Net Profit Margin",
    "Asset Turnover",
    "Equity Multiplier",
    "GDP Growth",
    "Household Consumption",
    "Internet Usage",
]


def set_chart_theme():
    sns.set_theme(style="whitegrid", context="talk")
    plt.rcParams["font.sans-serif"] = [
        "Microsoft JhengHei",
        "Microsoft YaHei",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["axes.facecolor"] = "#f8fafc"
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.edgecolor"] = "#cbd5e1"
    plt.rcParams["grid.color"] = "#e2e8f0"
    plt.rcParams["axes.titleweight"] = "bold"


def check_columns(data, required_columns, source_name):
    missing = [column for column in required_columns if column not in data.columns]
    if missing:
        raise KeyError(f"{source_name} missing columns: {', '.join(missing)}")


def load_worldbank_data():
    data = pd.read_excel(WORLDBANK_PATH, sheet_name="Data")
    data.columns = data.columns.str.strip()
    check_columns(data, ["Country Name", "Series Name", *YEAR_COLUMNS], "World Bank data")

    data = data[data["Country Name"].eq("East Asia & Pacific")].copy()
    data = data[data["Series Name"].isin(WORLDBANK_SERIES)].copy()

    long_data = data.melt(
        id_vars=["Series Name"],
        value_vars=YEAR_COLUMNS,
        var_name="Year Raw",
        value_name="Value",
    )
    long_data["Year"] = long_data["Year Raw"].str[:4].astype(int)
    long_data["Value"] = pd.to_numeric(long_data["Value"].replace("..", pd.NA), errors="coerce")

    yearly = long_data.pivot(index="Year", columns="Series Name", values="Value").reset_index()
    yearly = yearly.rename(columns=WORLDBANK_SERIES)
    yearly["Household Consumption"] = yearly["Household Consumption"] / 1_000_000_000_000
    return yearly.sort_values("Year")


def load_tej_data():
    data = pd.read_excel(TEJ_PATH)
    data.columns = data.columns.str.strip()
    check_columns(data, TEJ_COLUMNS.values(), "TEJ data")

    data["Year"] = data[TEJ_COLUMNS["date"]].astype(str).str[:4].astype(int)
    data["Net Profit Margin"] = data[TEJ_COLUMNS["net_income"]] / data[TEJ_COLUMNS["revenue"]]
    data["Asset Turnover"] = data[TEJ_COLUMNS["revenue"]] / data[TEJ_COLUMNS["assets"]]
    data["Equity Multiplier"] = data[TEJ_COLUMNS["assets"]] / data[TEJ_COLUMNS["equity"]]
    data["ROE"] = data["Net Profit Margin"] * data["Asset Turnover"] * data["Equity Multiplier"]
    return data


def save_figure(figure, filename):
    output_path = OUTPUT_DIR / filename
    figure.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(figure)
    print(f"Saved: {output_path}")


def format_line_label(column, value):
    if pd.isna(value):
        return ""
    if column == "Household Consumption":
        return f"{value:.1f}"
    if column in {"GDP Growth", "Internet Usage"}:
        return f"{value:.2f}%"
    return f"{value:.2f}"


def annotate_line(axis, data, x_col, y_col, color):
    for _, row in data.iterrows():
        label = format_line_label(y_col, row[y_col])
        if not label:
            continue
        axis.annotate(
            label,
            (row[x_col], row[y_col]),
            textcoords="offset points",
            xytext=(0, 9),
            ha="center",
            fontsize=10,
            fontweight="bold",
            color=color,
            bbox={
                "boxstyle": "round,pad=0.18",
                "facecolor": "white",
                "edgecolor": color,
                "linewidth": 0.8,
                "alpha": 0.92,
            },
        )


def plot_worldbank_line_chart(
    worldbank_data,
    column,
    title,
    subtitle,
    y_label,
    color,
    filename,
    y_limits,
    missing_2025_y=None,
):
    set_chart_theme()
    chart_data = worldbank_data.dropna(subset=[column]).copy()

    figure, axis = plt.subplots(figsize=(8.8, 4.8))
    axis.plot(
        chart_data["Year"],
        chart_data[column],
        marker="o",
        markersize=8,
        linewidth=3.2,
        color=color,
    )
    annotate_line(axis, chart_data, "Year", column, color)

    figure.suptitle(title, x=0.08, y=0.98, ha="left", fontsize=18, fontweight="bold")
    figure.text(0.08, 0.91, subtitle, fontsize=10.5, color="#64748b")
    axis.set_ylabel(y_label, fontsize=12)
    axis.set_xlabel("Year", fontsize=12)
    axis.set_xlim(2020.8, 2025.2)
    axis.set_xticks([2021, 2022, 2023, 2024, 2025])
    axis.set_ylim(*y_limits)
    axis.tick_params(axis="both", labelsize=11)
    axis.grid(axis="y", alpha=0.55)
    axis.grid(axis="x", alpha=0.15)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)

    if missing_2025_y is not None:
        axis.annotate(
            "2025 N/A",
            (2025, missing_2025_y),
            ha="center",
            va="center",
            fontsize=10,
            color="#64748b",
            bbox={"boxstyle": "round,pad=0.25", "facecolor": "#f8fafc", "edgecolor": "#cbd5e1"},
        )

    figure.text(
        0.08,
        0.02,
        "Source: World Bank Data360 / World Development Indicators",
        fontsize=9,
        color="#64748b",
    )
    figure.subplots_adjust(left=0.08, right=0.98, bottom=0.16, top=0.80)
    save_figure(figure, filename)


def plot_gdp_growth(worldbank_data):
    plot_worldbank_line_chart(
        worldbank_data=worldbank_data,
        column="GDP Growth",
        title="GDP Growth: East Asia & Pacific",
        subtitle="World Bank annual GDP growth, 2021-2024",
        y_label="Annual growth (%)",
        color="#dc2626",
        filename="worldbank_gdp_growth_labeled.png",
        y_limits=(2.4, 6.9),
        missing_2025_y=3.0,
    )


def plot_household_consumption(worldbank_data):
    plot_worldbank_line_chart(
        worldbank_data=worldbank_data,
        column="Household Consumption",
        title="Household Consumption: East Asia & Pacific",
        subtitle="Final consumption expenditure, 2021-2024",
        y_label="USD trillion",
        color="#0f766e",
        filename="worldbank_household_consumption_labeled.png",
        y_limits=(13.55, 15.15),
        missing_2025_y=13.75,
    )


def plot_internet_usage(worldbank_data):
    plot_worldbank_line_chart(
        worldbank_data=worldbank_data,
        column="Internet Usage",
        title="Internet Usage: East Asia & Pacific",
        subtitle="Individuals using the Internet, 2021-2025",
        y_label="% of population",
        color="#7c3aed",
        filename="worldbank_internet_usage_labeled.png",
        y_limits=(76.8, 90.0),
    )


def plot_correlation_heatmap(tej_data, worldbank_data):
    set_chart_theme()
    merged_data = tej_data.merge(worldbank_data, on="Year", how="left")
    analysis_data = merged_data[ANALYSIS_COLUMNS].apply(pd.to_numeric, errors="coerce")
    correlation = analysis_data.corr(numeric_only=True)

    figure, axis = plt.subplots(figsize=(12.5, 8.5))
    sns.heatmap(
        correlation,
        ax=axis,
        cmap="RdBu_r",
        vmin=-1,
        vmax=1,
        center=0,
        annot=True,
        fmt=".2f",
        linewidths=0.8,
        linecolor="white",
        square=True,
        cbar_kws={"shrink": 0.82, "label": "Correlation"},
    )
    axis.set_title("Correlation Analysis Heatmap: Exploratory Analysis", loc="left", pad=18, fontweight="bold")
    axis.set_xticklabels(axis.get_xticklabels(), rotation=30, ha="right")
    axis.tick_params(axis="y", rotation=0)
    figure.tight_layout()
    save_figure(figure, "correlation_heatmap.png")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    worldbank_data = load_worldbank_data()
    tej_data = load_tej_data()

    plot_gdp_growth(worldbank_data)
    plot_household_consumption(worldbank_data)
    plot_internet_usage(worldbank_data)
    plot_correlation_heatmap(tej_data, worldbank_data)
    print("Done!")


if __name__ == "__main__":
    main()
