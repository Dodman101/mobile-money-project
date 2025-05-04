import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set visualization style
# print(plt.style.available)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("deep")

# Load the data
def load_data():
    # Get the absolute path of the current script (e.g., dashboard/)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate one level up, then into data/processed/
    file_path = os.path.join(base_dir, '..', 'data', 'Mobile Payments.csv')
    file_path = os.path.abspath(file_path)  # Resolves ".." properly

    print(f"Loading data from: {file_path}")  # Optional for debugging

    df = pd.read_csv(file_path)
    return df

# Load the data
df = load_data()


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
def save_data():
    # Get the absolute path of the current script (e.g., dashboard/)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate one level up, then into data/processed/
    file_path = os.path.join(base_dir, '..', 'data', 'processed', 'cleaned_mobile_payments.csv')

    file_path = os.path.abspath(file_path)  # Resolves ".." properly

    print(f"Saving data to: {file_path}")  # Optional for debugging

    return df.to_csv(file_path, index=False)

save_data()

print("\nSummary statistics of the cleaned numeric data:")
print(df[numeric_columns].describe())