-- Compact audit table used as a pipeline check and portfolio talking point.
SELECT
    geography_type,
    COUNT(*) AS row_count,
    COUNT(DISTINCT geography) AS geography_count,
    COUNT(DISTINCT quarter) AS quarter_count,
    MIN(quarter) AS first_quarter,
    MAX(quarter) AS latest_quarter,
    SUM(CASE WHEN delinquency_rate_pct IS NULL THEN 1 ELSE 0 END) AS missing_rates,
    COUNT(*) - COUNT(DISTINCT geography || '|' || quarter) AS duplicate_keys
FROM mortgage_delinquency
GROUP BY geography_type
ORDER BY
    CASE geography_type
        WHEN 'country' THEN 1
        WHEN 'province' THEN 2
        ELSE 3
    END;
