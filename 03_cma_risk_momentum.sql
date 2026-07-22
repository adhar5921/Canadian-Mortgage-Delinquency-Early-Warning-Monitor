-- Descriptive monitoring matrix: current level plus two-year change.
-- The tiers support prioritization; they are not a predictive credit-risk model.
WITH latest_period AS (
    SELECT MAX(quarter_index) AS latest_index
    FROM mortgage_delinquency
),
latest AS (
    SELECT geography, quarter, delinquency_rate_pct
    FROM mortgage_delinquency, latest_period
    WHERE geography_type = 'cma'
      AND quarter_index = latest_index
),
two_years_prior AS (
    SELECT geography, delinquency_rate_pct
    FROM mortgage_delinquency, latest_period
    WHERE geography_type = 'cma'
      AND quarter_index = latest_index - 8
),
metrics AS (
    SELECT
        l.geography,
        l.quarter,
        l.delinquency_rate_pct AS latest_rate_pct,
        p.delinquency_rate_pct AS rate_two_years_prior_pct,
        ROUND(l.delinquency_rate_pct - p.delinquency_rate_pct, 2) AS two_year_change_pp
    FROM latest AS l
    JOIN two_years_prior AS p USING (geography)
)
SELECT
    *,
    CASE
        WHEN latest_rate_pct >= 0.25 AND two_year_change_pp >= 0.05 THEN 'High and rising'
        WHEN latest_rate_pct >= 0.25 THEN 'Elevated but stable/falling'
        WHEN two_year_change_pp >= 0.05 THEN 'Lower but rising'
        ELSE 'Lower and stable/falling'
    END AS monitoring_tier
FROM metrics
ORDER BY
    CASE monitoring_tier
        WHEN 'High and rising' THEN 1
        WHEN 'Elevated but stable/falling' THEN 2
        WHEN 'Lower but rising' THEN 3
        ELSE 4
    END,
    two_year_change_pp DESC,
    latest_rate_pct DESC;
