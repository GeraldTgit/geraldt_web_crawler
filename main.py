from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from scrapingbot import get_add_data
from datetime import datetime
import openpyxl
import pandas as pd
import os

# current dateTime
now = datetime.now()

# convert to string
date_time_str = now.strftime("%Y%m%d_%H%M%S")

# Directory to save the file in. Change as needed
print('Enter the directory of your index.html file:')
directory = input()
if os.path.exists(directory) == False: print("File not found!"), exit()

# which is the filename that we want to create. Change as needed
filename = f"{directory}/GERALDT_{date_time_str}.xlsx"

#Fetching data from index.html
with open(f"{directory}/index.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# Create a new workbook
workbook = openpyxl.Workbook(filename)

# The workbook object is then used to add new
worksheet = workbook.active

# Fetching all links with rewards
links = []
for link in soup.find_all("a"):
    href = link.get("href")
    if href and href.startswith("https://rewardsforjustice.net/rewards/"):
        links.append(href)

#Fetching category for each link
cat_h2 = soup.find_all("h2", class_='elementor-heading-title elementor-size-default')
i=0

data = []
# Define the URL to scrape
for r, url in enumerate(links):
    # Check robots.txt
    rp = RobotFileParser()
    rp.set_url(f'{url}/robots.txt')
    rp.read()
    if not rp.can_fetch('*', url):
        print('Cannot fetch URL')
        exit()

    #Fetching category for each link
    if cat_h2:
        div = cat_h2[i]  # 0-based indexing
        category = div.get_text(strip=True)
        categories = category
        i+=2
    else:
        categories = ""

    #Fetching additional data from get_add_data
    data.append(get_add_data(url, categories, title="", reward_amount="", assoc_org="", loc="", about="", img_urls="", dob_value=""))

# Create a data frame
df = pd.DataFrame(data, columns=["Page URL", "Category", "Title", "Reward amount", "Associated Organization(s)", "Associated Location(s)", "About", "Image URL(s)", "Date Of Birth (Store the data in ISO date format)"])

# replace null values with a default value
default_value = 'null'
df.fillna(default_value, inplace=True)

# Save the data frame to an Excel file
print(f"Saving data on {filename} .. .")
df.to_excel(filename, index=False)
print("Done")
