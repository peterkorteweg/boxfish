# website.py

""" Website is a module that contains functions for extracting tables from websites. """

from boxfish.utils.dicts import extract_values
from boxfish.utils import drivers
from boxfish.utils.lists import to_csv, to_list
from boxfish.data import soups


# Main functions
def get_website(url, config):
    """ Get data from a website based on config and url

    data = get_website(url=url, config=config):

    Args:
        url (str or list):  url
        config (dict):      configuration

    Returns:
        data (list): List of rows (list) of columns (str)
    """

    [pdataset] = extract_values(config, ['dataset'])

    data = get_data(url,config)
    save(data, pdataset)

    return data


def get_data(url,config):
    """ Get a list with data from url

    data = get_data(url, config)

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
            data = _get_data_from_driver(url, config, adriver)
            if data:
                ncols = len(data[0])
                colnames = ['Col' + str(i + 1) for i in range(ncols)]
        finally:
            drivers.driver_stop(adriver)
    data = colnames + data
    return data


# Beautiful Soup functions
def get_table(page, website):
    """ Retrieve table from an HTML page

        atable = get_table(page, website)

        Args:
            page(str): HTML text
            website(dict): Parameters with keys {'id','rows','cols'}

        Returns:
            atable (list): List of rows (list) of columns (str)
    """

    atable = []

    if page:
        soup = soups.get_soup(page)
        if soup:
            [id_, rows, cols] = extract_values(website, ['id', 'rows', 'cols'])
            atable =  soups.get_table(soup, id = id_, rows = rows, cols = cols)
    return atable


def get_url_next_page(page, params, base_url):
    """ ...

        url_next = get_url_next_page(page,website,url)

        Args:
            page(str): HTML text
            params(dict): Parameter with keys {'id','elem','class'}
            base_url(str): Url base

        Returns:
            url (str)
    """
    return ''


# File functions
def save(data, fileconfig):
    """ Saves data to file

        save(data, fileconfig)

        Args:
            data(dataframe or list): Data from HTML
            fileconfig(dict): Parameter with keys {'filename','date_format','replace'}

        Returns:
            None
    """
    lists.to_csv(data, fileconfig['filename'], \
                        date_format=fileconfig['date_format'], \
                        overwrite=fileconfig['overwrite'])

#Private functions
def _get_data_from_driver(url, config, adriver):
    """ Get a list with data from url

    data = _get_data_from_driver(url, config, adriver)

    Args:
        url (str or list):  url
        config (dict):      configuration
        adriver (driver):   driver

    Returns:
        data (list): List of rows (list) of columns (str)
    """
    data = []

    # Extract parameters
    [pwebsite] = extract_values(config, ['website'])
    [ppage] = extract_values(pwebsite, ['page'])

    i_request = 0
    for url_i in to_list(url):
        url_next = url_i
        while url_next != '':
            page = drivers.request_page(adriver, url=url_next, count=i_request)
            i_request = i_request + 1

            table = get_table(page, pwebsite)
            data.extend(table)

            url_next = get_url_next_page(page, ppage, url_i)
    return data