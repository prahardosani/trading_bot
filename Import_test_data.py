#This script will download yahoo finance data and save to csv for a particular stock.

import yfinance as yf # Import yfinance library to get the data from yahoo finance.
import os  # Import the os module for working with file paths
from datetime import datetime # Import datetime module to work with date times :/

# Define the folder path where you want to save the CSV file
folder_path = "./Historical_Data"

# Ensure the folder exists; create it if it doesn't
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Define the ticker symbol and date range
symbol = "AAPL"
start_date = "2020-01-01" #Static start_date to get enough data to back test
end_date = datetime.now().strftime("%Y-%m-%d")  # Use today's date as the end date

# Download historical data
data = yf.download(symbol, start=start_date, end=end_date)

# Generate the CSV file name based on symbol, start date, and end date
csv_file_name = f"{symbol}_{start_date}_{end_date}.csv"

# Specify the full path for the CSV file
csv_file_path = os.path.join(folder_path, csv_file_name)

# Save data to the CSV file in the specified folder
data.to_csv(csv_file_path)

print(f"Data saved to: {csv_file_path}")
