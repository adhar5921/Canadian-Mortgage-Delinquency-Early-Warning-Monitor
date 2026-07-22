# Project Brief

## Project title

Canadian Mortgage Delinquency Early-Warning Monitor

## Stakeholder

A retail-banking portfolio analytics or credit-risk team at a large Canadian bank.

## Business question

Which provinces and metropolitan areas combine high current mortgage delinquency with fast recent deterioration, and where should the bank prioritize monitoring and customer-support capacity?

## Decision supported

The analysis supports quarterly portfolio review, renewal-support planning, geographic drill-down, and prioritization of further investigation. It does not make decisions about individual borrowers.

## Measures

- Latest delinquency rate
- Quarter-over-quarter change
- Year-over-year change
- Two-year change
- Current-rate rank
- Momentum rank
- Descriptive monitoring tier

## Deliverables

- Reproducible data-cleaning pipeline
- Tidy public dataset and SQLite database
- Five documented SQL analyses
- Three executive-ready visualizations
- GitHub-ready README and data dictionary

## Interview summary

“I built an RBC-inspired mortgage portfolio monitor from a public CMHC workbook. I cleaned a wide, semi-structured Excel source into 2,430 tidy geography-quarter records, validated the data, loaded it into SQLite, and used SQL window functions and multi-period joins to distinguish high current delinquency from fast deterioration. The analysis showed that Saskatchewan remained high but was improving, while Ontario—especially Barrie, Toronto, and Oshawa—showed much stronger upward momentum. I translated that into a transparent monitoring matrix and business recommendations, while clearly separating aggregate portfolio analytics from individual lending decisions.”

## Suggested next iteration

Join Bank of Canada policy-rate history and Statistics Canada unemployment rates, test 1–8 quarter lags, and compare whether macro changes improve explanation of regional delinquency momentum. Treat the result as exploratory unless validated out of sample.
