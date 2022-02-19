# test_soups.py

import bs4
from bs4 import BeautifulSoup
import copy
import re
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


# BS4 Tree example
FILE_TREE = r'.\data\tree.html'
ID1_TREE = 'tree1'
ID2_TREE = 'tree2'

# Books to scrape example
FILE_BOOKS = r'.\data\bookstoscrape.html'
ID_BOOKS = 'default'
ROWS_PARENT_NAME_BOOKS = 'ol'
ROWS_PARENT_CLASS_BOOKS = ['row']
ROWS_BOOKS = {"elem": "li",
              "class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"
              }
COLS_BOOKS = {"rating": {"elem": "p",
                         "class": "star-rating"
                         },
              "price": {"elem": "p",
                        "class": "price_color"
                        }
              }
COLS_BOOKS_NO_MATCH = {"rating": {"elem": "a",
                                  "class": "star-rating"
                                  },
                       "price": {"elem": "a",
                                 "class": "price_color"
                                 }
                       }
ITEMS_ON_PAGE_BOOKS = 20
COLUMNS_BOOKS = 4

# Wikipedia lists
FILE_WIKI = r'.\data\ISO3166.html'
LISTS_NUMBER_WIKI = 44

LISTS_FILTER_WIKI = {"class": "vector-menu-content-list"}
LISTS_FILTER_NUMBER_WIKI = 11

LISTS_FILTER_ELEM_WIKI = {"elem": "ul"}
LISTS_FILTER_ELEM_NUMBER_WIKI = 11

TABLE_NUMBER_WIKI = 2


# Helper functions
def get_page(filename=FILE_DORMOUSE):
    if filename is '':
        page = PAGE_DORMOUSE
    else:
        page = scrape.utils.utils.read(filename)
    return page


def test_get_helper():
    # page = get_page(filename='')
    # page = get_page(filename=FILE_DORMOUSE)
    pass


# Main functions
def test_get_page():
    page = get_page()
    soup = scrape.soups.get_soup(page)

    # Get page from soup
    spage = scrape.soups.get_page(soup)
    assert isinstance(spage, str)

    # Get page from tag
    atag = soup.find('a')
    tpage = scrape.soups.get_page(atag)
    assert isinstance(tpage, str)

    # Get page from ResultSet
    rtag = soup.find_all('a')
    rpage = scrape.soups.get_page(rtag)
    assert isinstance(rpage, str)


def test_get_soup():
    page = get_page()
    soup = scrape.soups.get_soup(page)
    assert isinstance(soup, bs4.BeautifulSoup)


def test_get_table_rows_success():
    # Simple example, rows
    page = get_page()
    soup = scrape.soups.get_soup(page)
    rows = ROWS_DORMOUSE
    atable, _ = scrape.soups.get_table(soup, rows=rows)
    assert len(atable) == 3

    # Example, rows
    page = get_page(filename=FILE_BOOKS)
    soup = scrape.soups.get_soup(page)
    rows = ROWS_BOOKS
    atable, _ = scrape.soups.get_table(soup, rows=rows)
    aitem = atable[0]
    assert len(atable) == ITEMS_ON_PAGE_BOOKS
    assert len(aitem) == COLUMNS_BOOKS


def test_get_table_rows_no_match():
    # Simple example, rows
    page = get_page()
    soup = scrape.soups.get_soup(page)
    rows = {"elem": "p", "class": "sister"}
    atable, _ = scrape.soups.get_table(soup, rows=rows)
    assert len(atable) == 0


def test_get_table_rows_non_dict():
    # TODO
    #     # Simple example, rows
    #     page = get_page()
    #     soup = scrape.soups.get_soup(page)
    #     rows = []
    #     atable, _ = scrape.soups.get_table(soup, rows=rows)
    #     assert len(atable) == 0
    pass


def test_get_table_rows_cols():
    # Example, rows and cols
    page = get_page(filename=FILE_BOOKS)
    soup = scrape.soups.get_soup(page)
    rows = ROWS_BOOKS
    cols = COLS_BOOKS
    atable, _ = scrape.soups.get_table(soup, rows=rows, cols=cols)
    aitem = atable[0]
    assert len(atable) == ITEMS_ON_PAGE_BOOKS
    assert len(aitem) == len(cols.keys())


