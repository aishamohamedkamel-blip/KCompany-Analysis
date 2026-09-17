# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 12:01:55 2026

@author: Aisha
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as pltpy


KCompany = pd.read_csv(r'C:/Users/Aisha/Desktop/All About Python/Portfolio/King Housing Dataset/kc_house_data.csv')

KCompany.isnull().sum()

Dups = KCompany[KCompany.duplicated()]

MiddleClassLimit = KCompany['price'].quantile(0.75)

KCompany['Housing Class']= KCompany['price'].apply(lambda x: 'Luxury Class' if x > MiddleClassLimit else 'Middle Class')

KCompany['date'] = pd.to_datetime(KCompany['date'])

KCompany['Sale Year'] = KCompany['date'].dt.year

KCompany["House Age"] = KCompany["Sale Year"] - KCompany["yr_built"]

KCompany['is_renovated'] = (KCompany['Housing Class'] == 'Luxury Class').astype(int)

KCompany['is_luxury'] = (KCompany['Housing Class'] == 'Luxury Class').astype(int)

KCompany["price_per_sqft"] = (KCompany["price"] / KCompany["sqft_living"]).round(2)

KCompanyProperties = KCompany.drop_duplicates(subset=['id','long','lat'], keep = 'first')

MultipleTransHousing = KCompany[KCompany.duplicated(subset=['long','lat'], keep = 'first')].drop_duplicates(subset='id', keep = 'first')

KCompanyProperties.boxplot(column = 'price')

MiddleClassData = KCompanyProperties[KCompanyProperties['Housing Class'] == 'Middle Class']

MiddleClassData.boxplot(column = 'price')

LuxuryClassData = KCompanyProperties[KCompanyProperties['Housing Class'] == 'Luxury Class']

LuxuryClassData.boxplot(column = 'price')

########


import statsmodels.formula.api as smf

KCompanyProperties['log_price'] = np.log(KCompanyProperties['price'])
MiddleClassData['log_price'] = np.log(MiddleClassData['price'])
LuxuryClassData['log_price'] = np.log(LuxuryClassData['price'])


# Define the baseline housing features to evaluate
FeatureFormula = 'log_price ~ bedrooms + bathrooms + sqft_living + view + grade + condition + yr_built'

print("\n" + "="*60 + "\nANALYSIS 1: HOUSING FEATURE VALUE DRIVERS BY CLASS\n" + "="*60)

# ---------------------------------------------------------------------
# PART A: SPLIT SUBGROUP MODELS
# ---------------------------------------------------------------------
# White-robust standard errors (HC3) to handle property variance
mid_model = smf.ols(FeatureFormula, data=MiddleClassData).fit(cov_type='HC3')
lux_model = smf.ols(FeatureFormula, data=LuxuryClassData).fit(cov_type='HC3')

print("--- 1. Subgroup R-Squared Results ---")
print(f"Middle Class Model Fit: {mid_model.rsquared:.4f}")
print(f"Luxury Class Model Fit: {lux_model.rsquared:.4f}\n")

# Stack parameters to compare them side-by-side
compare_drivers = pd.DataFrame({
    'Middle Class Baseline Drivers': mid_model.params,
    'Luxury Class Baseline Drivers': lux_model.params
})
print("--- 2. Coefficient Comparison Matrix ---")
print(compare_drivers)


# ---------------------------------------------------------------------
# PART B: UNIFIED INTERACTION MODEL
# ---------------------------------------------------------------------
# We interact 'is_luxury' with 'view' and structural 'grade' to prove behavioral differences
interaction_formula = (
    'log_price ~ bedrooms + bathrooms + sqft_living + view + grade + condition + yr_built + '
    'is_luxury + is_luxury:view + is_luxury:grade'
)
interaction_model = smf.ols(interaction_formula, data=KCompanyProperties).fit(cov_type='HC3')

print("\n--- 3. Interaction Significance Testing ---")
interaction_summary = interaction_model.summary2().tables[1] # Extract coefficient & p-value table
print(interaction_summary.loc[['is_luxury:view', 'is_luxury:grade']])



compare_drivers.to_csv('Comparing Drivers')


KCompanyProperties.to_csv('KCompany Housing Processed Dataset', index = False)


import seaborn as sns

sns.boxplot(x="Housing Class", y="price", data=KCompanyProperties)
