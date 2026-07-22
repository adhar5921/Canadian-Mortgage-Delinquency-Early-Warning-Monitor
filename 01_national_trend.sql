-- National portfolio-level trend, including QoQ and YoY movement.
SELECT
    quarter,
    year,
    quarter_number,
    delinquency_rate_pct,
    ROUND(
        delinquency_rate_pct
        - LAG(delinquency_rate_pct, 1) OVER (ORDER BY quarter_index),
        2
    ) AS quarter_over_quarter_pp,
    ROUND(
        delinquency_rate_pct
        - LAG(delinquency_rate_pct, 4) OVER (ORDER BY quarter_index),
        2
    ) AS year_over_year_pp
FROM mortgage_delinquency
WHERE geography = 'Canada'
ORDER BY quarter_index;
