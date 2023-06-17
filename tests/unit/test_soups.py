# test_soups.py

import copy
import re

import bs4
from bs4 import BeautifulSoup

import boxfish
from boxfish.utils.utils import read

# BS4 Default example
FILE_DORMOUSE = r".\data\dormouse.html"
ROWS_DORMOUSE = {"elem": "a", "class": ["sister"]}
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
PAGE_WRAP = """<html>
<body>
    <i>Hello </i>World.
    <b>This is Pizzicato </b>Five.
</body>
</html>"""

# BS4 Tree example
FILE_TREE = r".\data\tree.html"
ID1_TREE = "tree1"
ID2_TREE = "tree2"

# BS4 Navstring example
FILE_SCRAPETHIS = r".\data\scrapethis.html"
ROWS_SCRAPETHIS = {"elem": "div", "class": ["col-md-4 country"]}


# Books to boxfish example
FILE_BOOKS = r".\data\bookstoscrape.html"
ID_BOOKS = {"elem": "body", "class": ["default"]}
ROWS_PARENT_NAME_BOOKS = "ol"
ROWS_PARENT_CLASS_BOOKS = ["row"]
ROWS_BOOKS = {"elem": "li", "class": ["col-xs-6 col-sm-4 col-md-3 col-lg-3"]}
COLS_BOOKS = [{"elem": "h3", "class": [""]}, {"elem": "p", "class": ["price_color"]}]
COLS_BOOKS_NO_MATCH = [
    {"elem": "a", "class": ["star-rating"]},
    {"elem": "a", "class": ["price_color"]},
]
ITEMS_ON_PAGE_BOOKS = 20
COLUMNS_BOOKS = 4
URL_BOOKS = "http://books.toscrape.com"

# Wikipedia lists
FILE_WIKI = r".\data\ISO3166.html"
LISTS_NUMBER_WIKI = 44

LISTS_FILTER_WIKI = {"class": ["vector-menu-content-list"]}
LISTS_FILTER_NUMBER_WIKI = 11

LISTS_FILTER_ELEM_WIKI = {"elem": "ul"}
LISTS_FILTER_ELEM_NUMBER_WIKI = 11

TABLE_NUMBER_WIKI = 2


# Helper functions
def get_page(filename=FILE_DORMOUSE):
    if filename is "":
        page = PAGE_DORMOUSE
    else:
        page = boxfish.utils.utils.read(filename)
    return page


def test_get_helper():
    # page = get_page(filename='')
    # page = get_page(filename=FILE_DORMOUSE)
    pass


# Main functions
def test_get_page():
    page = get_page()
    soup = boxfish.soups.get_soup(page)

    # Get page from soup
    spage = boxfish.soups.get_page(soup)
    assert isinstance(spage, str)

    # Get page from tag
    atag = soup.find("a")
    tpage = boxfish.soups.get_page(atag)
    assert isinstance(tpage, str)

    # Get page from ResultSet
    rtag = soup.find_all("a")
    rpage = boxfish.soups.get_page(rtag)
    assert isinstance(rpage, str)


def test_get_soup():
    page = get_page()
    soup = boxfish.soups.get_soup(page)
    assert isinstance(soup, bs4.BeautifulSoup)


def test_extract_table_rows_success():
    # Simple example, rows
    page = get_page()
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_DORMOUSE
    atable = boxfish.soups.extract_table(soup, rows=rows)
    assert len(atable) == 3

    # Example, rows
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_BOOKS
    atable = boxfish.soups.extract_table(soup, rows=rows)
    aitem = atable[0]
    assert len(atable) == ITEMS_ON_PAGE_BOOKS
    assert len(aitem) == COLUMNS_BOOKS


def test_extract_table_rows_no_match():
    # Simple example, rows
    page = get_page()
    soup = boxfish.soups.get_soup(page)
    rows = {"elem": "p", "class": "sister"}
    atable = boxfish.soups.extract_table(soup, rows=rows)
    assert len(atable) == 0


def test_extract_table_rows_non_dict():
    # TODO
    #     # Simple example, rows
    #     page = get_page()
    #     soup = boxfish.soups.get_soup(page)
    #     rows = []
    #     atable, _ = boxfish.soups.extract_table(soup, rows=rows)
    #     assert len(atable) == 0
    pass


def test_extract_table_rows_cols():
    # Example, rows and cols
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_BOOKS
    cols = COLS_BOOKS
    atable = boxfish.soups.extract_table(soup, rows=rows, cols=cols)
    aitem = atable[0]
    assert len(atable) == ITEMS_ON_PAGE_BOOKS
    assert len(aitem) == len(cols)


