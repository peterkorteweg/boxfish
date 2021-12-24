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
filename = 'config_monster.json'
config = scrape.config.read(filename)

# 2. Make a url
url = 'https://www.monster.com/jobs/search?q=portfolio+manager&where=new+york'

# 3. Scrape url
df = scrape.get_website(url=url, config=config)

# 4. Scrape url with Selenium
url = scrape.utils.urls.replace_subquery(url,'q=asset manager')

config['driver']['package'] = 'selenium'

df2 = scrape.get_website(url=url, config=config)


