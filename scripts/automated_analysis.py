import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def run_mobile_money_analysis(input_file='data\Mobile Payments.csv', output_dir='reports'):
    """
    Automated analysis of mobile money data that can be scheduled to run periodically.
    """
    print(f"Starting analysis at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Load and process data
    df = pd.read_csv(input_file)
    
    # Data cleaning and preparation
    df['date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
    df = df.sort_values('date')
    
    # Ensure numeric columns are properly formatted
    numeric_columns = ['Active Agents', 'Total Registered Mobile Money Accounts (Millions)', 
                      'Total Agent Cash in Cash Out (Volume Million)', 'Total Agent Cash in Cash Out (Value KSh billions)']
    
    for col in numeric_columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace(',', '').astype(float)
    
    # Generate report timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Calculate key metrics for the latest month
    latest_month = df.iloc[-1]
    previous_month = df.iloc[-2]
    previous_year_same_month = df[df['date'] == df['date'].iloc[-1] - pd.DateOffset(months=12)].iloc[0] if len(df) > 12 else None
    
    # Create monthly report dataframe
    report_data = {
        'Metric': [],
        'Current Value': [],
        'MoM Change': [],
        'MoM %': [],
        'YoY Change': [],
        'YoY %': []
    }
    
    for col in numeric_columns:
        report_data['Metric'].append(col)
        report_data['Current Value'].append(latest_month[col])
        
        # Month-over-Month calculations
        mom_change = latest_month[col] - previous_month[col]
        mom_pct = (mom_change / previous_month[col] * 100) if previous_month[col] != 0 else 0
        report_data['MoM Change'].append(mom_change)
        report_data['MoM %'].append(mom_pct)
        
        # Year-over-Year calculations (if data available)
        if previous_year_same_month is not None:
            yoy_change = latest_month[col] - previous_year_same_month[col]
            yoy_pct = (yoy_change / previous_year_same_month[col] * 100) if previous_year_same_month[col] != 0 else 0
            report_data['YoY Change'].append(yoy_change)
            report_data['YoY %'].append(yoy_pct)
        else:
            report_data['YoY Change'].append(np.nan)
            report_data['YoY %'].append(np.nan)
    
    # Create the report dataframe
    report_df = pd.DataFrame(report_data)
    
    # Format the numeric columns
    for col in ['Current Value', 'MoM Change', 'YoY Change']:
        report_df[col] = report_df[col].map('{:,.2f}'.format)
    
    for col in ['MoM %', 'YoY %']:
        report_df[col] = report_df[col].map('{:,.2f}%'.format)
    
    # Save report to Excel
    report_file = f"{output_dir}/mobile_money_report_{timestamp}.xlsx"
    with pd.ExcelWriter(report_file, engine='xlsxwriter') as writer:
        # Write the report
        report_df.to_excel(writer, sheet_name='Monthly Summary', index=False)
        
        # Write the raw data
        df.to_excel(writer, sheet_name='Raw Data', index=False)
        
        # Access the workbook and worksheet objects
        workbook = writer.book
        
        # Add formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'bg_color': '#D9E1F2',
            'border': 1
        })
        
        # Create charts in Excel
        chart_sheet = workbook.add_worksheet('Charts')
        
        # Create a chart for registered accounts
        accounts_chart = workbook.add_chart({'type': 'line'})
        
        # Configure the series for the chart
        accounts_chart.add_series({
            'name': 'Registered Accounts',
            'categories': ['Raw Data', 1, df.columns.get_loc('date'), len(df), df.columns.get_loc('date')],
            'values': ['Raw Data', 1, df.columns.get_loc('Total Registered Mobile Money Accounts (Millions)'), 
                       len(df), df.columns.get_loc('Total Registered Mobile Money Accounts (Millions)')],
        })
        
        accounts_chart.set_title({'name': 'Mobile Money Account Growth'})
        accounts_chart.set_x_axis({'name': 'Date'})
        accounts_chart.set_y_axis({'name': 'Number of Accounts'})
        
        chart_sheet.insert_chart('B2', accounts_chart, {'x_scale': 1.5, 'y_scale': 1.5})
    
    print(f"Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Report saved to {report_file}")
    
    return report_file

def send_email_report(report_file, recipient_email, sender_email, password):
    """
    Send the report via email.
    Note: For production use, consider using a more secure approach for credentials.
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Mobile Money Analysis Report - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Message body
        body = """
        Hello,
        
        Please find attached the latest Mobile Money Analysis Report.
        
        Best regards,
        Your Automation System
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach the report
        with open(report_file, "rb") as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(report_file))
        
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_file)}"'
        msg.attach(part)
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        
        print(f"Email sent successfully to {recipient_email}")
        return True
    
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    report_file = run_mobile_money_analysis()
    
    # Uncomment to send email (replace with actual credentials)
    # send_email_report(
    #     report_file=report_file,
    #     recipient_email="recipient@example.com",
    #     sender_email="your_email@gmail.com",
    #     password="your_app_password"  # Use app password for Gmail
    # )