def test_extract_table_rows_cols_no_match():
    # Example, rows and cols
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_BOOKS
    cols = COLS_BOOKS_NO_MATCH
    atable = boxfish.soups.extract_table(soup, rows=rows, cols=cols)
    assert len(atable) == 0


def test_extract_table_id_rows():
    # Example, rows
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    id_ = ID_BOOKS
    rows = ROWS_BOOKS
    atable = boxfish.soups.extract_table(soup, id=id_, rows=rows)
    aitem = atable[0]
    assert len(atable) == ITEMS_ON_PAGE_BOOKS
    assert len(aitem) == COLUMNS_BOOKS


def test_to_table_single_row():
    # See also content tests test_get_text
    page = get_page(filename=FILE_DORMOUSE)
    soup = boxfish.soups.get_soup(page)
    aitem = soup.find("a")
    atable = boxfish.soups.to_table(aitem, include_strings=True, include_links=False)

    nrows = len(atable)
    assert nrows == 1
    curr_row = atable[0]
    ncols = len(curr_row)
    assert curr_row[0] == "Elsie"
    assert ncols == 1


def test_to_table_multiple_rows():
    # See also content tests test_get_text
    page = get_page(filename=FILE_DORMOUSE)
    soup = boxfish.soups.get_soup(page)
    aitem = soup.find_all("a")
    atable = boxfish.soups.to_table(aitem, include_strings=True, include_links=False)

    nrows = len(atable)
    assert nrows == 3
    curr_row = atable[0]
    ncols = len(curr_row)
    assert curr_row[0] == "Elsie"
    assert ncols == 1


# Editing functions
def test_set_base():
    page = get_page(filename=FILE_DORMOUSE)
    url = "https://www.crummy.com/"
    bpage = boxfish.soups.set_base(page, url)

    soup = boxfish.soups.get_soup(bpage)
    abase = soup.find("base")
    assert abase
    assert abase["href"] == url


def test_split_soup():
    soup = boxfish.soups.get_soup(get_page())
    [meta, body] = boxfish.soups.split(soup)

    # Split
    assert boxfish.soups.is_soup(meta)
    assert boxfish.soups.is_tag(body)

    # Assert deep copy -- meta
    assert soup.title.string == meta.title.string
    meta.title.string = "meta string"
    assert soup.title.string != meta.title.string
    meta.title.string = soup.title.string

    # Assert deep copy -- body
    atag_soup = soup.find(id="link1")
    atag_body = body.find(id="link1")
    assert atag_soup.string == atag_body.string
    atag_body.string = "body string"
    assert atag_soup.string != atag_body.string
    atag_body.string = atag_soup.string


def test_merge_soup():
    soup = boxfish.soups.get_soup(get_page())
    [meta, _] = boxfish.soups.split(soup)

    # Merge tag with <body>
    body_new = BeautifulSoup("<body><p>Hello World</p>", "html.parser").find("body")
    soup_new = boxfish.soups.merge(meta, body_new)
    assert boxfish.soups.is_soup(soup_new)
    assert str(soup_new.p) == "<p>Hello World</p>"

    # Assert deep copy
    assert soup_new.title.string == soup.title.string
    soup_new.title.string = "hello"
    assert soup_new.title.string != soup.title.string
    soup_new.title.string = soup.title.string

    # Merge tag without <body>
    body_new = BeautifulSoup("<p>Hello World</p>", "html.parser").find("p")
    soup_new = boxfish.soups.merge(meta, body_new)
    assert boxfish.soups.is_soup(soup_new)
    assert str(soup_new.p) == "<p>Hello World</p>"

    # Assert deep copy
    assert soup_new.title.string == soup.title.string
    soup_new.title.string = "hello"
    assert soup_new.title.string != soup.title.string
    soup_new.title.string = soup.title.string

    # Merge ResultSet
    aset = soup.find_all("a")
    soup_new = boxfish.soups.merge(meta, aset)
    assert boxfish.soups.is_soup(soup_new)


