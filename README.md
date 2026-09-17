# KCompany-Analysis

## 📌 Project Overview (نظرة عامة على المشروع)
This project is an End-to-End Data Analytics pipeline focused on analyzing the KCompany House Sales dataset. The primary goal is to identify the key drivers of house prices and understand how these drivers differ between Middle-Class and Luxury real estate markets. The project integrates **Python** for Data ETL and Statistical Modeling, and **Power BI** for interactive visualization.

## 🎯 Business Problem (المشكلة التجارية)
Real estate investors often apply the same evaluation criteria to all properties. However, this analysis tests the hypothesis that the factors maximizing value for an average home (e.g., square footage, number of rooms) differ significantly from those driving premium prices in the luxury market (e.g., architectural grade, waterfront views).

## 🛠️ Tools & Technologies (الأدوات المستخدمة)
* **Python (Pandas, NumPy):** Data Cleaning, Feature Engineering.
* **Python (Statsmodels):** OLS Regression, Statistical Modeling.
* **Power BI:** Interactive Dashboards, Data Visualization.

## ⚙️ Methodology & Workflow (منهجية العمل)

### 1. Data Cleaning & Preprocessing (تنظيف البيانات)
* Removed duplicate property listings based on `id`, `lat`, and `long` coordinates to avoid skewed results[cite: 3].
* Handled outliers by filtering out logically invalid entries (e.g., properties with 0 bedrooms or properties with extreme counts like 33 bedrooms in small areas, restricting to 0 < bedrooms < 10).

### 2. Feature Engineering & Segmentation (هندسة الميزات والتصنيف)
* Market Segmentation: Divided the dataset using the 75th percentile (`quantile(0.75)`) of prices. Houses below this threshold were classified as **'Middle Class'**, while those above were classified as **'Luxury Class'**.
* Created a binary target variable `is_luxury` to facilitate interaction models.
* Applied Natural Log Transformation (`np.log()`) to the price column to handle skewness and normalize the data distribution for accurate regression modeling.

### 3. Statistical Analysis (التحليل الإحصائي)
* Conducted OLS Regression with robust standard errors (`cov_type='HC3'`) to compare feature value drivers by class[cite: 5].
* Built a Unified Interaction Model evaluating baseline traits (`bedrooms`, `bathrooms`, `sqft_living`, `view`, `grade`, `condition`, `yr_built`) against the `is_luxury` segment.

### 4. Data Visualization (رسوم البيانات - Power BI)
* Created a comprehensive Executive Dashboard displaying overall market KPIs.
* **Key Metrics Analyzed:** 
  * Total Houses Sold: 21.436K
  * Average House Price: $540.53K
  * Average Price per Sqft: $263.97
* Visualized the market segment distribution using Donut Charts (Middle Class: 75.09%, Luxury Class: 24.91%).
* Designed a Clustered Bar Chart translating the 'Coefficient Comparison Matrix' into a visual format to compare the impact of baseline drivers between the two market classes.

## 💡 Key Insights & Recommendations (أهم النتائج والتوصيات)
1. **Architectural Grade Impact:** The architectural and structural `grade` has a exponentially higher impact on the pricing of Luxury houses compared to Middle-Class houses.
2. **The Premium for 'View':** High-quality views (`view`) act as a major price multiplier specifically in the top 25% of the market.
3. **Core Utility vs. Luxury:** Middle-class property values are heavily driven by core utilities like `bathrooms` and `sqft_living`, making them safe investments for standard flipping or renting.
