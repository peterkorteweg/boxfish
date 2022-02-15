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


def test_is_child():
    pxpath = '/html/body/p[2]'
    npxpath = '/html/body/p[1]'
    npxpath2 = '/html/body/b[1]'
    axpath = pxpath + '/a[2]'

    pxpaths = [axpath]

    # Xpath is child
    axpaths = [npxpath, pxpath]
    assert scrape.xpaths.is_child(axpath, axpaths)

    # Xpath is in axpaths but not a child
    axpaths = [npxpath, axpath, npxpath2]
    assert not scrape.xpaths.is_child(axpath, axpaths)

    # Xpath is not in axpath and not a child
    axpaths = [npxpath, npxpath2]
    assert not scrape.xpaths.is_child(axpath, axpaths)


def test_is_descendant():

    gxpath = '/html/body/'
    pxpath = gxpath + '/p[2]'
    axpath = pxpath + '/a[2]'

    pxpaths1 = ['/html/body/p[2]/a[1]', axpath, '/html/body/p[2]/a[3]']
    pxpaths2 =['/html/body/p[1]', pxpath, '/html/body/p[3]']
    pxpaths3 = ['/html/head', '/html/head/title', gxpath]

    # Xpath is descendant (level 1)
    axpaths = [pxpath]
    assert scrape.xpaths.is_descendant(axpath, axpaths)

    axpaths = pxpaths2
    assert scrape.xpaths.is_descendant(axpath, axpaths)

    # Xpath is descendant (level 2)
    axpaths = [gxpath]
    assert scrape.xpaths.is_descendant(axpath, axpaths)

    axpaths = pxpaths3
    assert scrape.xpaths.is_descendant(axpath, axpaths)

    # Xpath is not a desdendant
    axpaths = [axpath]
    assert not scrape.xpaths.is_descendant(axpath, axpaths)

    axpaths = pxpaths1
    assert not scrape.xpaths.is_descendant(axpath, axpaths)


def test_split():
    # Test single item
    axpath = '/html/body/p[1]/b'
    [names, indices] = scrape.xpaths.split(axpath)
    assert names == ['html', 'body', 'p', 'b']
    assert indices == [1, 1, 1, 1]

    # Test multiple items
    axpath = '/html/body/p[2]/a[2]'
    [names, indices] = scrape.xpaths.split(axpath)
    assert names == ['html', 'body', 'p', 'a']
    assert indices == [1, 1, 2, 2]