def test_set_urls():
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)

    afilter = ROWS_BOOKS
    results = boxfish.soups.find_items(soup, afilter)
    aitem = results[0]

    alink = aitem.find("a")
    asouplink = soup.find("a")

    # Case 1: relative links

    # Item
    titem = boxfish.soups.set_urls(aitem, URL_BOOKS)
    tlink = titem.find("a")
    assert tlink["href"] == URL_BOOKS + "/" + alink["href"]

    # Results
    tresults = boxfish.soups.set_urls(results, URL_BOOKS)
    assert tresults is None

    # Soup
    tsoup = boxfish.soups.set_urls(soup, URL_BOOKS)
    tsouplink = tsoup.find("a")
    assert tsouplink["href"] == URL_BOOKS + "/" + asouplink["href"]

    # Case 2: relative link with paths up
    # 'http://books.toscrape.com'
    url_current = URL_BOOKS + "/path1/path2/index.html"
    name_html = "welcome.html"

    # Current folder
    ahref = name_html
    alink["href"] = ahref
    tlink = boxfish.soups.set_urls(alink, url_current)
    assert tlink["href"] == URL_BOOKS + "/path1/path2/" + name_html

    # One folder up
    ahref = "../path3/" + name_html
    alink["href"] = ahref
    tlink = boxfish.soups.set_urls(alink, url_current)
    assert tlink["href"] == URL_BOOKS + "/path1/path3/" + name_html


# Conversion functions
def test_to_body():
    soup = boxfish.soups.get_soup(get_page())
    atag = soup.find("a")

    # Assert body from tag
    abody = boxfish.soups.to_body(atag)
    assert abody.name == "body"


def test_unpack_hrefs():
    soup = boxfish.soups.get_soup(get_page())
    atag = soup.find("a")

    boxfish.soups.unpack_hrefs(atag)

    shref = atag["href"]
    last_tag = None
    for last_tag in atag.children:
        pass
    shref2 = str(last_tag.string)
    assert shref == shref2


def test_remove_navigable_strings():
    soup = boxfish.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    navstring = tag.string
    results = soup.find_all(class_="sister")
    results.append(navstring)
    len_with = len(results)
    boxfish.soups.remove_navigable_strings(results)
    len_without = len(results)
    assert len_without == len_with - 1


def test_wrap_navigable_strings():
    soup = boxfish.soups.get_soup(get_page(filename=FILE_SCRAPETHIS))
    astring = re.compile("Antigua and Barbuda")

    # Navstring cannot be found
    tag = boxfish.soups.find_item(soup, astr=astring)
    assert tag is None

    # Navstring tag can be found
    boxfish.soups.wrap_navigable_strings(soup)
    tag = boxfish.soups.find_item(soup, astr=astring)
    assert tag is not None

    ## Example with empty strings
    soup = boxfish.soups.get_soup(PAGE_WRAP)
    astring = ""

    # Find all tags with a string
    results_tags = boxfish.soups.find_items(soup, astr=astring)
    assert len(results_tags) > 0

    # Find all wrapped strings
    boxfish.soups.wrap_navigable_strings(soup)
    results_wrapped = boxfish.soups.find_items(soup, astr=astring)
    assert len(results_wrapped) > len(results_tags)

    # Find all wrapped strings, including empty strings
    boxfish.soups.wrap_navigable_strings(soup, empty=True)
    results_wrapped_empty = boxfish.soups.find_items(soup, astr=astring)
    assert len(results_wrapped_empty) > len(results_wrapped)


# I/O functions
def test_read():
    # Not needed
    pass


def test_write():
    # Not needed
    pass


# Search functions
def test_find_soup():
    soup = boxfish.soups.get_soup(get_page(filename=FILE_DORMOUSE))
    afilter = ROWS_DORMOUSE
    ritem = boxfish.soups.find_item(soup, afilter=afilter)
    asoup = boxfish.soups.find_soup(ritem)
    assert boxfish.soups.is_soup(asoup)


def test_find_items_elem_class():
    soup = boxfish.soups.get_soup(get_page(filename=FILE_DORMOUSE))
    afilter = ROWS_DORMOUSE
    aresults = boxfish.soups.find_items(soup, afilter)
    assert boxfish.soups.is_results(aresults)


def test_find_items_elem():
    soup = boxfish.soups.get_soup(get_page())
    afilter = {"elem": "a"}
    aresults = boxfish.soups.find_items(soup, afilter=afilter)
    assert boxfish.soups.is_results(aresults)
    assert len(aresults) == 3


def test_find_items_class():
    soup = boxfish.soups.get_soup(get_page())
    afilter = {"class": ["sister"]}
    aresults = boxfish.soups.find_items(soup, afilter=afilter)
    assert boxfish.soups.is_results(aresults)
    assert len(aresults) == 3


def test_find_items_elem_string():
    soup = boxfish.soups.get_soup(get_page())
    afilter = {"elem": "a"}
    astr = "Elsie"
    aresults = boxfish.soups.find_items(soup, afilter=afilter, astr=astr)
    assert boxfish.soups.is_results(aresults)
    assert len(aresults) == 1


