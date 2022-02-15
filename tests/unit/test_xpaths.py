# test_xpaths.py

import scrape
from scrape.utils.utils import read

# BS4 Default example
FILE_DORMOUSE = r'.\data\dormouse.html'
ROWS_DORMOUSE = {"elem": "a", "class": "sister"}
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


# Helper functions
def get_page(filename=FILE_DORMOUSE):
    if filename is '':
        page = PAGE_DORMOUSE
    else:
        page = scrape.utils.utils.read(filename)
    return page


def test_xpath_is_child():
    soup = scrape.soups.get_soup(get_page())
    alist = scrape.soups.xpaths(soup)

    afilter = {'elem': 'a'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    aitem = aresults[1]
    aparent = aitem.parent
    gparent = aparent.parent

    axpath = scrape.soups.xpath(aitem)
    pxpath = scrape.soups.xpath(aparent)
    pxpaths = scrape.soups.xpaths(aparent)
    gxpaths = scrape.soups.xpaths(gparent)


    # Xpath is child
    axpaths = list(set(gxpaths) - {axpath})
    assert scrape.xpaths.xpath_is_child(axpath, axpaths)

    # Xpath is in axpaths but not a child
    axpaths = pxpaths
    assert not scrape.xpaths.xpath_is_child(axpath, axpaths)

    # Xpath is not in axpath and not a child
    axpaths = list(set(pxpaths) - {axpath})
    assert not scrape.xpaths.xpath_is_child(axpath, axpaths)


def test_xpath_is_descendant():
    soup = scrape.soups.get_soup(get_page())
    alist = scrape.soups.xpaths(soup)

    afilter = {'elem': 'a'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    aitem = aresults[1]
    parent1 = aitem.parent
    parent2 = parent1.parent
    parent3 = parent2.parent

    axpath = scrape.soups.xpath(aitem)
    pxpath1 = scrape.soups.xpath(parent1)
    pxpath2 = scrape.soups.xpath(parent2)
    pxpaths1 = scrape.soups.xpaths(parent1)
    pxpaths2 = scrape.soups.xpaths(parent2)
    pxpaths3 = scrape.soups.xpaths(parent3)

    # Xpath is descendant (level 1)
    axpaths = [pxpath1]
    assert scrape.xpaths.xpath_is_descendant(axpath, axpaths)

    axpaths = pxpaths2
    assert scrape.xpaths.xpath_is_descendant(axpath, axpaths)

    # Xpath is descendant (level 2)
    axpaths = [pxpath2]
    assert scrape.xpaths.xpath_is_descendant(axpath, axpaths)

    axpaths = pxpaths3
    assert scrape.xpaths.xpath_is_descendant(axpath, axpaths)

    # Xpath is not a desdendant
    axpaths = [axpath]
    assert not scrape.xpaths.xpath_is_descendant(axpath, axpaths)

    axpaths = pxpaths1
    assert not scrape.xpaths.xpath_is_descendant(axpath, axpaths)


def test_xpath_split():
    soup = scrape.soups.get_soup(get_page())

    # Test single item
    afilter = {'elem': 'b'}
    aitem = scrape.soups.find_item(soup, afilter=afilter)
    xpath = scrape.soups.xpath(aitem)
    [names, indices] = scrape.xpaths.xpath_split(xpath)
    assert names == ['html', 'body', 'p', 'b']
    assert indices == [1, 1, 1, 1]

    # Test multiple items
    afilter = {'elem': 'a'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    aitem = aresults[1]
    xpath = scrape.soups.xpath(aitem)
    [names, indices] = scrape.xpaths.xpath_split(xpath)
    assert names == ['html', 'body', 'p', 'a']
    assert indices == [1, 1, 2, 2]
