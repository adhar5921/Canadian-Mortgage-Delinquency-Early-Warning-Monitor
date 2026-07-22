# Canadian Mortgage Delinquency Early-Warning Monitor

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB)
![SQL](https://img.shields.io/badge/SQL-SQLite-0064A5)
![Data](https://img.shields.io/badge/Data-Public%20Canadian%20Sources-F5B700)
![Status](https://img.shields.io/badge/Status-Complete-2E8B57)

An RBC-inspired public-data analytics project that turns 13+ years of Canadian mortgage delinquency data into a regional monitoring tool. It demonstrates data cleaning, SQL analysis, business framing, quality checks, and executive-ready visualization.

> **Independent portfolio project:** This analysis is not affiliated with, endorsed by, or based on private data from Royal Bank of Canada (RBC). RBC is the business inspiration; all analytical data is public.

## Business question

**Which Canadian provinces and metropolitan areas show the highest current mortgage delinquency risk and the strongest upward momentum, and where should a national bank prioritize early-intervention monitoring and customer support?**

The question is designed for a retail-banking credit-risk or portfolio-analytics team. It separates two signals that can require different responses:

- **Level:** Where is delinquency already elevated?
- **Momentum:** Where is delinquency increasing fastest?

## Executive summary

Using the latest available quarter in the source workbook (**2025 Q4**):

- Canada's mortgage delinquency rate reached **0.24%**, up **0.07 percentage points** from 2023 Q4, but still below the **0.29%** recorded in 2019 Q4.
- **Saskatchewan** had the highest provincial rate at **0.41%**, although it fell 0.05 points over two years. **Ontario** reached **0.27%** and had the largest two-year provincial increase at **+0.14 points**.
- **Regina** had the highest CMA rate at **0.43%**. The strongest two-year increases were in **Barrie (+0.22 points)**, **Toronto (+0.17)**, **Abbotsford–Mission (+0.16)**, and **Oshawa (+0.16)**.
- A bank should treat “high and rising” markets as monitoring priorities, while handling “high but falling” regions separately. Aggregate geography is appropriate for portfolio monitoring—not for individual credit decisions.

## Key visuals

### 1. National trend

![Canadian mortgage delinquency trend](outputs/figures/01_national_trend.png)

The national rate bottomed at 0.14% in 2022 Q3 and has since increased to 0.24%.

### 2. CMA risk and momentum matrix

![CMA risk and momentum matrix](outputs/figures/02_cma_risk_momentum.png)

The matrix prevents a common analytical mistake: treating the highest current rate as the same thing as the fastest deterioration.

### 3. Provincial year-end heatmap

![Provincial mortgage delinquency heatmap](outputs/figures/03_province_heatmap.png)

The heatmap makes Ontario's recent upward shift visible while preserving the difference between current level and direction of change.

## Data sources

| Source | Role in project | Grain / coverage |
|---|---|---|
| [CMHC Mortgage Delinquency Rate](https://www.cmhc-schl.gc.ca/professionals/housing-markets-data-and-research/housing-data/data-tables/mortgage-and-debt/mortgage-delinquency-rate-canada-provinces-cmas) | **Core analytical dataset used in this repository** | Quarterly, Canada + 10 provinces + 34 selected CMAs, 2012 Q3–2025 Q4; underlying source: Equifax Canada |
| [RBC 2025 Annual Report](https://www.rbc.com/investor-relations/_assets-custom/pdf/ar_2025_e.pdf) | Business context only; confirms the relevance of Canadian personal banking, lending, and credit-risk monitoring | Public corporate reporting; no RBC customer-level data used |
| [Bank of Canada Valet API](https://www.bankofcanada.ca/valet/docs) | Documented extension: join policy-rate history to test lagged macro relationships | Daily/monthly monetary and financial series |
| [Statistics Canada Table 14-10-0287-03](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1410028703) | Documented extension: join provincial unemployment to evaluate labour-market stress | Monthly, seasonally adjusted provincial labour-force measures |

CMHC notes that seasonal effects have not been removed and that data from 2019–2022 were revised. Those limitations are preserved in the interpretation.

Use and redistribution of the source data are subject to the [CMHC licence agreement](https://www.cmhc-schl.gc.ca/about-us/terms-conditions/hmip-terms-conditions). Required source notices are recorded in [`DATA_LICENSE.md`](DATA_LICENSE.md).

## Analytical approach

1. **Extract:** Parse the semi-structured CMHC Excel workbook and identify country, province, and CMA rows.
2. **Transform:** Convert the wide workbook into a tidy geography-quarter table with 2,430 rows.
3. **Validate:** Test row counts, geography counts, missing values, duplicate keys, allowed categories, and rate ranges.
4. **Load:** Create an indexed SQLite table using an explicit SQL schema.
5. **Analyze:** Use CTEs, joins, `LAG`, `RANK`, dynamic latest-period logic, and `CASE` segmentation.
6. **Communicate:** Export analysis tables and three decision-focused visualizations.

## SQL questions answered

| SQL file | Business purpose | Skills shown |
|---|---|---|
| `01_national_trend.sql` | How is the national portfolio changing quarter over quarter and year over year? | `LAG`, time ordering, rate-of-change logic |
| `02_latest_cma_rank.sql` | Which CMAs have the highest current delinquency rates? | Dynamic period selection, `RANK`, CTEs |
| `03_cma_risk_momentum.sql` | Which CMAs are high, rising, or both? | Self-join across time, `CASE`, segmentation |
| `04_province_watchlist.sql` | How do current provincial levels compare with one- and two-year momentum? | Multi-period joins, window ranking |
| `05_data_quality.sql` | Is the analytical table complete and unique? | Conditional aggregation, distinct counts |

## Repository structure

```text
rbc-mortgage-risk-analytics/
├── data/
│   ├── raw/                    # Original CMHC workbook
│   └── processed/              # Tidy analysis-ready CSV
├── outputs/
│   ├── figures/                # Three portfolio visualizations
│   └── tables/                 # SQL query results
├── sql/
│   ├── 00_schema.sql
│   └── analysis/               # Five documented SQL analyses
├── src/
│   ├── prepare_data.py
│   ├── run_analysis.py
│   └── make_visuals.py
├── DATA_DICTIONARY.md
├── DATA_LICENSE.md
├── PROJECT_BRIEF.md
├── requirements.txt
└── run_all.py
```

## Run the project

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run_all.py
```

The pipeline recreates the tidy CSV, SQLite database, SQL result tables, and all three figures. It uses only Python packages plus SQLite from the standard library; no database server is required.

## Business recommendations

- Prioritize **Barrie, Toronto, Abbotsford–Mission, and Oshawa** for closer portfolio monitoring because they combine elevated current rates with strong two-year increases.
- Keep **Regina and Saskatchewan** on an exposure watchlist because current rates remain high, even though the recent direction is stable or improving.
- Use aggregate trends to plan renewal support, hardship outreach capacity, and analyst attention; do not use regional rates as a substitute for customer-level affordability or fair-lending assessment.
- Add Bank of Canada policy rates and Statistics Canada unemployment as the next analytical layer, then test multiple lags rather than claiming a causal relationship from same-quarter correlations.

## Limitations

- Delinquency is a lagging indicator and does not identify the cause of financial stress.
- The dataset reports aggregate rates, not borrower-level characteristics, balances, or exposure at default.
- Seasonal effects are not removed.
- CMHC reports revisions to 2019–2022 data; earlier periods were not revised under the same process.
- The monitoring tiers are transparent business rules, not a validated predictive model.
- Differences between regions should guide investigation and support planning, not individual lending decisions.

## Skills demonstrated

`SQL` · `SQLite` · `Python` · `pandas` · `data cleaning` · `data validation` · `window functions` · `CTEs` · `time-series analysis` · `segmentation` · `data visualization` · `business recommendations` · `responsible analytics`

---

Created by **Aanchal Dhar** as a public-data portfolio project for Canadian banking analytics roles.