def test_find_items_string():
    soup = boxfish.soups.get_soup(get_page())
    astr = "Elsie"
    aresults = boxfish.soups.find_items(soup, astr=astr)
    assert boxfish.soups.is_results(aresults)
    assert len(aresults) == 1


def test_find_items_string_regex():
    soup = boxfish.soups.get_soup(get_page())
    astr = re.compile("ie")
    aresults = boxfish.soups.find_items(soup, astr=astr)
    assert boxfish.soups.is_results(aresults)
    assert len(aresults) == 3


def test_find_item():
    soup = boxfish.soups.get_soup(get_page())

    # Elem and class
    afilter = ROWS_DORMOUSE
    ritem1 = boxfish.soups.find_item(soup, afilter=afilter)
    assert boxfish.soups.is_tag(ritem1)

    # Elem
    afilter = {"elem": "a"}
    ritem2 = boxfish.soups.find_item(soup, afilter=afilter)
    assert boxfish.soups.is_tag(ritem2)

    # Class
    afilter = {"class": ["sister"]}
    ritem3 = boxfish.soups.find_item(soup, afilter=afilter)
    assert boxfish.soups.is_tag(ritem3)
    assert ritem1 == ritem2 == ritem3


def test_find_item_by_xpath():
    soup = boxfish.soups.get_soup(get_page(FILE_TREE))
    aitem1 = soup.find(id=ID1_TREE)

    # Absolute ===
    xpath1 = boxfish.soups.xpath(aitem1)

    # Absolute find item. Exist
    fitem = boxfish.soups.find_item_by_xpath(soup, axpath=xpath1, relative=False)
    assert fitem == aitem1

    # # Absolute find item. Exist. Self
    # 2022-02-12. No xpath for soup
    # xpaths = boxfish.soups.xpath(soup)
    # fitem = boxfish.soups.find_item_by_xpath(soup, axpath=xpaths, relative=False)
    # assert fitem == soup

    # Absolute find item. Not exist
    xpathn = xpath1 + "/b[1]"
    fitem = boxfish.soups.find_item_by_xpath(soup, axpath=xpathn, relative=False)
    assert fitem is None

    # Relative ===
    achildren1 = boxfish.soups.children(aitem1)
    alevel1 = achildren1[0]
    achildren2 = boxfish.soups.children(alevel1)
    alevel2 = achildren2[0]
    achildren3 = boxfish.soups.children(alevel2)
    alevel3 = achildren3[1]

    xpath_self = boxfish.soups.xpath(aitem1, root=aitem1)
    xpath_level1 = boxfish.soups.xpath(alevel1, root=aitem1)
    xpath_level3 = boxfish.soups.xpath(alevel3, root=aitem1)
    xpathn = xpath_level3 + "/b[1]"

    # Relative find item. Exist 1 level deep
    fitem = boxfish.soups.find_item_by_xpath(aitem1, axpath=xpath_level1, relative=True)
    assert fitem == alevel1

    # Relative find item. Exist 3 levels deep
    fitem = boxfish.soups.find_item_by_xpath(aitem1, axpath=xpath_level3, relative=True)
    assert fitem == alevel3

    # Relative find item. Exist. Self
    fitem = boxfish.soups.find_item_by_xpath(aitem1, axpath=xpath_self, relative=True)
    assert fitem == aitem1

    # Relative find item. Not exist
    fitem = boxfish.soups.find_item_by_xpath(aitem1, axpath=xpathn, relative=True)
    assert fitem is None


def test_find_lists():
    soup = boxfish.soups.get_soup(get_page(filename=FILE_WIKI))

    # All lists
    results = boxfish.soups.find_lists(soup)
    alist = boxfish.soups.get_strings(results)
    assert len(alist) == LISTS_NUMBER_WIKI

    # Subset of lists
    afilter = LISTS_FILTER_WIKI
    results = boxfish.soups.find_lists(soup, afilter=afilter)
    alist = boxfish.soups.get_strings(results)
    assert len(alist) == LISTS_FILTER_NUMBER_WIKI


def test_find_tables():
    soup = boxfish.soups.get_soup(get_page(filename=FILE_WIKI))

    # All lists
    results = boxfish.soups.find_tables(soup)
    alist = boxfish.soups.get_strings(results)
    assert len(alist) == TABLE_NUMBER_WIKI


def test_get_filter():
    soup = boxfish.soups.get_soup(get_page())

    # Tag with class
    tag = soup.find(id="link1")
    afilter = boxfish.soups.get_filter(tag)
    assert afilter["elem"] == "a" and afilter["class"] == ["sister"]

    # Tag without class
    tag = soup.find("b")
    afilter = boxfish.soups.get_filter(tag)
    assert afilter["elem"] == "b" and afilter["class"] == [""]


