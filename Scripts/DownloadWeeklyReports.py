import re
import requests
from bs4 import BeautifulSoup

# URL of the Weekly Market reports page
url = "https://reports-public.ieso.ca/public/WeeklyMarket/"

# Fetch HTML content from the webpage
response = requests.get(url)
if response.status_code == 200:
    html_content = response.text

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract all links ending with .csv
    csv_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.csv')]

    # Filter links to exclude those with '_*' before .csv
    # filtered_links = csv_links
    filtered_links = [link for link in csv_links if re.search(r'^.*\d{8}\.csv$', link)]

    # Print filtered links
    print("Filtered Links:")
    for link in filtered_links:
        print(link)

        # Download each file
        file_url = url + link
        file_name = link.split('/')[-1]
        with open(file_name, 'wb') as file:
            file.write(requests.get(file_url).content)
            print(f"Downloaded {file_name}")
else:
    print(f"Failed to fetch webpage: {response.status_code}")
