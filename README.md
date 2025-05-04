Kenya Mobile Money Analysis Project
===================================

![Dashboard Preview](https://github.com/Dodman101/mobile-money-project/blob/main/reports/assests/dashboard_preview.png)

Overview
--------

This project analyzes Kenya's revolutionary mobile money ecosystem from 2007 to 2025, tracking its transformation from an experimental service to a financial backbone that has fundamentally reshaped the nation's economy. Using comprehensive monthly data on agents, accounts, and transactions, we provide deep insights into one of the world's most successful financial inclusion initiatives.

Live Demo
---------

[View the live dashboard here](https://kenya-mobile-money-analysis-dashboard.streamlit.app/)

Features
--------

-   **Comprehensive Time Series Analysis**: Detailed examination of growth patterns across multiple metrics
-   **Interactive Dashboard**: Dynamic visualizations with filtering and drill-down capabilities
-   **Seasonal Pattern Detection**: Identification of annual usage cycles and their economic implications
-   **Correlation Analysis**: Exploration of relationships between infrastructure, adoption, and usage metrics
-   **Growth Phase Identification**: Recognition of distinct evolutionary phases in the ecosystem
-   **Predictive Modeling**: Forecasting of future trends based on historical patterns
-   **Automated Reporting**: Scheduled generation of analytical reports for ongoing monitoring

Key Metrics Analyzed
--------------------

The analysis focuses on four fundamental metrics that define Kenya's mobile money ecosystem:

1.  **Active Mobile Money Agents**: The physical infrastructure enabling cash deposits and withdrawals
2.  **Registered Mobile Money Accounts**: The user adoption metric tracking overall penetration
3.  **Transaction Volume**: The number of transactions processed through the system
4.  **Transaction Value**: The monetary value of transactions processed (in KSh billions)

Key Insights
------------

Our analysis revealed several critical insights:

1.  **Extraordinary Growth**: All key metrics grew by approximately 13-16x their 2010 values by 2025
2.  **Infrastructure Expansion**: Agent network growth from fewer than 1,000 agents in 2007 to approximately 400,000 by 2025
3.  **Widespread Adoption**: Growth to over 80 million registered accounts by 2025 (in a country of 55 million people)
4.  **Ecosystem Integration**: Remarkably high correlations (≥0.96) between all metrics, indicating well-coordinated expansion
5.  **Seasonal Patterns**: Clear annual cycles with peak activity in December-February and troughs in March-April and June
6.  **Pandemic Impact**: COVID-19 created an inflection point around 2020, accelerating growth in transaction value
7.  **Market Maturation**: While growth rates have naturally moderated, the ecosystem continues to expand across all metrics

Project Structure
-----------------

```
kenya-mobile-money-analysis/
├── data/
│   ├── Mobile_Payments.csv            # Raw mobile money data
│   └── processed/                     # Directory for processed datasets
│   └── cleaned_mobile_payments.csv    # Cleaned and processed mobile money data
├── scripts/
│   ├── data_preparation.py            # Data cleaning and preparation
│   ├── data_analysis.py               # Core analytical functions
│   ├── visualization.py               # Visualization generation
│   └── automated_analysis.py          # Automated reporting system
├── dashboard/
│   ├── mobile_money_dashboard.py      # Main Streamlit dashboard
├── reports/                           # Auto-generated reports
│   └── assets/                        # Directory for the initial graphs
├── docs/
│   ├── executive_summary.md           # Executive summary of findings
│   ├── case_study.md                  # Detailed case study analysis
│   ├── The Mobile Money Revolution in Kenya (2007-2025).pdf  # Detailed report of the study
│   └── deployment_guide.md            # Setup and deployment instructions
├── .gitignore                         # Git ignore file
├── requirements.txt                   # Project dependencies
└── README.md                          # Project overview (this file)

```

Technologies Used
-----------------

-   **Data Processing**: Python, pandas, numpy
-   **Statistical Analysis**: statsmodels, scikit-learn, Prophet
-   **Visualization**: matplotlib, seaborn, plotly
-   **Dashboard**: Streamlit
-   **Automated Reporting**: Python scheduler, XlsxWriter, ReportLab
-   **Version Control**: Git, GitHub

Setup and Installation
----------------------

For detailed setup instructions, see the [Deployment Guide](https://github.com/Dodman101/mobile-money-project/blob/main/docs/deployment_guide.md).

Quick setup:

```
# Clone the repository
git clone https://github.com/Dodman101/mobile-money-project.git
cd kenya-mobile-money-analysis

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard/mobile_money_dashboard.py

```

Documentation
-------------

-   [Executive Summary](https://github.com/Dodman101/mobile-money-project/blob/main/docs/executive_summary.md): High-level overview of key findings
-   [Case Study](https://github.com/Dodman101/mobile-money-project/blob/main/docs/case_study.md): Detailed analysis of Kenya's mobile money evolution
-   [Full Report](https://github.com/Dodman101/mobile-money-project/blob/main/docs/The%20Mobile%20Money%20Revolution%20in%20Kenya%20(2007-2025).pdf): Detailed pdf report of Kenya's mobile money study
-   [Deployment Guide](https://github.com/Dodman101/mobile-money-project/blob/main/docs/deployment_guide.md): Instructions for setting up and deploying the project

About Smatica
-------------

This project was developed by [Smatica](https://smatica-official-website.onrender.com/), a data analytics and visualization consultancy specializing in financial inclusion and emerging market analysis. We help organizations understand complex data landscapes through interactive dashboards, detailed analysis, and automated reporting systems.

For inquiries about custom analysis or dashboard development, contact us at:

-   Email: [info@smatica.co.ke](https://smatica-official-website.onrender.com/contact.html)
-   Website: [https://smatica.co.ke](https://smatica-official-website.onrender.com/)

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
---------------

-   Data sources: Central Bank of Kenya, Communications Authority of Kenya, Kaggle Datasets (Kenya's Mobile Money Payments Data by Collins Ogombo)
-   Academic references on mobile money and financial inclusion
-   Open source community for the excellent data analysis and visualization tools