def get_filter_most_common():
    # TODO
    pass


def remove_filters():
    # TODO
    pass


# Tree functions
def test_common_ancestor():
    soup = boxfish.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = boxfish.soups.find_items(soup, afilter)
    aitem1 = results[0]
    aitem2 = results[1]
    ritem = boxfish.soups.common_ancestor(aitem1, aitem2)
    assert (
        ritem.name == ROWS_PARENT_NAME_BOOKS
        and ritem["class"] == ROWS_PARENT_CLASS_BOOKS
    )

    # Example same soup, parent is soup
    afilter = ROWS_BOOKS
    aitem1 = boxfish.soups.find_item(soup, afilter)

    afilter = {"elem": "title"}
    aitem2 = boxfish.soups.find_item(soup, afilter)

    ritem = boxfish.soups.common_ancestor(aitem1, aitem2)
    assert ritem.name == "html" and ritem["class"] == ["no-js"]

    # Different soup
    aitem2 = BeautifulSoup("<body>", "html.parser").find("body")
    ritem = boxfish.soups.common_ancestor(aitem1, aitem2)
    assert ritem is None


def test_common_ancestors():
    # TODO
    pass


def test_ancestors():
    soup = boxfish.soups.get_soup(get_page(FILE_BOOKS))
    afilter = ROWS_BOOKS
    results = boxfish.soups.find_items(soup, afilter)
    aitem = results[0]
    ancestors = boxfish.soups.ancestors(aitem)
    assert len(ancestors) == 9

    # Ancestors for copied items
    # 1. Non Copy
    ancestor_non_copy = ancestors[4]
    achildren = boxfish.soups.children(ancestor_non_copy)
    achild = achildren[0]
    nancestors = boxfish.soups.ancestors(achild)
    assert len(nancestors) == 5

    # 2. Copy
    ancestor_copy = copy.copy(ancestors[4])
    achildren = boxfish.soups.children(ancestor_copy)
    achild = achildren[0]
    nancestors = boxfish.soups.ancestors(achild)
    assert len(nancestors) == 1


def test_children():
    soup = boxfish.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = boxfish.soups.find_items(soup, afilter)
    aitem1 = results[0]
    aparent = aitem1.parent
    achildren = boxfish.soups.children(aparent)
    assert len(achildren) == 20

    # Example same soup, exists, include_navs
    achildren = boxfish.soups.children(aparent, include_navs=True)
    assert len(achildren) == 41


def test_lineage():
    soup = boxfish.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = boxfish.soups.find_items(soup, afilter)
    aitem1 = results[0]
    aitem2 = results[1]
    aparent = boxfish.soups.common_ancestor(aitem1, aitem2)
    agrandparent = next(aparent.parents)

    # Example: ancestor is direct parent
    alineage = boxfish.soups.lineage(aparent, aitem1)
    assert len(alineage) == 0

    # Example: ancestor is non-direct parent
    alineage = boxfish.soups.lineage(agrandparent, aitem1)
    assert len(alineage) == 1

    # Example: no ancestor
    alineage = boxfish.soups.lineage(aitem1, aitem2)
    assert len(alineage) == 0


def test_position():
    soup = boxfish.soups.get_soup(get_page(FILE_BOOKS))

    # Example same soup, exists
    afilter = ROWS_BOOKS
    results = boxfish.soups.find_items(soup, afilter)
    aitem1 = results[0]

    # Include_navs = False
    idx = boxfish.soups.position(aitem1)
    assert idx == 0

    # Include_navs = True
    idx = boxfish.soups.position(aitem1, include_navs=True)
    assert idx == 1


def test_get_child_of_common_ancestor():
    soup = boxfish.soups.get_soup(get_page())

    # Example child of ancestor is item
    aitem1 = soup.find(id="link1")
    aitem2 = soup.find(id="link2")
    achild = boxfish.soups.get_child_of_common_ancestor(aitem1, aitem2)
    afilter = boxfish.soups.get_filter(achild)
    assert afilter["elem"] == "a" and afilter["class"] == ["sister"]

    # Example child of ancestor is ancestor of item
    soup = boxfish.soups.get_soup(get_page(FILE_TREE))
    atree2 = soup.find(id=ID2_TREE)
    aitem1 = atree2.find(id="CT")
    aitem2 = atree2.find(id="FT")
    achild = boxfish.soups.get_child_of_common_ancestor(aitem1, aitem2)
    afilter = boxfish.soups.get_filter(achild)
    assert afilter["elem"] == "span" and afilter["class"] == [""]


