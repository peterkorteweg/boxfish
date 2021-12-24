# batch_scrape_monster.py
# Created 26-9-2020
# Author P. Korteweg

import sys
import os
import scrape

# import folder of package
folder = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(folder)

# 1. Load a website configuration
filename = 'config_funda.json'
config = scrape.config.read(filename)

#config['driver']['package'] = 'selenium'
config['driver']['package'] = 'requests'

# 2. Scrape a page
aurl = 'https://www.funda.nl/koop/schoorl/beschikbaar/'
df = scrape.get_website(url=aurl, config=config)

# # 3. Scrape query from website
# path = scrape.config.get_path(config)
# path['gemeente']='Bergen-NH'
# df = scrape.get_website(path=path, config=config)
