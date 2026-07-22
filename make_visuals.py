"""Build three polished visualizations from the processed public data."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-rbc-project")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "processed" / "mortgage_delinquency_long.csv"
TABLE_DIR = ROOT / "outputs" / "tables"
FIGURE_DIR = ROOT / "outputs" / "figures"

NAVY = "#0B1F33"
BLUE = "#006AC3"
LIGHT_BLUE = "#DCECF8"
AMBER = "#F5B700"
RED = "#C74634"
GREY = "#6B7C8F"
ATTRIBUTION = (
    "Adapted from Canada Mortgage and Housing Corporation, Mortgage delinquency rate: "
    "Canada, Provinces and CMAs, March 2026. This does not constitute an endorsement "
    "by Canada Mortgage and Housing Corporation of this product."
)


def set_style() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titleweight": "bold",
            "axes.titlesize": 18,
            "axes.labelsize": 11,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "grid.color": "#E6ECF2",
            "grid.linewidth": 0.8,
        }
    )


def save(fig: plt.Figure, filename: str) -> None:
    fig.savefig(FIGURE_DIR / filename, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def national_trend(data: pd.DataFrame) -> None:
    national = data[data["geography"] == "Canada"].copy()
    national["period"] = pd.PeriodIndex(national["quarter"], freq="Q").to_timestamp()
    latest = national.iloc[-1]
    low = national.loc[national["delinquency_rate_pct"].idxmin()]

    fig, ax = plt.subplots(figsize=(11.5, 5.8))
    ax.plot(national["period"], national["delinquency_rate_pct"], color=BLUE, linewidth=3)
    ax.fill_between(
        national["period"],
        national["delinquency_rate_pct"],
        color=LIGHT_BLUE,
        alpha=0.65,
    )
    ax.scatter([low["period"], latest["period"]], [low["delinquency_rate_pct"], latest["delinquency_rate_pct"]], color=[AMBER, RED], s=80, zorder=3)
    ax.annotate(
        f"Series low\n{low['quarter']}: {low['delinquency_rate_pct']:.2f}%",
        (low["period"], low["delinquency_rate_pct"]),
        xytext=(-72, 38),
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "color": GREY},
        color=NAVY,
    )
    ax.annotate(
        f"Latest\n{latest['quarter']}: {latest['delinquency_rate_pct']:.2f}%",
        (latest["period"], latest["delinquency_rate_pct"]),
        xytext=(-70, 42),
        textcoords="offset points",
        arrowprops={"arrowstyle": "-", "color": GREY},
        color=NAVY,
    )
    ax.set_title(
        "Canadian mortgage delinquency is rising from its 2022 low",
        loc="left",
        color=NAVY,
        pad=34,
    )
    ax.text(
        0,
        1.015,
        "Share of mortgages 90+ days past due, quarterly",
        transform=ax.transAxes,
        color=GREY,
    )
    ax.set_ylabel("Delinquency rate (%)")
    ax.set_xlabel("")
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.012, ATTRIBUTION, color=GREY, fontsize=6.4)
    save(fig, "01_national_trend.png")


def cma_risk_momentum() -> None:
    risk = pd.read_csv(TABLE_DIR / "cma_risk_momentum.csv")
    palette = {
        "High and rising": RED,
        "Elevated but stable/falling": AMBER,
        "Lower but rising": BLUE,
        "Lower and stable/falling": "#9DAAB6",
    }

    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    for tier, group in risk.groupby("monitoring_tier", sort=False):
        ax.scatter(
            group["latest_rate_pct"],
            group["two_year_change_pp"],
            s=68,
            alpha=0.86,
            color=palette[tier],
            label=tier,
            edgecolor="white",
            linewidth=0.6,
        )

    ax.axvline(0.25, color=GREY, linewidth=1, linestyle="--")
    ax.axhline(0.05, color=GREY, linewidth=1, linestyle="--")
    label_specs = {
        "Barrie": (8, 6, "Barrie"),
        "Toronto": (8, 6, "Toronto"),
        "Abbotsford-Mission": (8, -18, "Abbotsford–Mission / Oshawa"),
        "Regina": (-48, 8, "Regina"),
    }
    labels = risk[risk["geography"].isin(label_specs)]
    for _, row in labels.iterrows():
        x_offset, y_offset, label = label_specs[row["geography"]]
        ax.annotate(
            label,
            (row["latest_rate_pct"], row["two_year_change_pp"]),
            xytext=(x_offset, y_offset),
            textcoords="offset points",
            fontsize=8,
            color=NAVY,
        )

    ax.set_title(
        "Where current delinquency and two-year momentum intersect",
        loc="left",
        color=NAVY,
        pad=34,
    )
    ax.text(
        0,
        1.015,
        "CMA monitoring matrix, latest quarter versus eight quarters earlier",
        transform=ax.transAxes,
        color=GREY,
    )
    ax.set_xlabel("Latest delinquency rate (%)")
    ax.set_ylabel("Two-year change (percentage points)")
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.text(0.01, 0.024, "Thresholds are descriptive prioritization rules, not a predictive credit-risk model.", color=GREY, fontsize=7.2)
    fig.text(0.01, 0.006, ATTRIBUTION, color=GREY, fontsize=6.0)
    save(fig, "02_cma_risk_momentum.png")


def province_heatmap(data: pd.DataFrame) -> None:
    provinces = data[
        (data["geography_type"] == "province")
        & (data["quarter_number"] == 4)
        & (data["year"] >= 2019)
    ]
    matrix = provinces.pivot(index="geography", columns="year", values="delinquency_rate_pct")
    matrix = matrix.loc[matrix[2025].sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    sns.heatmap(
        matrix,
        cmap=sns.light_palette(BLUE, as_cmap=True),
        annot=True,
        fmt=".2f",
        linewidths=1,
        linecolor="white",
        cbar_kws={"label": "Delinquency rate (%)"},
        ax=ax,
    )
    ax.set_title("Provincial risk levels tell different stories", loc="left", color=NAVY, pad=18)
    ax.text(0, 1.02, "Q4 snapshots, ranked by 2025 Q4 delinquency rate", transform=ax.transAxes, color=GREY)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(axis="y", labelrotation=0)
    fig.text(0.01, 0.026, "Saskatchewan remains highest; Ontario shows the strongest recent upward shift.", color=GREY, fontsize=7.2)
    fig.text(0.01, 0.006, ATTRIBUTION, color=GREY, fontsize=6.0)
    save(fig, "03_province_heatmap.png")


def main() -> None:
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    set_style()
    data = pd.read_csv(DATA_FILE)
    national_trend(data)
    cma_risk_momentum()
    province_heatmap(data)
    print("Created 3 figures in outputs/figures/.")


if __name__ == "__main__":
    main()
