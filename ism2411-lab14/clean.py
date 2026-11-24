# Self-Assessment
#
# 1. Filling missing values feels the most ambiguous to me because the value I use
# can affect the results of the analysis. On real data, I would want to know why
# the values are missing, how the data is used, and whether there is a business
# rule for estimating them before deciding what to fill in.
#
# 2. Yes. I revised my comments so someone unfamiliar with the dataset could
# understand why I made each decision. I explained why I dropped rows missing
# essential identifiers, kept negative revenues because they represent returns,
# and removed the 9999 quantity because it is a placeholder rather than a real order.
#
# 3. The biggest surprise after running describe() was how much one incorrect value
# could distort the dataset. A quantity_sold value of 9999 created a maximum revenue
# of 59994, which was far outside the normal range and showed how strongly one bad
# entry can affect the summary statistics.


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

# Exercise 3 - Handle missing values

print(df.shape)

# Fill numeric columns with only a small number of missing values using the mean
df["quantity_sold"] = df["quantity_sold"].fillna(df["quantity_sold"].mean())

# Drop rows missing essential identifiers because an order needs both an ID and a date
df = df.dropna(subset=["order_id", "order_date"])

print(df.shape)
print(df.isnull().sum())

# Exercise 4 - Fix types

df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
print(df["order_date"].isna().sum())

df["unit_price"] = (
df["unit_price"]
.str.replace("$", "", regex=False)
.str.replace(",", "", regex=False)
.astype(float)
)

df["quantity_sold"] = df["quantity_sold"].astype(int)

df["revenue"] = (df["unit_price"] * df["quantity_sold"]).round(2)

print(df.dtypes)

# Exercise 5 - Check duplicates

print(df.duplicated().sum())

df = df.drop_duplicates()

print(df.shape)

# Exercise 6 - Describe

print(df.describe())

# The negative minimum revenue is suspicious, but it can represent a customer return,
# so I am keeping negative revenues because they are legitimate business transactions.

# The extremely high maximum revenue could initially look like an unusually large bulk order,
# but it is caused by quantity_sold = 9999, a placeholder/data-entry error rather than a real order.

df = df[df["quantity_sold"] != 9999]

print(df.shape)

# Exercise 7 - Save

df.to_csv("data/clean_sales.csv", index=False)

check = pd.read_csv("data/clean_sales.csv")
check.info()

check_dates = pd.read_csv(
"data/clean_sales.csv",
parse_dates=["order_date"]
)
check_dates.info()