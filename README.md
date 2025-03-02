# Irrigation Nutrition
This repository has the Python and R files used to run regressions and do the analysis for the paper "Evidence of tradeoffs between child diet diversity and water-stressed irrigation expansion in the Global South"

This repository contains scripts used in the Irrigation & Nutrition data analysis and regressions. The scripts process, analyze, and visualize datasets related to irrigation, agricultural sustainability, and nutrition at global and regional scales.

**Repository Structure**
The repository consists of the following scripts:

**1. Global_v6_closest_three_models.rmd**
**Purpose: Runs models to estimate irrigation impacts on nutrition by selecting the three closest irrigation sites for comparison.**
Key Steps:
Reads irrigation and nutrition datasets.
Matches irrigation sites based on spatial proximity.
Estimates effects using statistical models.

**2. Global_v6_FE_diff_in_diff_v1.rmd
Purpose: Implements a fixed-effects difference-in-differences (FE-DID) approach to analyze changes in nutrition outcomes due to irrigation expansion.
**Key Steps:
Reads and preprocesses data.
Applies a FE-DID regression model.
Evaluates the impact of irrigation on food security indicators.

**3. Regional_v6_FE_closest_plots.Rmd
Purpose: Conducts regional-level analysis of irrigation effects using fixed effects models.
**Key Steps:
Filters data for specific regions.
Implements FE regression models at the regional scale.
Produces plots visualizing results.

**4. SPAM2010_HA_sust_unsust_2024Feb.py
Purpose: Processes SPAM 2010 crop harvested area data to compare sustainable vs. unsustainable irrigation.
**Key Steps:
Imports SPAM 2010 crop data.
Merges with DHS dataset to compute fractional harvested area (HA) per country.
Categorizes crops into cash crops and nutritional crops.
Aggregates data at country and sustainability levels.

**5. SPAM2010_sust_unsust_Export_prob.py
**Purpose: Computes export probability for sustainable and unsustainable agricultural production.
Key Steps:
Merges SPAM 2010 harvested area data with FAOSTAT export data.
Calculates export propensity (Export/Production ratio) for each crop.
Aggregates results at the regional and sustainability levels.


Descriptions for each file in the repo IrrigationNutrition/code/

1. code/Global_v6_FE_diff_in_diff_v1.rmd
This code was used to run the regressions of



2. 
