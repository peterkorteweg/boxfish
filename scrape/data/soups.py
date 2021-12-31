# soups.py
# Created 1/24/2021
# Author P. Korteweg

"""Soups is a module that contains functions for the Beautiful Soup library.

Objects
soup (bs4.BeautifulSoup): A BS4 object of an HTML page
tag  (bs4.element.Tag): A BS4 object of part of an HTML page
ResultSet (): A BS4 object of parts of an HTML page

aitem : soup or tag or ResultSet object
aitems: ResultSet object
atable (list): List of rows (list) of columns (str)

"""

import bs4
from bs4 import BeautifulSoup
import copy
from scrape.utils.dicts import extract_values
from scrape.utils.lists import is_empty
from scrape.utils.strings import replace_newlines
from scrape.utils.utils import read as _read, write as _write


def get_page(aitem):
    """ Get page from soup, tag or ResultSet object

    page = get_page(bitem)

    Args:
        aitem : soup or tag or ResultSet object

    Returns:

        page (str): HTML page
    """

    page = None
    if aitem is not None:
        if is_tag(aitem) or is_soup(aitem):
            page = aitem.decode()
        elif is_results(aitem):
            alist = [atag.decode() for atag in aitem]
            page = "\n".join(alist)
    return page


def get_soup(page):
    """ Get soup object from page

    soup = get_soup(page)

    Args:
        page (str): HTML page or an open file handle

    Returns:
        soup (bs4.BeautifulSoup): A BS4 object of an HTML page
    """

    if page is not None:
        soup = BeautifulSoup(page, 'lxml')
    else:
        soup = None
    return soup


def get_table(soup, **kwargs):
    """ Get table from soup

    [atable, colnames] = get_table(soup, id = "id", rows = rows, cols = cols)

    Args:
        soup (bs4.BeautifulSoup): A BS4 object of an HTML page
        **kwargs:
        id (str, optional): Identifier of subset of soup
        rows (dict): {'elem','class'}
        cols (dict): dict of dict with keys {'elem','class','href' (optional)}

    Returns:
        atable (list): List of rows (list) of columns (str)
        colnames (list): Column names
    """

    [id_, rows, cols] = extract_values(kwargs, ['id', 'rows', 'cols'])
    atable = []
    colnames = []

    # TODO Raise exception if parameters are not available
    if all(val is not None for val in [soup, rows]):

        new_soup = soup.find(id=id_) if id_ else None
        soup = new_soup if new_soup else soup

        results = find_items(soup, rows)
        [atable, colnames] = to_table(results, cols)
    return atable, colnames


def to_table(aitem, cols=None, include_strings=True, include_hrefs=False):
    """ Convert aitem to a table

    [atable, colnames] = to_table(aitem, cols=None, include_strings=True, include_hrefs=False)

    Args:
        aitem(tag or ResultSet): BS4 object
        # Extract subset of strings
        cols (dict): list of dict with keys {'elem','class','href' (optional)} or None
        # Extract all strings
        include_strings (boolean): Include hrefs as strings if true
        include_hrefs (boolean): Include hrefs as strings if true
    Returns:
        atable (list): List of rows (list) of columns (str)
        acolnames (list): Column names
    """
    atable = []
    if not is_results(aitem):
        aitem = [aitem]

    # Data
    for record in aitem:
        if cols is None or not cols:
            # Extract all strings
            row = get_text(record, include_strings=include_strings, include_hrefs=include_hrefs)
        else:
            # Extract subset of strings
            row = get_subtext(record, cols)

        if not is_empty(row):
            atable.append(row)

    # Column names
    if cols is None or not cols:
        aitem = atable[0] if atable else None
        acolnames = ['Col' + str(i+1) for i in range(len(aitem))] if aitem else []
    else:
        acolnames = list(cols.keys())
    return atable, acolnames


def set_base(page, url):
    """ Set <base> in page with url

    [bpage] = set_base(page, url)

    Args:
        page (str): HTML page
        url (str): URL link

    Returns:
        bpage (str): HTML page with <base>

    """
    asoup = get_soup(page)

    # Set base
    abase = asoup.find('base')
    if not abase:
        abase = asoup.new_tag('base')
    abase["href"] = url

    # Add base to head
    ahead = asoup.find('head')
    if not ahead:
        ahead = asoup.new_tag('head')
        asoup.append(ahead)
    ahead.append(abase)

    bpage = get_page(asoup)
    return bpage


