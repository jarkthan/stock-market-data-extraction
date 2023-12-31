from bs4 import BeautifulSoup
import re
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Path to your OAuth2 credentials JSON file (downloaded from Google Cloud Console)
JSON_KEYFILE_PATH = 'spreadsheets_cred.json'

# Scope for Google Sheets API
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Authenticate with OAuth2
credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE_PATH, SCOPE)
gc = gspread.authorize(credentials)

# Open Google Sheet in the specified folder
folder_id = '1kEEd-hSrJdeh4GJr83Ry0NzxwDG4lE7N'  # Replace with the actual folder ID
spreadsheet = gc.open('IndustryGroupList', folder_id=folder_id)

# Url of the web page
url = 'https://www.set.or.th/en/market/product/stock/search'

# Set up the Chrome driver (you need to download chromedriver.exe and provide the path)
service = Service(executable_path='/Users/jarkrunglerdkriangkrai/Downloads/chromedriver-mac-arm64/chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Open the webpage
driver.get(url)

# Extract the HTML content after the page has fully loaded
html_content = driver.page_source

# Quit Chrome
driver.quit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all links in the HTML
all_links = soup.find_all('a')

# Extract the href attribute of each link using a normal loop
href_list = []
for link in all_links:
    href = link.get('href')
    href_list.append(href)

# Remove None values from the list using the filter function
href_list = list(filter(None, href_list))

# Find only the target links
filtered_links = []
link_pattern = re.compile(r'^/en/market/index/set/[^/]+/')
for link in href_list:
    if link_pattern.match(link):
        filtered_links.append(link)

# Define the full url of each industry groups
industry_group_links = []
base_url = "https://www.set.or.th"
for link in filtered_links:
    full_url = base_url + link
    industry_group_links.append(full_url)

# Convert the list to a DataFrame
industry_group_df = pd.DataFrame(industry_group_links, columns=['IndustryGroupList'])

# Open the specific spreadsheet, select the specific worksheet, and update with our data
sheet = gc.open('IndustryGroupList')
worksheet1 = sheet.worksheet('Sheet1')
worksheet1.clear()
worksheet1.update([industry_group_df.columns.values.tolist()] + industry_group_df.values.tolist())
