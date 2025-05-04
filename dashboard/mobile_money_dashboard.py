import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# Set page configuration
st.set_page_config(
    page_title="Kenya Mobile Money Analysis",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to load data
@st.cache_data
def load_data():
    # Get the absolute path of the current script (e.g., dashboard/)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate one level up, then into data/processed/
    file_path = os.path.join(base_dir, '..', 'data', 'processed', 'cleaned_mobile_payments.csv')
    file_path = os.path.abspath(file_path)  # Resolves ".." properly

    print(f"Loading data from: {file_path}")  # Optional for debugging

    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    return df


# Load the data
df = load_data()

# Create sidebar for filtering
st.sidebar.title("Kenya Mobile Money Dashboard")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/800px-Flag_of_Kenya.svg.png", width=100)

# Add date range selector
min_date = df['date'].min().date()
max_date = df['date'].max().date()

start_date = st.sidebar.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Filter data based on date selection
filtered_df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]

# Main dashboard
st.title("Kenya Mobile Money Ecosystem Analysis")
st.subheader("Analysis of M-Pesa and Other Mobile Money Services (2007-2025)")

# Overview metrics
st.markdown("### Key Metrics")
col1, col2, col3, col4 = st.columns(4)

latest_data = filtered_df.iloc[-1]
earliest_data = filtered_df.iloc[0]

with col1:
    st.metric("Active Agents", 
              f"{int(latest_data['Active Agents']):,}", 
              f"{int(latest_data['Active Agents']) - int(earliest_data['Active Agents']):,}")

with col2:
    st.metric("Registered Accounts in Millions", 
              f"{int(latest_data['Total Registered Mobile Money Accounts (Millions)']):,}", 
              f"{int(latest_data['Total Registered Mobile Money Accounts (Millions)']) - int(earliest_data['Total Registered Mobile Money Accounts (Millions)']):,}")

with col3:
    st.metric("Transaction Volume in Millions", 
              f"{int(latest_data['Total Agent Cash in Cash Out (Volume Million)']):,}", 
              f"{int(latest_data['Total Agent Cash in Cash Out (Volume Million)']) - int(earliest_data['Total Agent Cash in Cash Out (Volume Million)']):,}")

with col4:
    st.metric("Transaction Value (KES) in Billions", 
              f"{int(latest_data['Total Agent Cash in Cash Out (Value KSh billions)']):,}", 
              f"{int(latest_data['Total Agent Cash in Cash Out (Value KSh billions)']) - int(earliest_data['Total Agent Cash in Cash Out (Value KSh billions)']):,}")

# Create tabs for different visualizations
tab1, tab2, tab3, tab4 = st.tabs(["Growth Trends", "Year-over-Year Analysis", "Per Account Metrics", "Correlations"])

with tab1:
    st.markdown("### Growth of Mobile Money Ecosystem")
    
    # Metric selector for the main chart
    selected_metric = st.selectbox(
        "Select Metric to Visualize",
        options=["Active Agents", "Total Registered Mobile Money Accounts (Millions)", 
                "Total Agent Cash in Cash Out (Volume Million)", "Total Agent Cash in Cash Out (Value KSh billions)"]
    )
    
    # Create line chart
    fig = px.line(filtered_df, x='date', y=selected_metric, 
                  title=f"Growth in {selected_metric} (2007-2025)")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown("### Year-over-Year Growth Analysis")
    
    # Calculate YoY growth for visualization
    if len(filtered_df) >= 13:  # Need at least 13 months for YoY calculation
        yoy_metrics = []
        for col in ["Active Agents", "Total Registered Mobile Money Accounts (Millions)", 
                   "Total Agent Cash in Cash Out (Volume Million)", "Total Agent Cash in Cash Out (Value KSh billions)"]:
            col_short = col.replace("Total ", "").replace(" ", "_")
            filtered_df[f'{col_short}_yoy'] = filtered_df[col].pct_change(12) * 100
            yoy_metrics.append(f'{col_short}_yoy')
        
        # Create multi-line chart for YoY growth
        fig = go.Figure()
        
        for metric in yoy_metrics:
            fig.add_trace(go.Scatter(
                x=filtered_df['date'][12:],  # Skip first year with NaN values
                y=filtered_df[metric][12:],
                mode='lines',
                name=metric.replace('_yoy', '')
            ))
        
        fig.update_layout(
            title="Year-over-Year Growth Rates (%)",
            xaxis_title="Date",
            yaxis_title="Growth Rate (%)",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Not enough data for year-over-year analysis. Please select a longer date range.")

with tab3:
    st.markdown("### Per Account Analysis")
    
    # Calculate metrics per account
    filtered_df['tx_per_account'] = filtered_df['Total Agent Cash in Cash Out (Volume Million)'] / filtered_df['Total Registered Mobile Money Accounts (Millions)']
    filtered_df['value_per_account'] = filtered_df['Total Agent Cash in Cash Out (Value KSh billions)'] / filtered_df['Total Registered Mobile Money Accounts (Millions)']
    
    # Create a two-metric chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Scatter(x=filtered_df['date'], y=filtered_df['tx_per_account'], name="Transactions per Account"),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x=filtered_df['date'], y=filtered_df['value_per_account'], name="Value per Account (KES)"),
        secondary_y=True,
    )
    
    fig.update_layout(
        title_text="Transaction Activity per Registered Account",
        height=500
    )
    
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Transactions per Account", secondary_y=False)
    fig.update_yaxes(title_text="Value per Account (KES)", secondary_y=True)
    
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### Correlation Analysis")
    
    # Calculate correlation matrix
    corr_matrix = filtered_df[["Active Agents", "Total Registered Mobile Money Accounts (Millions)", 
                              "Total Agent Cash in Cash Out (Volume Million)", "Total Agent Cash in Cash Out (Value KSh billions)"]].corr()
    
    # Create correlation heatmap
    fig = px.imshow(corr_matrix, 
                   labels=dict(x="Metric", y="Metric", color="Correlation"),
                   x=corr_matrix.columns,
                   y=corr_matrix.columns,
                   color_continuous_scale="RdBu_r",
                   zmin=-1, zmax=1)
    
    fig.update_layout(
        title="Correlation Matrix of Key Metrics",
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer with insights
st.markdown("---")
st.markdown("### Key Insights")
st.markdown("""
1. The mobile money ecosystem in Kenya has shown remarkable growth since inception in 2007.
2. There appears to be a strong correlation between the number of active agents and transaction volumes.
3. Per-account transaction metrics show how user behavior has evolved over time.
4. Seasonal patterns indicate:
 a) Mobile money activity peaks in November–December, driven by festive spending and end-of-year bonuses.
 b) Transaction volumes and values drop sharply around March–April due to financial strain and tax obligations.
 c) The number of active agents and registered accounts grows steadily throughout the year.
 d) Cash-in and cash-out transactions show higher seasonal volatility than account or agent growth.
""")

# Run the app with: streamlit run mobile_money_dashboard.py