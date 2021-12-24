# batch_soup.py
# Created 28-2-2021
# Author P. Korteweg

import sys
import os

# from bs4 import BeautifulSoup

# import folder of package
folder = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(folder)

# # Simple example to get a URL page with requests
# response = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
# page = response.text
# soup = scrape.utils.soups.get_soup(page)
#
# alist = scrape.utils.soups.get_strings(soup)
# print(alist)

#
PAGE_DORMOUSE = """<html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story" id = "story1">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """
page = PAGE_DORMOUSE
soup = scrape.data.soups.get_soup(page)

alist = scrape.data.soups.get_strings(soup)
print(alist)
