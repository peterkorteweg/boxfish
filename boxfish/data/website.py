# website.py

""" Website is a module that contains functions for extracting tables from websites. """

from boxfish.data import config
from boxfish.data import soups
from boxfish.utils.dicts import extract_values, get_subset
from boxfish.utils import drivers, urls
from boxfish.utils.lists import flatten, to_csv, to_list



# Main functions
def extract(url, config):
    """ Get data from a website based on config and url

    data = extract(url=url, config=config):

    Args:
        url (str or list):  url
        config (dict):      configuration

    Returns:
        data (list): List of rows (list) of columns (str)
    """

    [poutput] = extract_values(config, ['output'])
    data = extract_data(url,config)
    save(data, poutput)

    return data


def extract_data(url,config):
    """ Extract data from url to list

    data = extract_data(url, config)

    Args:
        url (str or list):  url
        config (dict):      configuration

    Returns:
        data (list): List of rows (list) of columns (str)
    """

    data = []
    colnames = []

    if url and config:
        adriver = drivers.driver_start(config['driver'])
        try:
            data = _extract_data_from_driver(url, config, adriver)
            # Column headers
            if data:
                ncols = len(data[0])
                colnames = ['col' + str(i + 1) for i in range(ncols)]
                data.insert(0, colnames)
        finally:
            drivers.driver_stop(adriver)

    return data


# Beautiful Soup functions
def extract_table(page, ptable):
    """ Extract table from an HTML page

        atable = extract_table(page, ptable)

        Args:
            page(str): HTML text
            ptable(dict): Table parameters with keys config.TABLEKEYS

        Returns:
            atable (list): List of rows (list) of columns (str)
    """

    atable = []

    if page:
        soup = soups.get_soup(page)
        if soup:
            pparams = get_subset(ptable, config.TABLEKEYS)
            atable = soups.extract_table(soup, **pparams)
    return atable


def extract_url_next_page(page, pnext_page, url):
    """ Extract url that refers to next page

        url_next = extract_url_next_page(page,pnext_page,url)

        Args:
            page(str): HTML text
            next_page(dict): Next page parameters with keys config.PAGEKEYS
            url(str): Url current page

        Returns:
            url_next_page (str): Url next page
    """
    url_next_page = ''
    [index] = extract_values(pnext_page, ['index'])
    index = index if index else -1

    pnext_page['include_strings'] = False
    pnext_page['include_links'] = True

    alinks = extract_table(page, pnext_page)
    if alinks:
        alinks = flatten(alinks)
        url_next_page = urls.replace_subpath(url,alinks[index],-1)
    return  url_next_page


# File functions
def save(data, fileconfig):
    """ Save data to CSV file

        save(data, fileconfig)

        Args:
            data(dataframe or list): Data from HTML
            fileconfig(dict): Parameter with keys {'filename','date_format','replace'}

        Returns:
            None
    """
    to_csv(data, fileconfig['filename'],
             date_format=fileconfig['date_format'],
             overwrite=fileconfig['overwrite'],
             quoting=fileconfig['quoting'])

# Private functions
def _extract_data_from_driver(url, config, adriver):
    """ Extract data from url to list

    data = _extract_data_from_driver(url, config, adriver)

    Args:
        url (str or list):  url
        config (dict):      configuration
        adriver (driver):   driver

    Returns:
        data (list): List of rows (list) of columns (str)
    """
    data = []

    # Extract parameters
    [phtml] = extract_values(config, ['html'])
    [ptable] = extract_values(phtml, ['table'])
    [ppage] = extract_values(phtml, ['page'])

    i_request = 0
    for url_i in to_list(url):
        url_next = url_i
        url_pre = ['']
        while url_next not in url_pre:
            page = drivers.request_page(adriver, url=url_next, count=i_request)
            i_request = i_request + 1

            table = extract_table(page, ptable)
            data.extend(table)

            url_pre.append(url_next)
            url_next = extract_url_next_page(page, ppage, url_next)
    return data