def test_get_table_rows_cols_no_match():
    # Example, rows and cols
    page = get_page(filename=FILE_BOOKS)
    soup = scrape.soups.get_soup(page)
    rows = ROWS_BOOKS
    cols = COLS_BOOKS_NO_MATCH
    atable, _ = scrape.soups.get_table(soup, rows=rows, cols=cols)
    assert len(atable) == 0


def test_get_table_id_rows():
    # Example, rows
    page = get_page(filename=FILE_BOOKS)
    soup = scrape.soups.get_soup(page)
    id_ = ID_BOOKS
    rows = ROWS_BOOKS
    atable, _ = scrape.soups.get_table(soup, id_=id_, rows=rows)
    aitem = atable[0]
    assert len(atable) == ITEMS_ON_PAGE_BOOKS
    assert len(aitem) == COLUMNS_BOOKS


def test_to_table_single_row():
    # See also content tests test_get_text and test_get_subtext
    page = get_page(filename=FILE_DORMOUSE)
    soup = scrape.soups.get_soup(page)
    aitem = soup.find('a')
    atable, colnames = scrape.soups.to_table(aitem, cols={}, include_strings=True, include_hrefs=False)

    nrows = len(atable)
    assert nrows == 1
    curr_row = atable[0]
    ncols = len(curr_row)
    assert curr_row[0] == 'Elsie'
    assert ncols == len(colnames)


def test_to_table_multiple_rows():
    # See also content tests test_get_text and test_get_subtext
    page = get_page(filename=FILE_DORMOUSE)
    soup = scrape.soups.get_soup(page)
    aitem = soup.find_all('a')
    atable, colnames = scrape.soups.to_table(aitem, cols={}, include_strings=True, include_hrefs=False)

    nrows = len(atable)
    assert nrows == 3
    curr_row = atable[0]
    ncols = len(curr_row)
    assert curr_row[0] == 'Elsie'
    assert ncols == len(colnames)


def test_to_table_colnames():
    # Test column names
    page = get_page(filename=FILE_BOOKS)
    soup = scrape.soups.get_soup(page)
    rows = ROWS_BOOKS
    aitem = scrape.soups.find_items(soup, rows)
    cols = COLS_BOOKS
    atable, colnames = scrape.soups.to_table(aitem, cols=cols)
    assert isinstance(colnames, list)
    assert len(colnames) == len(cols)


# Editing functions
def test_set_base():
    page = get_page(filename=FILE_DORMOUSE)
    url = 'https://www.crummy.com/'
    bpage = scrape.soups.set_base(page, url)

    soup = scrape.soups.get_soup(bpage)
    abase = soup.find('base')
    assert abase
    assert abase["href"] == url


def test_split_soup():
    soup = scrape.soups.get_soup(get_page())
    [meta, body] = scrape.soups.split(soup)

    # Split
    assert scrape.soups.is_soup(meta)
    assert scrape.soups.is_tag(body)

    # Assert deep copy -- meta
    assert soup.title.string == meta.title.string
    meta.title.string = "meta string"
    assert soup.title.string != meta.title.string
    meta.title.string = soup.title.string

    # Assert deep copy -- body
    atag_soup = soup.find(id='link1')
    atag_body = body.find(id='link1')
    assert atag_soup.string == atag_body.string
    atag_body.string = "body string"
    assert atag_soup.string != atag_body.string
    atag_body.string = atag_soup.string