def test_get_child_of_common_ancestors():
    # TODO
    pass


def get_ancestor_unique_filter():
    # TODO
    pass


def test_get_ancestors_unique_filter():
    # TODO
    pass


def test_get_parents():
    # TODO
    pass


# Tree extraction functions
def test_get_text_from_tag():
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_BOOKS

    aitem = boxfish.soups.find_item(soup, rows)
    alist = boxfish.soups.get_text(aitem, include_strings=True, include_links=False)

    assert len(alist) == 4
    assert alist[0] == "A Light in the ..."


def test_get_text_from_tag_cols():
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_BOOKS
    cols = COLS_BOOKS

    aitem = boxfish.soups.find_item(soup, rows)
    alist = boxfish.soups.get_text(
        aitem, cols=cols, include_strings=True, include_links=False
    )

    assert len(alist) == 2
    assert alist[0] == "A Light in the ..."


def test_get_text_from_tag_cols_fill_missing():
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_BOOKS
    cols = COLS_BOOKS

    aitem = boxfish.soups.find_item(soup, rows)
    # Remove item
    asubitem = boxfish.soups.find_item(aitem, cols[1])
    asubitem.decompose()

    alist = boxfish.soups.get_text(
        aitem,
        cols=cols,
        include_strings=True,
        include_links=False,
        fill_missing_cols=False,
    )
    assert len(alist) == 1
    alist = boxfish.soups.get_text(
        aitem,
        cols=cols,
        include_strings=True,
        include_links=False,
        fill_missing_cols=True,
    )
    assert len(alist) == 2


def test_get_text_from_results():
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_BOOKS

    results = boxfish.soups.find_items(soup, rows)
    alist = boxfish.soups.get_text(results, include_strings=True, include_links=False)

    nrows = len(alist)
    ncols = len(alist[0])
    assert nrows == len(results)
    assert ncols == 4
    assert isinstance(alist[0], list)
    assert alist[0][0] == "A Light in the ..."


def test_get_text_from_results_cols():
    page = get_page(filename=FILE_BOOKS)
    soup = boxfish.soups.get_soup(page)
    rows = ROWS_BOOKS
    cols = COLS_BOOKS

    results = boxfish.soups.find_items(soup, rows)
    alist = boxfish.soups.get_text(
        results, cols=cols, include_strings=True, include_links=False
    )

    nrows = len(alist)
    ncols = len(alist[0])
    assert nrows == len(results)
    assert ncols == len(cols)
    assert isinstance(alist[0], list)
    assert alist[0][0] == "A Light in the ..."


def test_get_strings_from_soup():
    # Function returns a list of strings
    soup = boxfish.soups.get_soup(get_page())
    alist = boxfish.soups.get_strings(soup)
    assert len(alist) == 10


def test_get_strings_from_tag():
    # Function returns a list of strings
    soup = boxfish.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    alist = boxfish.soups.get_strings(tag)
    assert len(alist) == 1 and alist[0] == "Elsie"


def test_get_strings_from_tag_include_links():
    # Function returns a list of strings
    soup = boxfish.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    alist = boxfish.soups.get_strings(tag, include_links=True)
    assert (
        len(alist) == 2
        and alist[0] == "Elsie"
        and alist[1] == "http://example.com/elsie"
    )


def test_get_strings_from_results():
    # Function returns a list of lists of strings
    soup = boxfish.soups.get_soup(get_page())
    results = soup.find_all("a")
    alist = boxfish.soups.get_strings(results)
    assert len(alist) == len(results)
    assert alist[0][0] == "Elsie"


def test_get_links_from_soup():
    # Function returns a list of links
    soup = boxfish.soups.get_soup(get_page())
    alist = boxfish.soups.get_links(soup)
    assert len(alist) == 3
    assert alist[0] == "http://example.com/elsie"


def test_get_links_from_tag():
    # Function returns a list of links
    soup = boxfish.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    alist = boxfish.soups.get_links(tag)
    assert len(alist) == 1
    assert alist[0] == "http://example.com/elsie"


def test_get_links_from_results():
    # Function returns a list of list of links
    soup = boxfish.soups.get_soup(get_page())
    results = soup.find_all(class_="sister")
    alist = boxfish.soups.get_links(results)
    assert len(alist) == len(results)
    assert isinstance(alist[0], list)
    assert alist[0][0] == "http://example.com/elsie"


