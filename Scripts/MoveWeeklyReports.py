import os
import shutil
import datetime
from datetime import timedelta

# Define source and destination directories
source_dir = '../WeeklyMarketReports'  # Replace with your source directory
dest_dir = '../WeeklyMarketReports2'  # Replace with your destination directory

# Create destination directory if it doesn't exist
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Define the start and end dates
end_date = datetime.datetime.strptime('20250331', '%Y%m%d')
start_date = datetime.datetime.strptime('20190523', '%Y%m%d')

# List to store the selected files
selected_files = []

# Work backwards from the end date to the start date in weekly increments
current_date = end_date
while current_date >= start_date:
    # Format the date to match the filename format
    date_str = current_date.strftime('%Y%m%d')
    file_name = f"PUB_WeeklyMarket_{date_str}.csv"
    file_path = os.path.join(source_dir, file_name)
    
    # Check if the file exists
    if os.path.exists(file_path):
        selected_files.append(file_name)
        # Copy the file to the destination directory
        shutil.copy2(file_path, os.path.join(dest_dir, file_name))
        print(f"Copied: {file_name}")
    else:
        print(f"Warning: File not found: {file_name}")
    
    # Move back one week
    current_date -= timedelta(days=7)

print(f"\nCopied {len(selected_files)} weekly market reports from {end_date.strftime('%Y-%m-%d')} to {start_date.strftime('%Y-%m-%d')}")