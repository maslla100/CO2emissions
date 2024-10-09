
# Data Sources for CO2 Emission Prediction Project

This document provides information on the datasets used for the CO2 Emission Prediction Project, including the sources, descriptions, and relevant fields.

## 1. World Bank - World Development Indicators
- **Source**: [World Bank](https://data.worldbank.org/indicator/EN.ATM.CO2E.KT)
- **Description**: This dataset contains global CO2 emissions by country, covering multiple decades. The data is sourced from the World Bank and includes additional indicators such as energy consumption, industrial output, and GDP.
- **Relevant Fields**:
  - `Country Name`
  - `Country Code`
  - `Year-by-Year CO2 Emissions (kt)`
  - `Energy Usage`
  - `GDP`

## 2. Carbon Dioxide Information Analysis Center (CDIAC)
- **Source**: [CDIAC](https://cdiac.ess-dive.lbl.gov/)
- **Description**: The CDIAC dataset provides historical CO2 emissions data from fossil fuel combustion, cement production, and gas flaring, at both country and global levels.
- **Relevant Fields**:
  - `Country Name`
  - `CO2 Emissions (kt)`
  - `Fossil Fuel Consumption`
  - `Cement Production`
  - `Year-by-Year Emissions Data`

## 3. Kaggle - CO2 Emissions Dataset
- **Source**: [Kaggle](https://www.kaggle.com/datasets)
- **Description**: This dataset from Kaggle contains historical global CO2 emissions data with details on contributing factors such as energy production, deforestation rates, and industrial activities.
- **Relevant Fields**:
  - `Country`
  - `CO2 Emissions (kt)`
  - `Energy Consumption`
  - `Deforestation Rates`
  - `Year`

## 4. Global Energy Statistical Yearbook (Enerdata)
- **Source**: [Enerdata](https://yearbook.enerdata.net/)
- **Description**: Provides energy consumption and production statistics by country. It includes data on energy types such as oil, gas, coal, and renewables, along with their contribution to CO2 emissions.
- **Relevant Fields**:
  - `Country`
  - `Energy Type`
  - `CO2 Emissions`
  - `Industrial Production`

## Dataset Structure
Most datasets include the following:
- **Country**: The name or code of the country or region.
- **Year**: The year for which the CO2 emissions data is recorded.
- **CO2 Emissions (kt)**: The total emissions in kilotons (kt).
- **Energy and Economic Factors**: Additional variables related to energy use, industrial activity, and economic growth.

## Data Cleaning and Preprocessing
- Datasets are cleaned by handling missing values, filtering relevant fields, and transforming the data into a usable format for machine learning.
- The cleaned datasets are stored in the `data/cleaned/` folder and are ready for analysis.

For more information on how the datasets were processed, refer to the **data_cleaning.py** script in the `scripts/` folder.


