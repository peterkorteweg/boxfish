# config.py

"""Config is a module that contains functions for boxfish configuration"""

import os
import re
import shutil
from boxfish.data import soups
from boxfish.utils.dicts import extract_values
from boxfish.utils.utils import read_json, write_json, flip
from boxfish import utils

SEARCH_NAIVE = 'naive'
SEARCH_STENCIL = 'tree'
SEARCH_NONE = 'none'

CONFIGKEYS = ['driver', 'html', 'output']
HTMLKEYS = ['url', 'parser', 'table', 'page']
TABLEKEYS = ['id', 'rows', 'cols', 'include_strings', 'include_links']
CONFIGTABLEKEYS = TABLEKEYS + ['search']
PAGEKEYS = ['id', 'rows', 'index']
OUTPUTKEYS = ['filename', 'date_format', 'overwrite']
SEARCHTYPES = [SEARCH_NAIVE, SEARCH_STENCIL, SEARCH_NONE]

BACKUP_EXT = '.bak'

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'accept-language': 'nl,en-US;q=0.7,en;q=0.3',
           'accept-encoding': 'gzip, deflate, br'
           }


# Initialization
def create(url=''):
    """ Creates a boxfish configuration dictionary

        config = create(url)

        Args:
            url (str): Url

        Returns:
            config(dict)
    """

    config = dict.fromkeys(CONFIGKEYS, {})

    config['driver'] = utils.drivers.create_params(package='requests',
                                                   headers=HEADERS,
                                                   timeout=10,
                                                   filename='',
                                                   log='',
                                                   sleep={'1': 1, '200': 3600},
                                                   headless=True)

    config['html'] = dict.fromkeys(HTMLKEYS, {})
    config['html']['url'] = url
    config['html']['parser'] = 'html.parser'

    config['html']['table'] = dict.fromkeys(CONFIGTABLEKEYS, {})
    config['html']['table']['id'] = ''
    config['html']['table']['rows'] = dict.fromkeys(['elem', 'class'], {})
    config['html']['table']['cols'] = {}
    config['html']['table']['include_strings'] = True
    config['html']['table']['include_links'] = True
    config['html']['table']['search'] = SEARCH_NONE

    config['html']['page'] = dict.fromkeys(PAGEKEYS, {})
    config['html']['page']['id'] = ''
    config['html']['page']['rows'] = dict.fromkeys(['elem', 'class'], {})
    config['html']['page']['index'] = -1

    config['output'] = dict.fromkeys(OUTPUTKEYS, {})
    config['output']['filename'] = ''
    config['output']['date_format'] = '%Y%m%d'
    config['output']['overwrite'] = False

    return config


# I/O
def read(filename):
    """ Read a boxfish configuration from file

        config = read(filename)

        Args:
            filename (str): file name of configuration

        Returns:
            config(dict)
    """

    config = read_json(filename)
    if config is None:
        print('Cannot find' + filename)

    _process(config)
    return config


def write(filename, config):
    """ Write a boxfish configuration to file. Save current configuration to backup if exists

        write(filename, config)

        Args:
            filename (str): file name of configuration
            config (dict): configuration

        Returns:
            None

        Raises:
            IOError (): error in case function cannot write to filename
        """

    if os.path.isfile(filename):
        shutil.copy(filename, filename+BACKUP_EXT)
    write_json(filename, config)


def revert(filename):
    """ Revert a boxfish configuration file to backup.
        Flips current configuration with backup configuration if both exist
        Backup is determined by filename + BACKUP_EXT

        revert(filename)

        Args:
            filename (str): file name of configuration

        Returns:
            None

        Raises:
            IOError (): error in case function cannot write to filename
        """
    flip(filename, filename + BACKUP_EXT)


