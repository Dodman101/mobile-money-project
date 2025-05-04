import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_exploration import numeric_columns, df
from data_analysis import monthly_patterns, correlation

# Function to create time series plots
def plot_time_series(df, column, title, y_label, color='blue'):
    plt.figure(figsize=(12, 6))
    plt.plot(df['date'], df[column], color=color, linewidth=2)
    plt.title(title, fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{title.lower().replace(' ', '_')}.png", dpi=300)
    plt.show()

# Create individual plots for each metric
plot_time_series(df, 'Active Agents', 'Growth in Mobile Money Agents', 'Number of Active Agents', 'green')
plot_time_series(df, 'Total Registered Mobile Money Accounts (Millions)', 'Mobile Money Account Adoption', 'Number of Accounts', 'blue')
plot_time_series(df, 'Total Agent Cash in Cash Out (Volume Million)', 'Transaction Volume Growth', 'Number of Transactions', 'orange')
plot_time_series(df, 'Total Agent Cash in Cash Out (Value KSh billions)', 'Transaction Value Growth', 'Value (KES)', 'red')

# Function to create comparative growth visualizations
def plot_comparative_growth(df, base_year=2010):
    # Filter data starting from base_year
    start_date = pd.Timestamp(year=base_year, month=1, day=1)
    filtered_df = df[df['date'] >= start_date].copy()
    
    # Calculate relative growth with first period as base (=100)
    for col in numeric_columns:
        base_value = filtered_df[col].iloc[0]
        filtered_df[f"{col}_indexed"] = filtered_df[col] / base_value * 100
    
    # Plot indexed growth
    plt.figure(figsize=(14, 8))
    
    for col in numeric_columns:
        indexed_col = f"{col}_indexed"
        label = col.replace('Total ', '').replace(' ', '_')
        plt.plot(filtered_df['date'], filtered_df[indexed_col], linewidth=2, label=label)
    
    plt.title(f'Relative Growth Since {base_year} (Indexed to 100)', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Growth Index (Base=100)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    plt.tight_layout()
    plt.savefig(f"comparative_growth_since_{base_year}.png", dpi=300)
    plt.show()

# Plot comparative growth
plot_comparative_growth(df, base_year=2010)

# Create YoY growth rate visualization
plt.figure(figsize=(14, 8))
for column in numeric_columns:
    col_name = column.split(' ')[-1] if 'Total' in column else column.replace(' ', '_')
    pct_col = f"{col_name}_yoy_growth"
    
    # Skip the first year which will have NaN values
    plt.plot(df['date'][12:], df[pct_col][12:], linewidth=2, 
             label=column.replace('Total ', '').replace(' ', '_'))

plt.title('Year-over-Year Growth Rates', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Growth Rate (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("yoy_growth_rates.png", dpi=300)
plt.show()

# Create a heatmap of the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
plt.title('Correlation Matrix of Key Metrics', fontsize=16)
plt.tight_layout()
plt.savefig("correlation_heatmap.png", dpi=300)
plt.show()

# Create seasonal patterns visualization
plt.figure(figsize=(14, 8))
for column in numeric_columns:
    # Normalize to make all metrics comparable
    normalized = monthly_patterns[column] / monthly_patterns[column].max()
    plt.plot(monthly_patterns.index, normalized, linewidth=2, marker='o',
             label=column.replace('Total ', '').replace(' ', '_'))

plt.title('Seasonal Patterns in Mobile Money Metrics', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Relative Magnitude (Normalized)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig("seasonal_patterns.png", dpi=300)
plt.show()