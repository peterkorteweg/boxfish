# test_soups.py
# Created 2/28/2021
# Author P. Korteweg

import bs4
from bs4 import BeautifulSoup
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
ITEMS_ON_PAGE_WIKI = 44
FILTER_WIKI = {"class": "vector-menu-content-list"}
ITEMS_ON_PAGE_FILTER_WIKI = 11
FILTER_ELEM_WIKI = {"elem": "ul"}
ITEMS_ON_PAGE_FILTER_ELEM_WIKI = 11


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


# def test_get_table_rows_non_dict():
#     # Simple example, rows
#     page = get_page()
#     soup = scrape.soups.get_soup(page)
#     rows = []
#     atable, _ = scrape.soups.get_table(soup, rows=rows)
#     assert len(atable) == 0


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


def test_set_base():
    page = get_page(filename=FILE_DORMOUSE)
    url = 'https://www.crummy.com/'
    bpage = scrape.soups.set_base(page, url)

    soup = scrape.soups.get_soup(bpage)
    abase = soup.find('base')
    assert abase
    assert abase["href"] == url


# Editing functions
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


def test_find_common_parent():
    soup = scrape.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = scrape.soups.find_items(soup, afilter)
    aitem1 = results[0]
    aitem2 = results[1]
    ritem = scrape.soups.find_common_parent(aitem1, aitem2)
    assert ritem.name == ROWS_PARENT_NAME_BOOKS and ritem["class"] == ROWS_PARENT_CLASS_BOOKS

    # Example same soup, parent is soup
    afilter = ROWS_BOOKS
    aitem1 = scrape.soups.find_item(soup, afilter)

    afilter = {'elem': 'title'}
    aitem2 = scrape.soups.find_item(soup, afilter)

    ritem = scrape.soups.find_common_parent(aitem1, aitem2)
    assert ritem.name == 'html' and ritem["class"] == ['no-js']

    # Different soup
    aitem2 = BeautifulSoup('<body>', 'html.parser').find("body")
    ritem = scrape.soups.find_common_parent(aitem1, aitem2)
    assert ritem is None


def test_find_descendants():
    soup = scrape.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = scrape.soups.find_items(soup, afilter)
    aitem1 = results[0]
    aitem2 = results[1]
    aparent = scrape.soups.find_common_parent(aitem1, aitem2)

    # Example: direct parent
    adescendants = scrape.soups.find_descendants(aparent, aitem1)
    assert len(adescendants) == 1

    # Example: non-direct parent
    agrandparent = next(aparent.parents)
    adescendants = scrape.soups.find_descendants(agrandparent, aitem1)
    assert len(adescendants) == 2

    # Example: no parent
    adescendants = scrape.soups.find_descendants(aitem1, aitem2)
    assert len(adescendants) == 0


def test_find_lists():
    soup = scrape.soups.get_soup(get_page(filename=FILE_WIKI))

    # All lists
    results = scrape.soups.find_lists(soup)
    alist = scrape.soups.get_strings(results)
    assert len(alist) == ITEMS_ON_PAGE_WIKI

    # Subset of lists
    afilter = FILTER_WIKI
    results = scrape.soups.find_lists(soup, afilter=afilter)
    alist = scrape.soups.get_strings(results)
    assert len(alist) == ITEMS_ON_PAGE_FILTER_WIKI


# Extraction functions
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


def test_get_filter():
    soup = scrape.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    afilter = scrape.soups.get_filter(tag)
    assert afilter['elem'] == 'a' and afilter['class'] == ['sister']


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