# Stencil functions
def test_stencil():
    page = get_page(FILE_TREE)
    soup = boxfish.soups.get_soup(page)
    # aitem1 = soup.find(id=ID1_TREE)
    # aitem2 = soup.find(id=ID2_TREE)
    # amask = boxfish.soups.get_mask(aitem1)

    # TODO NOT WORKING YET
    # astencil = boxfish.soups.stencil(aitem2, amask)
    # Check that astencil contains the same tags as amask
    pass


def test_get_mask():
    soup = boxfish.soups.get_soup(get_page())

    # Tag
    afilter = ROWS_DORMOUSE
    ritem = boxfish.soups.find_item(soup, afilter=afilter)
    titem = boxfish.soups.get_mask(ritem)
    assert titem.string == "" and titem["href"] == ""

    # Tag with child tags
    afilter = ROWS_DORMOUSE
    titem = boxfish.soups.get_mask(soup)
    ritem = boxfish.soups.find_item(titem, afilter=afilter)
    assert ritem.string == "" and ritem["href"] == ""

    # Results
    afilter = ROWS_DORMOUSE
    ritem = boxfish.soups.find_items(soup, afilter=afilter)
    titem = boxfish.soups.get_mask(ritem)
    assert titem is None


# Identification functions
def test_is_tag():
    soup = boxfish.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    results = soup.find_all(class_="sister")

    # Example TRUE
    assert boxfish.soups.is_tag(tag)

    # Example FALSE
    assert not boxfish.soups.is_tag(results)


def test_is_results():
    soup = boxfish.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    results = soup.find_all(class_="sister")

    # Example TRUE
    assert boxfish.soups.is_results(results)

    # Example FALSE
    assert not boxfish.soups.is_results(tag)
    assert not boxfish.soups.is_results(soup)


def test_is_soup():
    soup = boxfish.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    results = soup.find_all(class_="sister")

    # Example TRUE
    assert boxfish.soups.is_soup(soup)

    # Example FALSE
    assert not boxfish.soups.is_soup(tag)
    assert not boxfish.soups.is_soup(results)


def test_is_navigable_string():
    soup = boxfish.soups.get_soup(get_page())
    tag = soup.find(id="link1")
    navstring = tag.string
    results = soup.find_all(class_="sister")

    # Example TRUE
    assert boxfish.soups.is_navigable_string(navstring)

    # Example FALSE
    assert not boxfish.soups.is_navigable_string(tag)
    assert not boxfish.soups.is_navigable_string(results)


def test_is_leaf():
    # TODO
    pass


def test_is_empty_filter():
    afilter = {"elem": "", "class": [""]}
    tf = boxfish.soups.is_empty_filter(afilter)
    assert tf

    afilter = {"elem": "", "class": ["o"]}
    tf = boxfish.soups.is_empty_filter(afilter)
    assert not tf

    afilter = {"elem": "o", "class": [""]}
    tf = boxfish.soups.is_empty_filter(afilter)
    assert not tf


def test_is_filter():
    afilter = {"elem": "ul", "class": ["list"]}
    tf = boxfish.soups.is_filter(afilter)
    assert tf

    afilter = {"elem": "ul"}
    tf = boxfish.soups.is_filter(afilter)
    assert not tf

    afilter = {"class": ["list"]}
    tf = boxfish.soups.is_filter(afilter)
    assert not tf


def test_is_unique_filter():
    page = get_page(filename=FILE_DORMOUSE)
    soup = boxfish.soups.get_soup(page)

    afilter = ROWS_DORMOUSE
    nonfilter = {"elem": "hello"}
    afilter_zero = {"elem": "a", "class": ["brother"]}
    afilter_one = {"elem": "p", "class": ["title"]}
    results = boxfish.soups.find_items(soup, afilter)

    aitem = soup.find("body")

    # False, filter is not a filter
    assert not boxfish.soups.is_unique_filter(nonfilter, soup)

    # False, aitem is not a tag or soup
    assert not boxfish.soups.is_unique_filter(afilter, results)

    # False, zero results
    assert not boxfish.soups.is_unique_filter(afilter_zero, soup)

    # False, multiple results
    assert not boxfish.soups.is_unique_filter(afilter, soup)

    # True, single results from soup
    assert boxfish.soups.is_unique_filter(afilter_one, soup)

    # True, single results from tag
    assert boxfish.soups.is_unique_filter(afilter_one, aitem)


