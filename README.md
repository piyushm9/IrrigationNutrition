# Irrigation Nutrition
This repository has the Python and R files used to run regressions and do the analysis for the paper "Evidence of tradeoffs between child diet diversity and water-stressed irrigation expansion in the Global South"  

This repository contains scripts used in the Irrigation & Nutrition data analysis and regressions. The scripts process, analyze, and visualize datasets related to irrigation, agricultural sustainability, and nutrition at global and regional scales.  

**Repository Structure**  
The repository consists of the following scripts:  

**1. Global_v6_closest_three_models.rmd**  
**Purpose: Runs Fixed-Effects regressions to estimate the association of irrigation expansion on diet diversity for overall, no water stress and water stress clusters.**  
Key Steps:  
Reads irrigation and nutrition datasets.  
Estimates effects using statistical models.  
Produces plots visualizing results.  

**2. Global_v6_FE_diff_in_diff_v1.rmd**  
**Purpose: Runs Fixed-Effects regressions difference-in-differences (FE-DID) regresssion to estimate the association between irrigation expansion on change in diet diversity.**  
Key Steps:  
Reads and preprocesses data.  
Applies a FE-DID regression model.  
Evaluates the impact of irrigation on food security indicators.  

**3. Regional_v6_FE_closest_plots.Rmd  
Purpose: Runs Fixed-Effects regressions to estimate the association of irrigation expansion on diet diversity for overall, no water stress and water stress clusters for each region.**  
Key Steps:  
Filters data for specific regions.  
Implements FE regression models at the regional scale.  
Produces plots visualizing results.  

**4. SPAM2010_HA_sust_unsust_2024Feb.py  
Purpose: Processes SPAM 2010 crop harvested area data to compare sustainable vs. unsustainable irrigation.**  
Key Steps:  
Imports SPAM 2010 crop data.  
Merges with DHS dataset to compute fractional harvested area (HA) per country.  
Categorizes crops into cash crops and nutritional crops.  
Aggregates data at country and sustainability levels.  

**5. SPAM2010_sust_unsust_Export_prob.py  
Purpose: Computes export probability for sustainable and unsustainable agricultural production.**  
Key Steps:  
Merges SPAM 2010 harvested area data with FAOSTAT export data.  
Calculates export propensity (Export/Production ratio) for each crop.  
Aggregates results at the regional and sustainability levels.

**Global.csv**   
Sample dataset to run the above codes.

---

# **Software Requirements, Installation, and Execution Guide**

This document provides details on the software dependencies, installation instructions, and execution steps for the **Irrigation & Nutrition**. The provided **R and Python scripts** analyze the associations between irrigation expansion and child diet diversity.

## **1. Software Requirements**  
This repository requires the following software and packages:

### **R Environment**  
- **Version:** R **4.2+**  
- **Required R Packages:**  
  - `tidyverse` (for data manipulation and visualization)  
  - `lme4` (for fixed effects models)  
  - `plm` (for panel data analysis)  
  - `stargazer` (for regression output formatting)  
  - `ggplot2` (for visualization)  
  - `readr` (for reading data files)  
  - `dplyr` (for data manipulation)  

### **Python Environment**  
- **Version:** Python **3.8+**  
- **Required Python Libraries:**  
  - `pandas` (for data processing)  
  - `numpy` (for numerical computations)  
  - `openpyxl` (for working with Excel files)  
  - `os` (for file path handling)  

---

## **2. Installation Instructions**

### **Install R and R Packages**  
1. **Download and Install R (if not already installed)**:  
   - [Download R from CRAN](https://cran.r-project.org/)  
2. **Install R dependencies in RStudio**:  
   Open RStudio and run the following command:  
   ```r
   install.packages(c("tidyverse", "lme4", "plm", "stargazer", "ggplot2", "readr", "dplyr"))
   ```

### **Install Python and Required Libraries**  
1. **Install Python** (if not installed):  
   - [Download Python 3.8+](https://www.python.org/downloads/)  
2. **Install dependencies using pip**:  
   Open a terminal or command prompt and run:  
   ```bash
   pip install pandas numpy openpyxl
   ```

---

## **3. Steps to Execute the Code**  

### **R Scripts (`.Rmd` files)**  
1. **Open the R script in RStudio**.  
2. Ensure the dataset files are placed in the correct directory.  
3. Run the script **chunk-by-chunk** or **execute the entire file** using:  
   ```r
   rmarkdown::render("Global_v6_FE_diff_in_diff_v1.rmd")  
   ```
---

### **Python Scripts (`.py` files)**  
1. **Navigate to the script directory**:  
   ```bash
   cd /path/to/IrrigationNutrition
   ```
2. **Run the Python script**:  
   ```bash
   python SPAM2010_HA_sust_unsust_2024Feb.py  
   ```
   or  
   ```bash
   python SPAM2010_sust_unsust_Export_prob.py  
   ```
---

### **Demo Dataset**
To facilitate testing, a **small demo dataset** is included in the repository:
- `global.csv`: Contains a subset of irrigation and nutrition data for demonstration.

To run the analysis on the demo dataset, modify the file paths in the scripts to point to `demo_data.csv`.

---

## **4. Notes**
- Ensure all dependencies are installed before running the scripts.
- If running the **R scripts** in **RStudio**, execute line-by-line for troubleshooting.
- For **Python scripts**, ensure the correct file paths are specified.

