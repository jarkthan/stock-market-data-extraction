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
stock_sheet = gc.open('StockList', folder_id=folder_id)
industry_sheet = gc.open('IndustryGroupList', folder_id=folder_id)

# Select the specific worksheet
worksheet1 = sheet.worksheet('Sheet1')

# Replace 'https://example.com' with the actual URL of the web page you want to scrape
url = industry_group_links[1]

# Set up the Chrome driver (you need to download chromedriver.exe and provide the path)
chrome_path = '/Users/jarkrunglerdkriangkrai/Downloads/chromedriver-mac-arm64/chromedriver'  # Replace with the actual path
# service = ChromeService(chrome_path)
driver = webdriver.Chrome(executable_path=chrome_path)

# Open the webpage
driver.get(url)

# Extract the HTML content after the page has fully loaded
html_content = driver.page_source

# Parse the HTML content as needed (e.g., using BeautifulSoup)
# Here, we use a simple example with Selenium to find an element by its class name
all_contents = driver.find_elements(By.TAG_NAME, 'a')

all_links = []

for content in all_contents:
    href = content.get_attribute('href')
    all_links.append(href)

stock_links = []

for link in all_links:
    if isinstance(link, str) and '/en/market/product/stock/quote/' in link:
        stock_links.append(link)

# Close the browser
driver.quit()