# Xpath functions
def test_xpath():
    soup = boxfish.soups.get_soup(get_page())

    # Test soup
    assert boxfish.soups.xpath(soup) == ""

    # Test single item
    afilter = {"elem": "b"}
    aitem1 = boxfish.soups.find_item(soup, afilter=afilter)
    assert boxfish.soups.xpath(aitem1) == "/html/body/p[1]/b"

    # Test multiple items
    afilter = {"elem": "a"}
    aresults = boxfish.soups.find_items(soup, afilter=afilter)
    aitem1 = aresults[0]
    assert boxfish.soups.xpath(aitem1) == "/html/body/p[2]/a[1]"
    aitem2 = aresults[1]
    assert boxfish.soups.xpath(aitem2) == "/html/body/p[2]/a[2]"

    # test single item relative
    afilter = {"elem": "a"}
    aitem1 = boxfish.soups.find_item(soup, afilter=afilter)
    aparent = aitem1.parent
    agrandparent = aparent.parent
    # self
    assert boxfish.soups.xpath(aitem1, root=aitem1) == "//"
    # parent
    assert boxfish.soups.xpath(aitem1, root=aparent) == "//a[1]"
    # grandparent
    assert boxfish.soups.xpath(aitem1, root=agrandparent) == "//p[2]/a[1]"

    # test first_index= True
    afilter = {"elem": "body"}
    aresults = boxfish.soups.find_items(soup, afilter=afilter)
    aitem1 = aresults[0]
    assert boxfish.soups.xpath(aitem1, first_index=True) == "/html[1]/body[1]"

    # test single item relative, first_index= True
    afilter = {"elem": "body"}
    aresults = boxfish.soups.find_items(soup, afilter=afilter)
    aitem1 = aresults[0]
    aparent = aitem1.parent
    assert boxfish.soups.xpath(aitem1, root=aparent, first_index=True) == "//body[1]"


def test_xpaths():
    soup = boxfish.soups.get_soup(get_page())

    # Test soup
    alist = boxfish.soups.xpaths(soup)
    assert len(alist) == 11

    # Test item
    afilter = {"elem": "p", "class": ["story"]}
    aitem1 = boxfish.soups.find_item(soup, afilter=afilter)

    # Absolute
    alist1 = boxfish.soups.xpaths(aitem1)
    assert len(alist1) == 3

    # Relative
    alist2 = boxfish.soups.xpaths(aitem1, root=aitem1)
    assert len(alist2) == 3


# Xpath set functions
def test_xpaths_set_union():
    soup = boxfish.soups.get_soup(get_page(FILE_TREE))

    # Compare two trees
    aitem1 = soup.find(id=ID1_TREE)
    aitem2 = soup.find(id=ID2_TREE)
    ulist = boxfish.soups.xpaths_set(aitem1, aitem2, operation="union", relative=True)
    assert len(ulist) == 6  # 6 Nodes


def test_xpaths_set_intersect():
    soup = boxfish.soups.get_soup(get_page(FILE_TREE))

    # Compare two trees
    aitem1 = soup.find(id=ID1_TREE)
    aitem2 = soup.find(id=ID2_TREE)
    ulist = boxfish.soups.xpaths_set(
        aitem1, aitem2, operation="intersect", relative=True
    )
    assert len(ulist) == 4  # 4 nodes


def test_xpaths_set_difference():
    soup = boxfish.soups.get_soup(get_page(FILE_TREE))

    # Compare two trees
    aitem1 = soup.find(id=ID1_TREE)
    aitem2 = soup.find(id=ID2_TREE)
    ulist1 = boxfish.soups.xpaths_set(
        aitem1, aitem2, operation="difference", relative=True
    )
    ulist2 = boxfish.soups.xpaths_set(
        aitem2, aitem1, operation="difference", relative=True
    )
    assert len(ulist1) == 1  # 1 node
    assert len(ulist2) == 1  # 1 node


# Xpath private functions
def test_get_xpath_index():
    soup = boxfish.soups.get_soup(get_page())

    # Test soup
    assert boxfish.soups._get_xpath_index(soup) == 0

    # Test single item
    afilter = {"elem": "b"}
    aitem1 = boxfish.soups.find_item(soup, afilter=afilter)
    assert boxfish.soups._get_xpath_index(aitem1) == 0

    # Test single item, first_index = True
    afilter = {"elem": "b"}
    aitem1 = boxfish.soups.find_item(soup, afilter=afilter)
    assert boxfish.soups._get_xpath_index(aitem1, first_index=True) == 1

    # Test multiple items
    afilter = {"elem": "a"}
    aresults = boxfish.soups.find_items(soup, afilter=afilter)
    aitem1 = aresults[0]
    assert boxfish.soups._get_xpath_index(aitem1) == 1
    aitem2 = aresults[1]
    assert boxfish.soups._get_xpath_index(aitem2) == 2


def test_get_xpath_set():
    # See test_xpath_union, test_xpath_intersect, test_xpath_diff
    pass
