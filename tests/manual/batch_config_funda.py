# batch_config.py
# Created 27-10-2020
# Author P. Korteweg

import sys
import os
import scrape

# import folder of package
folder = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(folder)

# 1. Create a website configuration
config = scrape.config.create('http://funda.nl')

# 2. Add tableau data
config['website']['url'] = 'https://www.funda.nl/koop/schoorl/beschikbaar/'
config['website']['id'] = 'content'
config['website']['rows'] = dict.fromkeys(['elem','class'])
config['website']['rows']['elem'] = 'div'
config['website']['rows']['class'] = 'search-result-main'

# 3. Add columns data
config['website']['columns'] = {
"adres": {
    "elem": "h2",
    "class": "search-result__header-title fd-m-none"
},
"postcode": {
    "elem": "h4",
    "class": "search-result__header-subtitle fd-m-none"
},
"kenmerken": {
    "elem": "ul",
    "class": "search-result-kenmerken"
},
"link": {
    "elem": "div",
    "class": "search-result__header-title-col",
    "href": ""
}
}


# Write config to file
filename = 'config_funda.json'
scrape.config.write(filename,config)