def test_merge_soup():
    soup = scrape.soups.get_soup(get_page())
    [meta, _] = scrape.soups.split(soup)

    # Merge tag with <body>
    body_new = BeautifulSoup('<body><p>Hello World</p>', 'html.parser').find("body")
    soup_new = scrape.soups.merge(meta, body_new)
    assert scrape.soups.is_soup(soup_new)
    assert str(soup_new.p) == '<p>Hello World</p>'

    # Assert deep copy
    assert soup_new.title.string == soup.title.string
    soup_new.title.string = "hello"
    assert soup_new.title.string != soup.title.string
    soup_new.title.string = soup.title.string

    # Merge tag without <body>
    body_new = BeautifulSoup('<p>Hello World</p>', 'html.parser').find("p")
    soup_new = scrape.soups.merge(meta, body_new)
    assert scrape.soups.is_soup(soup_new)
    assert str(soup_new.p) == '<p>Hello World</p>'

    # Assert deep copy
    assert soup_new.title.string == soup.title.string
    soup_new.title.string = "hello"
    assert soup_new.title.string != soup.title.string
    soup_new.title.string = soup.title.string

    # Merge ResultSet
    aset = soup.find_all('a')
    soup_new = scrape.soups.merge(meta, aset)
    assert scrape.soups.is_soup(soup_new)


# Conversion functions
def test_to_body():
    soup = scrape.soups.get_soup(get_page())
    atag = soup.find('a')

    # Assert body from tag
    abody = scrape.soups.to_body(atag)
    assert abody.name == 'body'


def test_unpack_hrefs():
    soup = scrape.soups.get_soup(get_page())
    atag = soup.find('a')

    scrape.soups.unpack_hrefs(atag)

    shref = atag["href"]
    last_tag = None
    for last_tag in atag.children:
        pass
    shref2 = str(last_tag.string)
    assert shref == shref2


def test_remove_navigable_string():
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    navstring = tag.string
    results = soup.find_all(class_="sister")
    results.append(navstring)
    len_with = len(results)
    scrape.soups.remove_navigable_string_items(results)
    len_without = len(results)
    assert len_without == len_with - 1


# I/O functions
def test_read():
    # Not needed
    pass


def test_write():
    # Not needed
    pass


# Search functions
def test_find_soup():
    soup = scrape.soups.get_soup(get_page(filename=FILE_DORMOUSE))
    afilter = ROWS_DORMOUSE
    ritem = scrape.soups.find_item(soup, afilter=afilter)
    asoup = scrape.soups.find_soup(ritem)
    assert scrape.soups.is_soup(asoup)


def test_find_items_elem_class():
    soup = scrape.soups.get_soup(get_page(filename=FILE_DORMOUSE))
    afilter = ROWS_DORMOUSE
    aresults = scrape.soups.find_items(soup, afilter)
    assert scrape.soups.is_results(aresults)