# Editing functions - deep copy
def split(soup):
    """ Split HTML soup into objects meta and body. Meta and body are deep copies.

    [meta, body] = split(soup)

    Args:
        soup (bs4.BeautifulSoup): A BS4 object of an HTML page with <html> tag

    Returns:
        meta (bs4.BeautifulSoup): Contains HTML outside <body> plus empty body
        body (bs4.element.Tag): Contains HTML inside <body>

    """
    meta = None
    body = None

    if soup is not None and soup.html is not None:
        meta = copy.copy(soup)
        body = meta.find("body")
        if body is None:
            body = BeautifulSoup('<body>', 'html.parser').find("body")
        else:
            body.extract()
        meta.html.append(BeautifulSoup('<body>', 'html.parser').find("body"))
    return meta, body


def merge(meta, body):
    """ Merge HTML meta and body into a soup object. Soup contains deep copies of meta and body

    [soup] = merge(meta, body)

    Args:
        meta (bs4.BeautifulSoup): Contains HTML outside <body> plus empty body
        body (tag or ResultSet): Contains HTML inside <body>

    Returns:
        soup (bs4.BeautifulSoup): A BS4 object of an HTML page with <html> tag

    """
    if meta is not None and body is not None:
        # Create body with <body>
        body = to_body(body)

        # Meta
        soup = copy.copy(meta)
        # Extract current body
        body_curr = soup.find("body")
        if body_curr is not None:
            body_curr.extract()

        # Insert new body
        body_new = copy.copy(body)
        soup.html.append(body_new)
    else:
        soup = None
    return soup


# Conversion functions
def to_body(aitem):
    """ Convert aitem to tag with <body>

    body = to_body(aitem)

    Args:
        aitem(tag or ResultSet): BS4 object

    Returns:
        body (tag): tag with a <body>
    """
    if is_tag(aitem):
        if aitem.name == 'body':
            body = aitem
        else:
            temp = BeautifulSoup('<body>', 'html.parser').find("body")
            temp.append(aitem)
            body = temp
    elif is_results(aitem):
        temp = BeautifulSoup('<body>', 'html.parser').find("body")
        for btag in aitem:
            temp.append(btag)
        body = temp
    else:
        body = None
    return body


def unpack_hrefs(tag):
    """ Unpacks the href links from all a tags, and append the links as a string tag
        The function changes the existing tag

        Args:
            tag (tag): BS4 tag

        Returns:
        """
    results = tag.find_all('a')
    results.append(tag)

    for atag in results:
        if 'href' in atag.attrs:
            astr = '<p>' + str(atag["href"]) + '</p>'
            htag = BeautifulSoup(astr, 'html.parser').find("p")
            atag.append(htag)


def remove_navigable_string_items(results):
    """ Remove navigable string items from ResultSet
    The function removes list item of type Navigable String.
    Tag items which contain Nagigable Strings are not rremoved.

    results = remove_navigable_string_items(results)

    Args:
        results (ResultSet): BS4 ResultSet

    Returns:
        results (ResultSet): BS4 ResultSet
    """
    for aitem in reversed(results):
        if is_navigable_string(aitem):
            results.remove(aitem)
    return results


# I/O functions
def read(filename):
    """ Read page from file

        page = read(filename)

        Args:
            filename (str): file name of HTML page

        Returns:
            page(str)
    """

    page = _read(filename)
    return page


def write(filename, page):
    """ Write HTML page to file

            write(filename, page)

            Args:
                filename (str): file name
                page (str): HTML page

            Returns:
                None

            Raises:
                IOError (): error in case function cannot write to filename
        """

    _write(filename, page)


# Search functions
def find_items(aitem, afilter=None, astr=''):
    """ Find items from atag based on filter and/or string

    ritems = find_items(aitems, filter=afilter, astr='')

    Args:
        aitem(soup or tag or ResultSet): BS4 object
        afilter (dict): BS4 filter on keys "elem" and "class"
        astr (str): string or regular expressiom for filter on aitem.string

    Returns:
        ritems (ResultSet): BS4 resultset
    """

    # if not isinstance(afilter, dict):
    # TODO Raise error

    afilter = {} if afilter is None else afilter
    has_item = "elem" in afilter
    has_class = "class" in afilter

    if has_item and has_class:
        ritems = aitem.find_all(afilter["elem"], class_=afilter["class"], string=astr)
    elif has_item and not has_class:
        ritems = aitem.find_all(afilter["elem"], string=astr)
    elif not has_item and has_class:
        ritems = aitem.find_all(class_=afilter["class"], string=astr)
    else:
        ritems = aitem.find_all(True, string=astr)
    return ritems


