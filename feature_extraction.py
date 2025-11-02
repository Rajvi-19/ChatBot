# ChatBot

import pandas as pd

excel = pd.read_excel("Finance_document.xlsx", sheet_name="Sheet1")

# Create the df variable from the excel DataFrame
df = excel.copy()

df.to_csv("data.csv", index=False)

df["Revenue Growth (%)"] = df.groupby(['Company'])['Revenue'].pct_change() * 100

# Income growth
df['Net Income Growth (%)'] = df.groupby(['Company'])['Net Income'].pct_change() * 100

# Convert relevant columns to numeric, coercing errors
df['Net Income'] = pd.to_numeric(df['Net Income'], errors='coerce')
df['Revenue'] = pd.to_numeric(df['Revenue'], errors='coerce')
df['Total Assets'] = pd.to_numeric(df['Total Assets'], errors='coerce')
df['Total Liabilities'] = pd.to_numeric(df['Total Liabilities'], errors='coerce')

#Profit margin
df["Profit Margin (%)"] = (df["Net Income"] / df["Revenue"]) * 100

# Return on Assets
df["ROA (%)"] = (df["Net Income"] / df["Total Assets"]) * 100

#Debt to asset ratio
df["Debt to Asset Ratio"] = df["Total Liabilities"] / df["Total Assets"]


# Display the updated DataFrame
display(df)

