import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
# print(plt.style.available)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Load the data
df = pd.read_csv('data\Mobile Payments.csv')

# Display the first few rows to understand the structure
print("First 5 rows of the dataset:")
print(df.head())

# Check the data types of each column
print("\nData types:")
print(df.dtypes)

# Check dataset dimensions
print(f"\nDataset dimensions: {df.shape[0]} rows and {df.shape[1]} columns")

# Check column names
print("\nColumn names:")
print(df.columns.tolist())

# Check for missing values
print("\nMissing values in each column:")
print(df.isnull().sum())

# Data cleaning and preparation

# Convert full month names to month numbers
df['Month'] = pd.to_datetime(df['Month'], format='%B').dt.month

# Create a proper date column
df['date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))

# Sort by date to ensure chronological order
df = df.sort_values('date')

# Check for any duplicates
print(f"\nNumber of duplicate rows: {df.duplicated().sum()}")

# Convert numeric columns if they're not already
numeric_columns = ['Active Agents', 'Total Registered Mobile Money Accounts (Millions)', 
                   'Total Agent Cash in Cash Out (Volume Million)', 'Total Agent Cash in Cash Out (Value KSh billions)']

for col in numeric_columns:
    if df[col].dtype == 'object':
        # Remove commas and convert to numeric
        df[col] = df[col].str.replace(',', '').astype(float)

# Add year-month column for easier grouping
df['year_month'] = df['date'].dt.strftime('%Y-%m')

# Save the cleaned dataset
df.to_csv('data\processed\cleaned_mobile_payments.csv', index=False)

print("\nSummary statistics of the cleaned numeric data:")
print(df[numeric_columns].describe())