def find_item(aitem, afilter=None, astr=''):
    """ Find single item from atag based on filter and/or string

    ritem = find_item(aitems, filter=afilter, astr='')

    Args:
        aitem(soup or tag or ResultSet): BS4 object
        afilter (dict): Keys "elem" and "class"
        astr (str): string or regular expressiom for filter on aitem.string

    Returns:
        ritem (tag): BS4 tag
    """

    # if not isinstance(afilter, dict):
    # TODO Raise error

    afilter = {} if afilter is None else afilter
    has_item = "elem" in afilter
    has_class = "class" in afilter

    if has_item and has_class:
        ritem = aitem.find(afilter["elem"], class_=afilter["class"], string=astr)
    elif has_item and not has_class:
        ritem = aitem.find(afilter["elem"], string=astr)
    elif not has_item and has_class:
        ritem = aitem.find(class_=afilter["class"], string=astr)
    else:
        ritem = aitem.find(True, string=astr)
    return ritem


def find_common_parent(aitem1, aitem2):
    """ Find parent tag whose descendants contain both str1 and str2

    ritem = find_item(asoup, aitem1, aitem2)

    Args:
        aitem1 (tag): BS4 tag
        aitem2 (tag): BS4 tag

    Returns:
        ritem (tag): BS4 tag
    """
    # TODO
    aitem = None
    if is_tag(aitem1) and is_tag(aitem2):
        parents1 = [parent for parent in reversed(list(aitem1.parents))]
        parents2 = [parent for parent in reversed(list(aitem2.parents))]
        for p1, p2 in zip(parents1, parents2):
            if p1 == p2:
                aitem = p1
    return aitem


def find_descendants(aparent, adescendant):
    """ Finds all descendants from aparent up to adescendant
    Returns an ordered list of descendants

    rlist = find_descendants(aparent, adescendant)

    Args:
        aparent (tag): BS4 tag
        adescendant (tag): BS4 tag

    Returns:
        rlist (list): List of BS4 tag
    """
    rlist = [parent for parent in reversed(list(adescendant.parents))]
    tf = False
    while not tf and len(rlist) > 0:
        curr_parent = rlist.pop(0)
        tf = (curr_parent == aparent)
    if tf:
        rlist.append(adescendant)
    return rlist


def find_lists(aitem, afilter=None, astr=''):
    """ Find all lists in aitem. Lists are defined as HTML elements <dl>, <ol>, or <ul>

    ritems = find_lists(aitems)

    Args:
        aitem(soup or tag or ResultSet): BS4 object
        afilter (dict): Keys "elem" and "class"
        astr (str): string or regular expressiom for filter on aitem.string

    Returns:
        ritems (ResultSet): BS4 resultset
    """

    afilter = {} if afilter is None else afilter
    afilter.update({"elem": ["dl", "ol", "ul"]})
    ritems = find_items(aitem, afilter=afilter, astr=astr)
    return ritems


def find_tables(aitem, afilter=None, astr=''):
    """ Find all tables in aitem. Tables are defined as HTML elements <table>

    ritems = find_tables(aitems)

    Args:
        aitem(soup or tag or ResultSet): BS4 object
        afilter (dict): Keys "elem" and "class"
        astr (str): string or regular expressiom for filter on aitem.string

    Returns:
        ritems (ResultSet): BS4 resultset
    """

    afilter = {} if afilter is None else afilter
    afilter.update({"elem": ["table"]})
    ritems = find_items(aitem, afilter=afilter, astr=astr)
    return ritems


# Extraction functions
def get_text(aitem, include_strings=True, include_hrefs=False):
    """ Get text from soup objects. Text consists of strings and/or hrefs.

    alist = get_text(aitem)

    Args:
        aitem(soup or tag or ResultSet): BS4 object
        include_strings (boolean): Include hrefs as strings if true
        include_hrefs (boolean): Include hrefs as strings if true

    Returns:
        alist (list): alist (list): List of strings
    """
    alist = []
    if include_strings:
        alist = get_strings(aitem, include_hrefs=include_hrefs)
    elif not include_strings and include_hrefs:
        alist = get_hrefs(aitem)
    return alist


def get_subtext(aitem, cols):
    """ Get text from soup objects. Text consists of strings and/or hrefs. Relevant
    text is specified by cols

    alist = get_text(aitem, cols)

    Args:
        aitem(soup or tag or ResultSet): BS4 object
        cols (dict): list of dict with keys {'elem','class','href' (optional)}

    Returns:
        alist (list): alist (list): List of strings
    """
    row = []

    if not is_results(aitem):
        aitem = [aitem]

    for record in aitem:
        for val in cols.values():
            atag = find_item(record, val)
            if atag is None:
                value = ''
            else:
                value = replace_newlines(atag.text.strip())
                if 'href' in val:
                    htag = atag.find('a', href=True)
                    if htag is not None:
                        value = htag['href']
            row.append(value)
    return row