# Editing configurations
def build(config=None, url='', rows=None, cols=None, search=SEARCH_STENCIL, next_page=''):
    """ Build configuration

        config = build(config, url= '', rows=[], cols=[], search='none')

        Args:
            config (dict): configuration
            url (str): url
            rows (list): list of strings from two rows
            cols (list): list of strings from one or more columns
            search (str): column search type SEARCHTYPES
            next_page (str): url of next page

        Returns:
            config (dict): configuration

        Examples:
            # 1. Rows, no columns
            config = build(config=config, url='', rows=[rowstring1,rowstring2], search='tree')
            # 2. Columns, no rows
            config = build(config=config, url='', cols=[colstring1, colstring2], search='tree')
            # 3. Rows and columns
            config = build(config=config, url='', rows=[rowstring1,rowstring2], cols=[colstring1, colstring2], search='tree')

    """
    config = create(url) if config is None else config

    [pdriver] = utils.dicts.extract_values(config, ['driver'])
    page = utils.drivers.get_page(url=url, params=pdriver)
    soup = soups.get_soup(page)

    if soup:
        config = _build_table(soup, config, url, rows, cols, search)
        config = _build_next_page(soup, config, url, next_page)
    return config


# Private functions
def _process(config):
    """ Processes a configuration.
    The function removes non-config keys
    The function adds missing config keys with default values, two levels deep

        _process(config)

        Args:
            config (dict): configuration

        Returns:
            None
    """

    dconfig = create()

    keys = list(config.keys())
    for key in keys:
        if key not in CONFIGKEYS:
            config.pop(key)

    for key in dconfig.keys():
        if key not in config.keys():
            config[key] = dconfig[key]
        else:
            for ckey in dconfig[key]:
                if ckey not in config[key].keys():
                    config[key][ckey] = dconfig[key][ckey]


def _build_table(soup, config, url='', rows=None, cols=None, search=SEARCH_STENCIL):
    """ Build table configuration

        config = _build_table(soup, config, url= '', rows=[], cols=[], search='none')

        Args:
            soup (bs4.BeautifulSoup): A BS4 object of an HTML page
            config (dict): configuration
            url (str): url
            rows (list): list of strings from two rows
            cols (list): list of strings from one or more columns
            search (str): column search type SEARCHTYPES

        Returns:
            config (dict): configuration

    """
    rows = [] if rows is None else rows
    cols = [] if cols is None else cols
    search = SEARCH_STENCIL if search not in SEARCHTYPES else search

    tf = False

    # Website rows
    if len(rows) >= 2:
        aitem1 = soups.find_item(soup, astr=re.compile(rows[0]))
        aitem2 = soups.find_item(soup, astr=re.compile(rows[1]))
    elif len(cols) >= 2:
        aitem1 = soups.find_item(soup, astr=re.compile(cols[0]))
        aitem2 = soups.find_item(soup, astr=re.compile(cols[1]))
    else:
        aitem1 = None
        aitem2 = None

    afilter = soups.get_filter_child_of_common_ancestor(aitem1, aitem2)
    if afilter:
        config['html']['url'] = url
        config['html']['table']['rows'] = afilter
        tf = True

    # Website columns
    if tf and len(cols) > 0:
        # TODO
        # cols from dict to list
        if search == SEARCH_NONE:
            ritem = soups.find_item(soup, astr=re.compile(cols[0]))
            adict = {}
            for index, col in enumerate(cols):
                citem = soups.find_item(ritem, astr=re.compile(col))
                afilter = soups.get_filter(citem)
                adict['col' + str(index + 1)] = afilter
            config['html']['table']['cols'] = adict
        elif search == SEARCH_STENCIL:
            # TODO
            config['html']['table']['cols'] = {}
        else:
            # search == SEARCH_NAIVE:
            config['html']['table']['cols'] = {}
    return config


def _build_next_page(soup, config, url='', next_page=''):
    """ Build next page configuration

        config = _build_next_page(soup, config, url= '', next_page=None)

        Args:
            soup (bs4.BeautifulSoup): A BS4 object of an HTML page
            config (dict): configuration
            url (str): url
            next_page ()

        Returns:
            config (dict): configuration

    """
    if len(url) > 0 and len(next_page) > 0:
        citem = soups.find_item(soup, astr=re.compile(next_page))
        if citem:
            afilter = soups.get_filter(citem.parent)
            # TODO
            config['html']['table']['page']['id'] = ""
            config['html']['table']['page']['elem'] = afilter['elem']
            config['html']['table']['page']['class'] = afilter['class']
            config['html']['table']['page']['index'] = -1
    return config
