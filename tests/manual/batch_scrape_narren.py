# batch_scrape_monster.py
# Created 26-9-2020
# Modiefied 24-12-2021
# Author P. Korteweg

import sys
import os
import requests
import scrape

# import folder of package
folder = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(folder)

# 1. Load a website configuration
filename = 'config_narrenschip.json'
config = scrape.config.read(filename)

# 2. Load page
aurl = 'https://www.datnarrenschip.nl/collections/amsterdam'
response = requests.get(aurl)
page = response.text
soup = scrape.soups.get_soup(page)

# 3. Get tables
website = config["website"]
rows = website["rows"]
cols = website["columns"]
atable = scrape.soups.get_table(soup, rows=rows)
atable2 = scrape.soups.get_table(soup, cols=cols, rows=rows)

# 4. Scrape a page
aurl = 'https://www.datnarrenschip.nl/collections/amsterdam'
df = scrape.get_website(url=aurl, config=config)

# 5. Get next page
# tag = soup.find(id="Collection")
# results = tag.find_all("ul",class_="list--inline pagination")
# alist = scrape.utils.soups.get_strings(results)
# print(alist[0])
# arefs = scrape.utils.soups.get_hrefs(results)
# print(arefs[0])

# 6. Create scraper from scratch
# Note: this requires as input data from the website
# astr1 'Amsterdam Stadsplattegrond in vogelvluchtperspectief - Romeyn de Hooghe / Theodorus Danckerts - 1694'
# astr2 'Amsterdam Aanzicht vanaf het IJ - Frederick de Wit - ca. 1685'

aurl = 'https://www.datnarrenschip.nl/collections/amsterdam'
astr1 = df['Col1'][0]
astr2 = df['Col1'][1]
aconfig = scrape.config.create(aurl)
scrape.config.build_rows(aconfig, url=aurl, slist=[astr1, astr2])
df2 = scrape.get_website(url=aurl, config=aconfig)
