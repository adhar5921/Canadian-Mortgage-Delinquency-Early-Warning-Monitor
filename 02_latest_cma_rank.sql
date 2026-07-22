-- Rank CMAs at the most recent quarter without hard-coding the date.
WITH latest_period AS (
    SELECT MAX(quarter_index) AS quarter_index
    FROM mortgage_delinquency
),
ranked AS (
    SELECT
        m.geography,
        m.quarter,
        m.delinquency_rate_pct,
        RANK() OVER (ORDER BY m.delinquency_rate_pct DESC) AS delinquency_rank
    FROM mortgage_delinquency AS m
    JOIN latest_period AS p
        ON m.quarter_index = p.quarter_index
    WHERE m.geography_type = 'cma'
)
SELECT *
FROM ranked
ORDER BY delinquency_rank, geography;
