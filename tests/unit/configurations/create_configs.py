# create_configs.py

import boxfish as bf
import pandas as pd

# BOOKSTOSCRAPE
url = 'http://books.toscrape.com'
url_next_page_full = 'https://books.toscrape.com/catalogue/page-2.html'
url_next_page_partial = 'catalogue/page-2.html'

filename = './config_bookstscrape2.json'
config = bf.config.create(url)

config['driver']['selenium']['filename'] = r'..\..\drivers\geckodriver.exe'
config['driver']['selenium']['log'] = r'..\..\drivers\geckodriver.log'

config['output']['filename'] = r'.\results\bookstoscrape2.csv'
config['output']['overwrite'] = True

# Build rows, single page
rows = ["A Light in","Tipping the Velvet"]
config = bf.config.build(config, url=url, rows=rows)
# bf.config.write(filename,config)

config = bf.config.build(config, url=url, next_page=url_next_page_partial)

# Extract data and analyse data
data = bf.extract(url,config)
headers = data.pop(0)
df = pd.DataFrame(data, columns=headers)
print(df.head())

# cols = ["A Light in", "51.77"]
# bf.config.build(config, url=url, rows=rows, cols=cols, search=bf.config.SEARCH_NONE)

