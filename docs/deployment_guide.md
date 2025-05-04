Kenya Mobile Money Analysis - Deployment Guide
==============================================

This guide provides detailed instructions for setting up and deploying the Kenya Mobile Money Analysis project, including the interactive dashboard and automated reporting system.

Prerequisites
-------------

Before starting, ensure you have:

-   Python 3.8+ installed
-   Git installed
-   Basic knowledge of command line operations
-   Approximately 2GB of free disk space
-   A GitHub account (for cloning the repository)
-   [Optional] Streamlit account (for deploying the dashboard publicly)

Local Setup
-----------

### 1\. Clone the Repository

```
git clone https://github.com/[your-username]/kenya-mobile-money-analysis.git
cd kenya-mobile-money-analysis

```

### 2\. Set Up a Virtual Environment

#### For Windows:

```
python -m venv venv
venv\Scripts\activate

```

#### For macOS/Linux:

```
python3 -m venv venv
source venv/bin/activate

```

### 3\. Install Dependencies

```
pip install -r requirements.txt

```

This will install all necessary packages including:

-   pandas==1.5.3
-   numpy==1.23.5
-   matplotlib==3.7.1
-   seaborn==0.12.2
-   streamlit==1.22.0
-   plotly==5.14.1
-   statsmodels==0.13.5
-   scikit-learn==1.2.2
-   xlsxwriter==3.1.0
-   prophet==1.1.2
-   openpyxl==3.1.2

### 4\. Prepare the Data

The project uses a CSV file containing Kenya's mobile money data from 2007 to 2025.

1.  Ensure `Mobile_Payments.csv` is in the root directory of the project
2.  Run the data preparation script:

    ```
    python data_preparation.py

    ```

    This will clean the data and create necessary derivative datasets for analysis.

Running the Local Dashboard
---------------------------

To run the Streamlit dashboard locally:

```
streamlit run mobile_money_dashboard.py

```

This will start a local server and automatically open the dashboard in your default web browser (typically at http://localhost:8501).

Setting Up Automated Reporting
------------------------------

The automated reporting system generates periodic analysis reports based on the mobile money data.

### 1\. Configure Report Settings

Edit `config/report_config.json` to customize your report settings:

```
{
  "report_frequency": "monthly",  // Options: "daily", "weekly", "monthly"
  "report_format": "pdf",         // Options: "pdf", "excel", "html"
  "email_delivery": false,        // Set to true to enable email delivery
  "recipients": [],               // Add email addresses if email_delivery is true
  "report_sections": [
    "executive_summary",
    "growth_metrics",
    "seasonal_analysis",
    "correlation_analysis",
    "forecasts"
  ]
}

```

### 2\. Set Up Report Scheduling

#### Using Cron (Linux/macOS):

1.  Open your crontab file:

    ```
    crontab -e

    ```

2.  Add a line to schedule the automated report generation (monthly example):

    ```
    0 0 1 * * cd /path/to/kenya-mobile-money-analysis && /path/to/venv/bin/python automated_analysis.py

    ```

#### Using Task Scheduler (Windows):

1.  Open Task Scheduler
2.  Create a new Basic Task
3.  Set the trigger (e.g., monthly on the 1st)
4.  Set the action to:
    -   Program: `C:\path\to\venv\Scripts\python.exe`
    -   Arguments: `C:\path\to\kenya-mobile-money-analysis\automated_analysis.py`
    -   Start in: `C:\path\to\kenya-mobile-money-analysis`

Cloud Deployment
----------------

### Deploying to Streamlit Cloud

1.  Ensure your code is pushed to GitHub
2.  Create an account at [streamlit.io](https://streamlit.io/)
3.  Create a new app and connect it to your GitHub repository
4.  Select the `mobile_money_dashboard.py` file as the main file
5.  Deploy the app

The app will be available at `https://[your-username]-kenya-mobile-money-analysis.streamlit.app`

### Alternative Cloud Deployment Options

#### Heroku Deployment

1.  Install Heroku CLI
2.  Create a `Procfile` in the project root with:

    ```
    web: streamlit run mobile_money_dashboard.py

    ```

3.  Deploy with:

    ```
    heroku loginheroku create kenya-mobile-money-appgit push heroku main

    ```

#### AWS Deployment

For production-level deployment with higher resource needs:

1.  Create an EC2 instance (t2.medium or higher recommended)

2.  Install required packages:

    ```
    sudo apt update
    sudo apt install python3-pip python3-venv

    ```

3.  Clone the repository and follow the local setup instructions

4.  Set up a systemd service for persistent running:

    ```
    sudo nano /etc/systemd/system/mobile-money-dashboard.service

    ```

    Add the following content:

    ```
    [Unit]
    Description=Kenya Mobile Money Dashboard
    After=network.target

    [Service]
    User=ubuntu
    WorkingDirectory=/path/to/kenya-mobile-money-analysis
    ExecStart=/path/to/venv/bin/streamlit run mobile_money_dashboard.py
    Restart=always

    [Install]
    WantedBy=multi-user.target

    ```

5.  Enable and start the service:

    ```
    sudo systemctl enable mobile-money-dashboard
    sudo systemctl start mobile-money-dashboard

    ```

Setting Up Email Notifications
------------------------------

To enable email delivery of reports:

1.  Create a `.env` file in the project root
2.  Add your email configuration:

    ```
    EMAIL_SENDER=your-email@example.comEMAIL_PASSWORD=your-app-passwordSMTP_SERVER=smtp.gmail.comSMTP_PORT=587

    ```

3.  Set `email_delivery` to `true` in your report config
4.  Add recipient email addresses to the `recipients` list

Troubleshooting
---------------

### Common Issues and Solutions

1.  **Dashboard fails to load data**

    -   Check that `Mobile_Payments.csv` is properly located in the data directory
    -   Verify the CSV format matches the expected structure
    -   Run `python data_validation.py` to check for data integrity issues
2.  **Visualization rendering issues**

    -   Update plotly: `pip install plotly --upgrade`
    -   Clear your browser cache or try a different browser
3.  **Automated reports not generating**

    -   Check the log files in `logs/report_generation.log`
    -   Verify the scheduled task is running properly
    -   Ensure the python environment is correctly activated in your scheduler
4.  **Dashboard running slowly**

    -   Consider using the caching features of Streamlit by adding `@st.cache_data` decorators
    -   Optimize data queries in `data_analysis.py`

Updating the Project
--------------------

To update the project with new data or code changes:

1.  Pull the latest code:

    ```
    git pull origin main

    ```

2.  Update dependencies if needed:

    ```
    pip install -r requirements.txt --upgrade

    ```

3.  If using new data, run the data preparation script again:

    ```
    python data_preparation.py

    ```

Security Considerations
-----------------------

1.  Do not commit sensitive information (API keys, passwords) to the repository
2.  Use environment variables or `.env` files (added to `.gitignore`) for sensitive configuration
3.  If deploying publicly, consider adding authentication to the Streamlit dashboard

Contact for Support
-------------------

For technical assistance with deployment or customization, contact:

-   Email: support@smatica.com
-   Website: https://smatica.com/support

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.