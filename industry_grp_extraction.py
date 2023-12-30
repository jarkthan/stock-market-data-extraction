from bs4 import BeautifulSoup
import re

# Open the HTML file
with open('industry_page.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all links in the HTML
all_links = soup.find_all('a')

# Initialize an empty list to store href attributes
href_list = []

# Extract the href attribute of each link using a normal loop
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

for link in industry_group_links:
    print(link)
