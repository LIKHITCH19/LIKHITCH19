<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img alt="Likhit Vardhan Chiliveri, Business Analyst. Chart of Chipotle's restaurant margin, reported for 2024-2025 and my forecast for 2026-2027." src="assets/header-light.svg" width="100%">
</picture>

I'm a business analyst, and the part of the job I care about most is getting the numbers right. My projects start with a real business question, pull public data from the source (SEC filings, the Census API, BLS), and end with a model or dashboard plus a plain write-up of what I'd actually do about it.

Each card below is one project. The big number is the main result, and every figure on it comes from that repo.

### Selected work

<p>
<a href="https://github.com/LIKHITCH19/chipotle-fpa-forecast"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/chipotle-dark.svg"><img alt="Chipotle FP&A forecast: Q3 2026 margin forecast 23.4% vs actual 23.3%" src="assets/chipotle-light.svg" width="49%"></picture></a>
<a href="https://github.com/LIKHITCH19/furniture-tariff-exposure"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/tariffs-dark.svg"><img alt="Furniture tariff exposure: effective duty rate 5.3% in 2024 to 17.5% in Aug 2026" src="assets/tariffs-light.svg" width="49%"></picture></a>
</p>
<p>
<a href="https://github.com/LIKHITCH19/supply-chain-delivery-analytics"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/supply-chain-dark.svg"><img alt="Supply chain delivery: 24.9% late-delivery rate in Congo DRC" src="assets/supply-chain-light.svg" width="49%"></picture></a>
<a href="https://github.com/LIKHITCH19/swiggy-sales-analytics-dashboard"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/swiggy-dark.svg"><img alt="Swiggy sales dashboard: sales corrected from 46.2M to 53.0M rupees" src="assets/swiggy-light.svg" width="49%"></picture></a>
</p>
<p>
<a href="https://github.com/LIKHITCH19/graduate-admissions-analysis"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/admissions-dark.svg"><img alt="Graduate admissions regression: R-squared 78.1%" src="assets/admissions-light.svg" width="49%"></picture></a>
<a href=".github/workflows/live-tile.yml"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/live-dark.svg"><img alt="Live tile: restaurant menu inflation from BLS" src="assets/live-light.svg" width="49%"></picture></a>
</p>

The last card updates itself. Every Monday a GitHub Action pulls the BLS series for restaurant prices (CPI, food away from home), works out the year-over-year change and redraws the chart ([script](scripts/update_live_tile.py)). I picked it because pricing was the biggest lever in my Chipotle model.

The Chipotle forecast was published on [Tableau Public](https://public.tableau.com/app/profile/likhit.vardhan.chiliveri/viz/ChipotleFPA-2027MarginBudgetandQ32026Forecast/ChipotleFPA) on Oct 16, before the company reported.

### How I work

```mermaid
flowchart LR
    A[Business question] --> B[Public data<br/>from the source]
    B --> C[Clean it and<br/>check it against<br/>reported totals]
    C --> D[SQL and Python<br/>analysis]
    D --> E[Excel model or<br/>Tableau / Power BI<br/>dashboard]
    E --> F[Write-up: findings,<br/>limits, next steps]
```

### Experience

- **Business Analyst Intern (FP&A)**, NOV Inc. &nbsp;·&nbsp; Jul 2026 to now
- **Data Analyst, Transportation Operations**, University of North Texas
- **Business Analyst**, ACKO General Insurance
- **Business Analyst Intern**, Caterpillar

MS in Business Analytics, University of North Texas &nbsp;·&nbsp; BBA, Osmania University
<br>Microsoft Certified: Power BI Data Analyst (PL-300) &nbsp;·&nbsp; Microsoft Excel certification

<sub>The graphics on this page are SVGs drawn by the scripts in this repo, from my own project results.</sub>