def get_strings(aitem, include_hrefs=False):
    """ Get strings from soup objects

    alist = get_strings(aitem)

    Args:
        aitem(soup or tag or ResultSet): BS4 object
        include_hrefs (boolean): Include hrefs as strings if true

    Returns:
        alist (list): List of strings
    """
    alist = []
    if is_tag(aitem):
        alist = _get_strings_from_tag(aitem, include_hrefs)
    elif is_results(aitem):
        alist = _get_strings_from_results(aitem, include_hrefs)
    return alist


def get_hrefs(aitem):
    """ Get hrefs from soup objects

    alist = get_hrefs(aitem)

    Args:
        aitem(soup or tag or ResultSet): BS4 object

    Returns:
        alist (list): List of strings
    """
    alist = []
    if is_tag(aitem) or is_soup(aitem):
        alist = _get_hrefs_from_tag(aitem)
    elif is_results(aitem):
        alist = _get_hrefs_from_results(aitem)
    return alist


def get_filter(aitem):
    """ Get filter for aitem

    afilter = get_filter(aitem)

    Args:
        aitem(tag): BS4 object

    Returns:
        afilter (dict): dict with keys 'elem' and 'class_'
    """
    afilter = {'elem': '', 'class': ''}
    if is_tag(aitem):
        afilter['elem'] = aitem.name
        afilter['class'] = aitem['class']
    return afilter


# Identification functions
def is_tag(aitem):
    """ Returns true if aitem is bs4.element.Tag

    tf = is_tag(aitem)

    Args:
        aitem(soup or tag or ResultSet): BS4 object

    Returns:
        tf (bool): True if aitem is BS4 tag, False otherwise
    """
    return isinstance(aitem, bs4.element.Tag)


def is_results(aitem):
    """ Returns true if aitem is bs4.element.ResultSet

    tf = is_results(aitem)

    Args:
        aitem(soup or tag or ResultSet): BS4 object

    Returns:
        tf (bool): True if aitem is BS4 Resultset, False otherwise
    """
    return isinstance(aitem, bs4.element.ResultSet)


def is_soup(aitem):
    """ Returns true if aitem is bs4.BeautifulSoup

    tf = is_soup(aitem)

    Args:
        aitem(soup or tag or ResultSet): BS4 object

    Returns:
        tf (bool): True if aitem is BS4 soup, False otherwise
    """
    return isinstance(aitem, bs4.BeautifulSoup)


def is_navigable_string(aitem):
    """ Returns true if aitem is BS4 NavigableString

    tf = is_naviagble_string(aitem)

    Args:
        aitem: BS4 object

    Returns:
        tf (bool): True if aitem is BS4 Navigable String, False otherwise
    """
    return isinstance(aitem, bs4.element.NavigableString)


# Private functions
def _get_strings_from_results(results, include_hrefs=False):
    """ Get strings from results

    alist = _get_strings_from_results(results)

    Args:
        results (ResultSet): BS4 result set
        include_hrefs (boolean): Include hrefs as strings if true

    Returns:
        alist (list): List of strings
    """
    return [_get_strings_from_tag(tag, include_hrefs) for tag in results]


def _get_hrefs_from_results(results):
    """ Get strings with hrefs from results

    alist = _get_hrefs_from_results(results)

    Args:
        results (ResultSet): BS4 result set

    Returns:
        alist (list): List of href strings
    """
    return [_get_hrefs_from_tag(tag) for tag in results]


# Tag functions
def _get_strings_from_tag(tag, include_hrefs=False):
    """ Get strings from tag

    alist = _get_strings_from_tag(tag)

    Args:
        tag (tag): BS4 tag
        include_hrefs (boolean): Include hrefs as strings if true

    Returns:
        alist (list): List of strings
    """
    if include_hrefs:
        atag = copy.copy(tag)
        unpack_hrefs(atag)
    else:
        atag = tag
    return [text for text in atag.stripped_strings]


def _get_hrefs_from_tag(tag):
    """ Get href strings from tag

    alist = _get_hrefs_from_tag(tag)

    Args:
        tag (tag): BS4 tag

    Returns:
        alist (list): List of href strings
    """
    results = tag.find_all('a')
    results.append(tag)
    alist = [tag['href'] if 'href' in tag.attrs else None for tag in results]
    alist = list(filter(None, alist))
    return alist
