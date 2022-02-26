# website.py

""" Website is a module that contains functions for extracting tables from websites. """

from boxfish.utils import dataframes
from boxfish.utils.dicts import extract_values
from boxfish.utils import drivers
from boxfish.utils.lists import to_list
from boxfish.data import soups


# Main functions
def get_website(url, config):
    """ Get data from a website based on config and url

    df = get_website(url=url, config=config):

    Args:
        url (str or list):  url
        config (dict):      configuration

    Returns:
        df (Pandas Dataframe): Dataframe from website
    """

    [pdataset] = extract_values(config, ['dataset'])

    data, colnames = get_data(url,config)
    df = dataframes.list_to_dataframe(data,colnames)
    save(df, pdataset)

    return df


def get_data(url,config):
    """ Get a list with data from url

    data, colnames = get_data(url, config)

    Args:
        url (str or list):  url
        config (dict):      configuration

    Returns:
        data (list): List of rows (list) of columns (str)
        colnames (list): Column names
    """

    data = []
    colnames = []

    #TODO exception handling
    if url and config:
        adriver = drivers.driver_start(config['driver'])
        try:
            data, colnames = _get_data_from_driver(url, config, adriver)
        finally:
            drivers.driver_stop(adriver)
    return data, colnames


# Beautiful Soup functions
def get_table(page, website):
    """ Retrieve table from an HTML page

        atable = get_table(page, website)

        Args:
            page(str): HTML text
            website(dict): Parameters with keys {'id','rows','columns'}

        Returns:
            atable (list): List of rows (list) of columns (str)
            colnames (list): Column names
    """

    atable = []
    colnames = []

    if page:
        soup = soups.get_soup(page)
        if soup:
            [id_, rows, cols] = extract_values(website, ['id', 'rows', 'cols'])
            [atable, colnames] =  soups.get_table(soup, id = id_, rows = rows, cols = cols)
    return atable, colnames


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

#     links = process_page_links(page, params)
#     if links is not None:
#         url_next = links[0]
#     else:
#         url_next = ''
#
#     if url_next != '':
#         path_next = urls.get_path(url_next)
#         query_next = urls.get_query(url_next)
#         # Logging
#         # print('url_next ' + url_next)
#         # print('path_next')
#         # print(path_next)
#         # print('query_next')
#         # print(query_next)
#         url_next = urls.create_from_parts(url=base_url,
#                                                 path=path_next,
#                                                 query=query_next,
#                                                 remove_existing_path=True,
#                                                 remove_existing_query=False)
#
#     return url_next

# def process_page_links(page, params):
#     """ ???
#
#         links = process_links(page, website)
#
#         Args:
#             page(str): HTML text
#             params(dict): Parameter with keys {'id','elem','class'}
#
#         Returns:
#             links (???)
#     """
#
#     soup = soups.get_soup(page)
#     tag = soup.find(id=params['id'])
#
#     elem =  params['elem']
#     class_ = params['class']
#
#     if not elem is None:
#         if class_ is None:
#             results = tag.find_all(elem)
#         else:
#             results = tag.find_all(elem, class_= class_)
#     else:
#         results = tag
#
#     links = soups.get_hrefs(results)
#     return links


# File functions
def save(df, fileconfig):
    """ Saves a dataframe to file

        save(df, fileconfig)

        Args:
            df(dataframe): HTML text
            fileconfig(dict): Parameter with keys {'filename','date_format','replace'}

        Returns:
            None
    """
    dataframes.save(df, fileconfig['filename'], \
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
        colnames (list): Column names
    """
    data = []
    colnames = []
    # Extract parameters
    [pwebsite] = extract_values(config, ['website'])
    [ppage] = extract_values(pwebsite, ['page'])

    i_request = 0
    for url_i in to_list(url):
        url_next = url_i
        while url_next != '':
            page = drivers.request_page(adriver, url=url_next, count=i_request)
            i_request = i_request + 1

            table, colnames = get_table(page, pwebsite)
            data.extend(table)

            url_next = get_url_next_page(page, ppage, url_i)
    return data, colnames