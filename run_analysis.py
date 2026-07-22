"""Run every portfolio SQL query and export recruiter-friendly result tables."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATABASE_FILE = ROOT / "mortgage_risk.db"
QUERY_DIR = ROOT / "sql" / "analysis"
OUTPUT_DIR = ROOT / "outputs" / "tables"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_FILE) as connection:
        for sql_file in sorted(QUERY_DIR.glob("*.sql")):
            query = sql_file.read_text(encoding="utf-8")
            result = pd.read_sql_query(query, connection)
            output_name = sql_file.stem.split("_", maxsplit=1)[1] + ".csv"
            result.to_csv(OUTPUT_DIR / output_name, index=False)
            print(f"{sql_file.name}: {len(result):,} rows -> outputs/tables/{output_name}")


if __name__ == "__main__":
    main()
