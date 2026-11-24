# Exercise 1 - Inspect

import pandas as pd

df = pd.read_csv("data/messy_sales.csv")

df.info()
print(df.isnull().sum())

# Data quality issues:
# 1. Customer ID has 362 missing values, about 7.54% of the dataset.
# 2. Quantity Sold has 94 missing values, about 1.96% of the dataset.
# 3. Unit Price is stored as object/text, but it should be numeric for calculations.

# Exercise 2 - Standardize column names

df.columns = df.columns.str.lower().str.replace(" ", "_")

print(df.columns.tolist())