def test_find_items_elem():
    soup = scrape.soups.get_soup(get_page())
    afilter = {'elem': 'a'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    assert scrape.soups.is_results(aresults)
    assert len(aresults) == 3


def test_find_items_class():
    soup = scrape.soups.get_soup(get_page())
    afilter = {'class': 'sister'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    assert scrape.soups.is_results(aresults)
    assert len(aresults) == 3


def test_find_items_elem_string():
    soup = scrape.soups.get_soup(get_page())
    afilter = {'elem': 'a'}
    astr = 'Elsie'
    aresults = scrape.soups.find_items(soup, afilter=afilter, astr=astr)
    assert scrape.soups.is_results(aresults)
    assert len(aresults) == 1


def test_find_items_string():
    soup = scrape.soups.get_soup(get_page())
    astr = 'Elsie'
    aresults = scrape.soups.find_items(soup, astr=astr)
    assert scrape.soups.is_results(aresults)
    assert len(aresults) == 1


def test_find_items_string_regex():
    soup = scrape.soups.get_soup(get_page())
    astr = re.compile('ie')
    aresults = scrape.soups.find_items(soup, astr=astr)
    assert scrape.soups.is_results(aresults)
    assert len(aresults) == 3


def test_find_item():
    soup = scrape.soups.get_soup(get_page())

    # Elem and class
    afilter = ROWS_DORMOUSE
    ritem1 = scrape.soups.find_item(soup, afilter=afilter)
    assert scrape.soups.is_tag(ritem1)

    # Elem
    afilter = {'elem': 'a'}
    ritem2 = scrape.soups.find_item(soup, afilter=afilter)
    assert scrape.soups.is_tag(ritem2)

    # Class
    afilter = {'class': 'sister'}
    ritem3 = scrape.soups.find_item(soup, afilter=afilter)
    assert scrape.soups.is_tag(ritem3)
    assert ritem1 == ritem2 == ritem3


def test_find_item_by_xpath():
    soup = scrape.soups.get_soup(get_page(FILE_TREE))
    aitem1 = soup.find(id=ID1_TREE)

    # Absolute ===
    xpath1 = scrape.soups.xpath(aitem1)

    # Absolute find item. Exist
    fitem = scrape.soups.find_item_by_xpath(soup, axpath=xpath1, relative=False)
    assert fitem == aitem1

    # # Absolute find item. Exist. Self
    # 2022-02-12. No xpath for soup
    # xpaths = scrape.soups.xpath(soup)
    # fitem = scrape.soups.find_item_by_xpath(soup, axpath=xpaths, relative=False)
    # assert fitem == soup

    # Absolute find item. Not exist
    xpathn = xpath1 + '/b[1]'
    fitem = scrape.soups.find_item_by_xpath(soup, axpath=xpathn, relative=False)
    assert fitem is None

    # Relative ===
    achildren1 = scrape.soups.children(aitem1)
    alevel1 = achildren1[0]
    achildren2 = scrape.soups.children(alevel1)
    alevel2 = achildren2[0]
    achildren3 = scrape.soups.children(alevel2)
    alevel3 = achildren3[1]

    xpath_self = scrape.soups.xpath(aitem1, root=aitem1)
    xpath_level1 = scrape.soups.xpath(alevel1, root=aitem1)
    xpath_level3 = scrape.soups.xpath(alevel3, root=aitem1)
    xpathn = xpath_level3 + '/b[1]'

    # Relative find item. Exist 1 level deep
    fitem = scrape.soups.find_item_by_xpath(aitem1, axpath=xpath_level1, relative=True)
    assert fitem == alevel1

    # Relative find item. Exist 3 levels deep
    fitem = scrape.soups.find_item_by_xpath(aitem1, axpath=xpath_level3, relative=True)
    assert fitem == alevel3

    # Relative find item. Exist. Self
    fitem = scrape.soups.find_item_by_xpath(aitem1, axpath=xpath_self, relative=True)
    assert fitem == aitem1

    # Relative find item. Not exist
    fitem = scrape.soups.find_item_by_xpath(aitem1, axpath=xpathn, relative=True)
    assert fitem is None


def test_find_lists():
    soup = scrape.soups.get_soup(get_page(filename=FILE_WIKI))

    # All lists
    results = scrape.soups.find_lists(soup)
    alist = scrape.soups.get_strings(results)
    assert len(alist) == LISTS_NUMBER_WIKI

    # Subset of lists
    afilter = LISTS_FILTER_WIKI
    results = scrape.soups.find_lists(soup, afilter=afilter)
    alist = scrape.soups.get_strings(results)
    assert len(alist) == LISTS_FILTER_NUMBER_WIKI


def test_find_tables():
    soup = scrape.soups.get_soup(get_page(filename=FILE_WIKI))

    # All lists
    results = scrape.soups.find_tables(soup)
    alist = scrape.soups.get_strings(results)
    assert len(alist) == TABLE_NUMBER_WIKI


def test_get_filter():
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    afilter = scrape.soups.get_filter(tag)
    assert afilter['elem'] == 'a' and afilter['class'] == ['sister']


# Tree functions
def test_common_ancestor():
    soup = scrape.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = scrape.soups.find_items(soup, afilter)
    aitem1 = results[0]
    aitem2 = results[1]
    ritem = scrape.soups.common_ancestor(aitem1, aitem2)
    assert ritem.name == ROWS_PARENT_NAME_BOOKS and ritem["class"] == ROWS_PARENT_CLASS_BOOKS

    # Example same soup, parent is soup
    afilter = ROWS_BOOKS
    aitem1 = scrape.soups.find_item(soup, afilter)

    afilter = {'elem': 'title'}
    aitem2 = scrape.soups.find_item(soup, afilter)

    ritem = scrape.soups.common_ancestor(aitem1, aitem2)
    assert ritem.name == 'html' and ritem["class"] == ['no-js']

    # Different soup
    aitem2 = BeautifulSoup('<body>', 'html.parser').find("body")
    ritem = scrape.soups.common_ancestor(aitem1, aitem2)
    assert ritem is None


def test_ancestors():
    soup = scrape.soups.get_soup(get_page(FILE_BOOKS))
    afilter = ROWS_BOOKS
    results = scrape.soups.find_items(soup, afilter)
    aitem = results[0]
    ancestors = scrape.soups.ancestors(aitem)
    assert len(ancestors) == 9

    # Ancestors for copied items
    # 1. Non Copy
    ancestor_non_copy = ancestors[4]
    achildren = scrape.soups.children(ancestor_non_copy)
    achild = achildren[0]
    nancestors = scrape.soups.ancestors(achild)
    assert len(nancestors) == 5

    # 2. Copy
    ancestor_copy = copy.copy(ancestors[4])
    achildren = scrape.soups.children(ancestor_copy)
    achild = achildren[0]
    nancestors = scrape.soups.ancestors(achild)
    assert len(nancestors) == 1


def test_children():
    soup = scrape.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = scrape.soups.find_items(soup, afilter)
    aitem1 = results[0]
    aparent = aitem1.parent
    achildren = scrape.soups.children(aparent)
    assert len(achildren) == 20

    # Example same soup, exists, include_navs
    achildren = scrape.soups.children(aparent, include_navs=True)
    assert len(achildren) == 41


def test_lineage():
    soup = scrape.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = scrape.soups.find_items(soup, afilter)
    aitem1 = results[0]
    aitem2 = results[1]
    aparent = scrape.soups.common_ancestor(aitem1, aitem2)
    agrandparent = next(aparent.parents)

    # Example: ancestor is direct parent
    alineage = scrape.soups.lineage(aparent, aitem1)
    assert len(alineage) == 0

    # Example: ancestor is non-direct parent
    alineage = scrape.soups.lineage(agrandparent, aitem1)
    assert len(alineage) == 1

    # Example: no ancestor
    alineage = scrape.soups.lineage(aitem1, aitem2)
    assert len(alineage) == 0


def test_position():
    soup = scrape.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = scrape.soups.find_items(soup, afilter)
    aitem1 = results[0]

    # Include_navs = False
    idx = scrape.soups.position(aitem1)
    assert idx == 0

    # Include_navs = True
    idx = scrape.soups.position(aitem1, include_navs=True)
    assert idx == 1


# Tree extraction functions
def test_get_text():
    page = get_page()
    soup = scrape.soups.get_soup(page)
    aitem = soup.find('a')
    alist = scrape.soups.get_text(aitem, include_strings=True, include_hrefs=True)

    ncols = len(alist)
    assert ncols == 2
    assert alist[0] == 'Elsie'


def test_get_subtext():
    page = get_page(filename=FILE_BOOKS)
    soup = scrape.soups.get_soup(page)
    rows = ROWS_BOOKS
    cols = COLS_BOOKS

    results = scrape.soups.find_items(soup, rows)

    # Assert results
    alist = scrape.soups.get_subtext(results, cols=cols)

    ncols = len(alist)
    assert ncols == len(rows) * len(results)

    # Assert tag
    aitem = results[0]
    alist = scrape.soups.get_subtext(aitem, cols=cols)

    ncols = len(alist)
    assert ncols == len(rows)


def test_get_strings_from_soup():
    # Function returns a list of strings
    soup = scrape.soups.get_soup(get_page())
    alist = scrape.soups.get_strings(soup)
    assert len(alist) == 10


def test_get_strings_from_tag():
    # Function returns a list of strings
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    alist = scrape.soups.get_strings(tag)
    assert len(alist) == 1 and alist[0] == "Elsie"


def test_get_strings_from_tag_include_hrefs():
    # Function returns a list of strings
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    alist = scrape.soups.get_strings(tag, include_hrefs=True)
    assert len(alist) == 2 and alist[0] == "Elsie" and alist[1] == "http://example.com/elsie"


def test_get_strings_from_results():
    # Function returns a list of lists of strings
    soup = scrape.soups.get_soup(get_page())
    results = soup.find_all("a")
    alist = scrape.soups.get_strings(results)
    assert len(alist) == len(results) and alist[0][0] == "Elsie"


def test_get_hrefs_from_soup():
    # Function returns a list of href strings
    soup = scrape.soups.get_soup(get_page())
    alist = scrape.soups.get_hrefs(soup)
    assert len(alist) == 3 and alist[0] == 'http://example.com/elsie'


def test_get_hrefs_from_tag():
    # Function returns a single href string
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    alist = scrape.soups.get_hrefs(tag)
    assert len(alist) == 1 and alist[0] == 'http://example.com/elsie'


def test_get_hrefs_from_results():
    # Function returns a list of single href strings
    soup = scrape.soups.get_soup(get_page())
    results = soup.find_all(class_="sister")
    alist = scrape.soups.get_hrefs(results)
    assert len(alist) == len(results) and alist[0][0] == 'http://example.com/elsie'


# Stencil functions
def test_stencil():
    page = get_page(FILE_TREE)
    soup = scrape.soups.get_soup(page)
    aitem1 = soup.find(id=ID1_TREE)
    aitem2 = soup.find(id=ID2_TREE)
    amask = scrape.soups.get_mask(aitem1)

    # TODO NOT WORKING YET
    astencil = scrape.soups.stencil(aitem2, amask)
    # Check that astencil contains the same tags as amask
    pass


def test_get_mask():
    soup = scrape.soups.get_soup(get_page())

    # Tag
    afilter = ROWS_DORMOUSE
    ritem = scrape.soups.find_item(soup, afilter=afilter)
    titem = scrape.soups.get_mask(ritem)
    assert titem.string == '' and titem['href'] == ''

    # Tag with child tags
    afilter = ROWS_DORMOUSE
    titem = scrape.soups.get_mask(soup)
    ritem = scrape.soups.find_item(titem, afilter=afilter)
    assert ritem.string == '' and ritem['href'] == ''

    # Results
    afilter = ROWS_DORMOUSE
    ritem = scrape.soups.find_items(soup, afilter=afilter)
    titem = scrape.soups.get_mask(ritem)
    assert titem is None


# Identification functions
def test_is_tag():
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    results = soup.find_all(class_="sister")

    # Example TRUE
    assert scrape.soups.is_tag(tag)

    # Example FALSE
    assert not scrape.soups.is_tag(results)


def test_is_results():
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    results = soup.find_all(class_="sister")

    # Example TRUE
    assert scrape.soups.is_results(results)

    # Example FALSE
    assert not scrape.soups.is_results(tag)
    assert not scrape.soups.is_results(soup)


def test_is_soup():
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    results = soup.find_all(class_="sister")

    # Example TRUE
    assert scrape.soups.is_soup(soup)

    # Example FALSE
    assert not scrape.soups.is_soup(tag)
    assert not scrape.soups.is_soup(results)


def test_is_navigable_string():
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    navstring = tag.string
    results = soup.find_all(class_="sister")

    # Example TRUE
    assert scrape.soups.is_navigable_string(navstring)

    # Example FALSE
    assert not scrape.soups.is_navigable_string(tag)
    assert not scrape.soups.is_navigable_string(results)


# Xpath functions
def test_xpath():
    soup = scrape.soups.get_soup(get_page())

    # Test soup
    assert scrape.soups.xpath(soup) == ''

    # Test single item
    afilter = {'elem': 'b'}
    aitem1 = scrape.soups.find_item(soup, afilter=afilter)
    assert scrape.soups.xpath(aitem1) == '/html/body/p[1]/b'

    # Test multiple items
    afilter = {'elem': 'a'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    aitem1 = aresults[0]
    assert scrape.soups.xpath(aitem1) == '/html/body/p[2]/a[1]'
    aitem2 = aresults[1]
    assert scrape.soups.xpath(aitem2) == '/html/body/p[2]/a[2]'

    # test single item relative
    afilter = {'elem': 'a'}
    aitem1 = scrape.soups.find_item(soup, afilter=afilter)
    aparent = aitem1.parent
    agrandparent = aparent.parent
    # self
    assert scrape.soups.xpath(aitem1, root=aitem1) == '//'
    # parent
    assert scrape.soups.xpath(aitem1, root=aparent) == '//a[1]'
    # grandparent
    assert scrape.soups.xpath(aitem1, root=agrandparent) == '//p[2]/a[1]'

    # test first_index= True
    afilter = {'elem': 'body'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    aitem1 = aresults[0]
    assert scrape.soups.xpath(aitem1, first_index=True) == '/html[1]/body[1]'

    # test single item relative, first_index= True
    afilter = {'elem': 'body'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    aitem1 = aresults[0]
    aparent = aitem1.parent
    assert scrape.soups.xpath(aitem1, root=aparent, first_index=True) == '//body[1]'


def test_xpaths():
    soup = scrape.soups.get_soup(get_page())

    # Test soup
    alist = scrape.soups.xpaths(soup)
    assert len(alist) == 11

    # Test item
    afilter = {'elem': 'p', 'class': 'story'}
    aitem1 = scrape.soups.find_item(soup, afilter=afilter)

    # Absolute
    alist1 = scrape.soups.xpaths(aitem1)
    assert len(alist1) == 3

    # Relative
    alist2 = scrape.soups.xpaths(aitem1, root=aitem1)
    assert len(alist2) == 3


# Xpath set functions
def test_xpaths_set_union():
    soup = scrape.soups.get_soup(get_page(FILE_TREE))

    # Compare two trees
    aitem1 = soup.find(id=ID1_TREE)
    aitem2 = soup.find(id=ID2_TREE)
    ulist = scrape.soups.xpaths_set(aitem1, aitem2, operation='union', relative=True)
    assert len(ulist) == 6  # 6 Nodes


def test_xpaths_set_intersect():
    soup = scrape.soups.get_soup(get_page(FILE_TREE))

    # Compare two trees
    aitem1 = soup.find(id=ID1_TREE)
    aitem2 = soup.find(id=ID2_TREE)
    ulist = scrape.soups.xpaths_set(aitem1, aitem2, operation='intersect', relative=True)
    assert len(ulist) == 4  # 4 nodes


def test_xpaths_set_difference():
    soup = scrape.soups.get_soup(get_page(FILE_TREE))

    # Compare two trees
    aitem1 = soup.find(id=ID1_TREE)
    aitem2 = soup.find(id=ID2_TREE)
    ulist1 = scrape.soups.xpaths_set(aitem1, aitem2, operation='difference', relative=True)
    ulist2 = scrape.soups.xpaths_set(aitem2, aitem1, operation='difference', relative=True)
    assert len(ulist1) == 1  # 1 node
    assert len(ulist2) == 1  # 1 node


# Xpath private functions
def test_get_xpath_index():
    soup = scrape.soups.get_soup(get_page())

    # Test soup
    assert scrape.soups._get_xpath_index(soup) == 0

    # Test single item
    afilter = {'elem': 'b'}
    aitem1 = scrape.soups.find_item(soup, afilter=afilter)
    assert scrape.soups._get_xpath_index(aitem1) == 0

    # Test single item, first_index = True
    afilter = {'elem': 'b'}
    aitem1 = scrape.soups.find_item(soup, afilter=afilter)
    assert scrape.soups._get_xpath_index(aitem1, first_index=True) == 1

    # Test multiple items
    afilter = {'elem': 'a'}
    aresults = scrape.soups.find_items(soup, afilter=afilter)
    aitem1 = aresults[0]
    assert scrape.soups._get_xpath_index(aitem1) == 1
    aitem2 = aresults[1]
    assert scrape.soups._get_xpath_index(aitem2) == 2


def test_get_xpath_set():
    # See test_xpath_union, test_xpath_intersect, test_xpath_diff
    pass
