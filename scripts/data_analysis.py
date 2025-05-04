from data_exploration import numeric_columns, df

# Create a function to calculate year-over-year growth
def calculate_yoy_growth(df, column):
    # Calculate absolute year-over-year difference
    yoy_diff = df[column].diff(12)
    
    # Calculate percentage growth
    yoy_pct = df[column].pct_change(12) * 100
    
    return yoy_diff, yoy_pct

# Apply to each main metric
for column in numeric_columns:
    col_name = column.split(' ')[-1] if 'Total' in column else column.replace(' ', '_')
    diff_col = f"{col_name}_yoy_diff"
    pct_col = f"{col_name}_yoy_growth"
    
    df[diff_col], df[pct_col] = calculate_yoy_growth(df, column)

# Calculate monthly growth rates
for column in numeric_columns:
    col_name = column.split(' ')[-1] if 'Total' in column else column.replace(' ', '_')
    df[f"{col_name}_monthly_growth"] = df[column].pct_change() * 100

# Calculate per account metrics
df['transactions_per_account'] = df['Total Agent Cash in Cash Out (Volume Million)'] / df['Total Registered Mobile Money Accounts (Millions)']
df['value_per_account'] = df['Total Agent Cash in Cash Out (Value KSh billions)'] / df['Total Registered Mobile Money Accounts (Millions)']
df['value_per_transaction'] = df['Total Agent Cash in Cash Out (Value KSh billions)'] / df['Total Agent Cash in Cash Out (Volume Million)']

# Calculate transactions per agent
df['transactions_per_agent'] = df['Total Agent Cash in Cash Out (Volume Million)'] / df['Active Agents']
df['value_per_agent'] = df['Total Agent Cash in Cash Out (Value KSh billions)'] / df['Active Agents']

# Check correlations between key metrics
correlation = df[numeric_columns].corr()
print("\nCorrelation matrix:")
print(correlation)

# Calculate seasonal patterns (monthly averages)
monthly_patterns = df.groupby(df['date'].dt.month)[numeric_columns].mean()
monthly_patterns.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Calculate compound annual growth rate (CAGR)
def calculate_cagr(start_value, end_value, num_years):
    return (end_value / start_value) ** (1 / num_years) - 1

# Calculate for each numeric column
for col in numeric_columns:
    start_val = df[col].iloc[0]
    end_val = df[col].iloc[-1]
    years = df['date'].iloc[-1].year - df['date'].iloc[0].year + (df['date'].iloc[-1].month - df['date'].iloc[0].month) / 12
    
    if start_val > 0:  # Avoid division by zero
        cagr = calculate_cagr(start_val, end_val, years)
        print(f"CAGR for {col}: {cagr:.2%}")