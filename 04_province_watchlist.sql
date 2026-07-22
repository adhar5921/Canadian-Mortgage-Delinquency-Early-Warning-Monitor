-- Provincial view separates current exposure from recent momentum.
WITH latest_period AS (
    SELECT MAX(quarter_index) AS latest_index
    FROM mortgage_delinquency
),
latest AS (
    SELECT geography, quarter, delinquency_rate_pct
    FROM mortgage_delinquency, latest_period
    WHERE geography_type = 'province'
      AND quarter_index = latest_index
),
one_year_prior AS (
    SELECT geography, delinquency_rate_pct
    FROM mortgage_delinquency, latest_period
    WHERE geography_type = 'province'
      AND quarter_index = latest_index - 4
),
two_years_prior AS (
    SELECT geography, delinquency_rate_pct
    FROM mortgage_delinquency, latest_period
    WHERE geography_type = 'province'
      AND quarter_index = latest_index - 8
)
SELECT
    l.geography,
    l.quarter,
    l.delinquency_rate_pct AS latest_rate_pct,
    ROUND(l.delinquency_rate_pct - y1.delinquency_rate_pct, 2) AS one_year_change_pp,
    ROUND(l.delinquency_rate_pct - y2.delinquency_rate_pct, 2) AS two_year_change_pp,
    RANK() OVER (ORDER BY l.delinquency_rate_pct DESC) AS current_rate_rank,
    RANK() OVER (
        ORDER BY l.delinquency_rate_pct - y2.delinquency_rate_pct DESC
    ) AS two_year_momentum_rank
FROM latest AS l
JOIN one_year_prior AS y1 USING (geography)
JOIN two_years_prior AS y2 USING (geography)
ORDER BY current_rate_rank;
