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


# 6. Create scraper from scratch
# Note: this requires as input data from the website
# astr1 ABW
# astr2 NGA

aurl = 'https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3'
astr1 = 'Aruba'
astr2 = 'Niger'
aconfig = scrape.config.create(aurl)
scrape.config.build_rows(aconfig, url=aurl, slist=[astr1, astr2])
df2 = scrape.get_website(url=aurl, config=aconfig)
