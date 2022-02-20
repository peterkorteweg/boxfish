# config.py

"""Config is a module that contains functions for scrape configuration"""

import os
import re
import shutil
from scrape.data import soups
from scrape.utils.dicts import extract_values
from scrape.utils.utils import read_json, write_json, flip
from scrape import utils

SEARCH_STENCIL = 'tree'
SEARCH_STRIPPED_STRINGS = 'naive'
SEARCH_EXACT_COLUMNS = 'none'

CONFIGKEYS = ['driver', 'website', 'dataset']
WEBSITEKEYS = ['url', 'parser', 'id', 'rows', 'columns', 'page']
DATASETKEYS = ['filename', 'date_format', 'overwrite']
SEARCHTYPES = [SEARCH_STENCIL, SEARCH_STRIPPED_STRINGS, SEARCH_EXACT_COLUMNS]

BACKUP_EXT = '.bak'

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'accept-language': 'nl,en-US;q=0.7,en;q=0.3',
           'accept-encoding': 'gzip, deflate, br'
           }


# Initialization
def create(url=''):
    """ Creates a scrape configuration dictionary

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

    config['website'] = dict.fromkeys(WEBSITEKEYS, {})
    config['website']['url'] = url
    config['website']['parser'] = 'html.parser'
    config['website']['id'] = ''
    config['website']['rows'] = dict.fromkeys(['elem', 'class'], {})
    config['website']['columns'] = {}
    config['website']['page'] = dict.fromkeys(['id', 'elem', 'class'], {})

    config['dataset'] = dict.fromkeys(DATASETKEYS, {})
    config['dataset']['filename'] = ''
    config['dataset']['date_format'] = '%Y%m%d'
    config['dataset']['overwrite'] = False

    return config


# I/O
def read(filename):
    """ Read a scrape configuration from file

        config = read(filename)

        Args:
            filename (str): file name of configuration

        Returns:
            config(dict)
    """

    config = read_json(filename)
    if config is None:
        print('Cannot find' + filename)

    process(config)
    return config


def write(filename, config):
    """ Write a scrape configuration to file. Save current configuration to backup if exists

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
    """ Revert a scrape configuration file to backup.
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
def process(config):
    """ Processes a configuration.
    The function removes non-config keys
    The function adds missing config keys with default values, two levels deep

        process(config)

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


def build(config, url='', rows=None, cols=None, search=SEARCH_STENCIL):
    """ Build configuration
        Function builds website configuration.

        tf = build(config, url= '', rows=[], cols=[], search='none')

        Args:
            config (dict): configuration
            url (str): url
            rows (list): list of strings from two rows
            cols (list): list of strings from one or more columns
            search (str): column search type SEARCHTYPES

        Returns:
            tf (bool): true if config is updated false otherwise

        Examples:
            # 1. Rows, no columns
            tf = build(config, url= '', rows=[rowstring1,rowstring2], search='tree')
            # 2. Columns, no rows
            tf = build(config, url= '', cols=[colstring1, colstring2], search='tree')
            # 3. Rows and columns
            tf = build(config, url= '', rows=[rowstring1,rowstring2], cols=[colstring1, colstring2], search='tree')

    """
    rows = [] if rows is None else rows
    cols = [] if cols is None else cols
    search = SEARCH_STENCIL if search not in SEARCHTYPES else search

    tf = False

    [pparams] = utils.dicts.extract_values(config, ['params'])
    page = utils.drivers.get_page(url=url, params=pparams)
    soup = soups.get_soup(page)

    if soup:
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

        afilter = soups.get_filter_child_of_common_ancestor(soup, aitem1, aitem2)
        if afilter:
            config['website']['url'] = url
            config['website']['rows'] = afilter
            tf = True

        # Website columns
        if tf and len(cols) > 0:
            # TODO
            # cols from dict to list
            if search == SEARCH_EXACT_COLUMNS:
                ritem = soups.find_item(soup, astr=re.compile(cols[0]))
                for col in cols:
                    citem = soups.find_item(ritem, astr=re.compile(col))
                    if citem:
                        afilter = soups.get_filter(citem)
                        config['website']['cols'] = afilter
            elif search == SEARCH_STENCIL:
                # TODO
                config['website']['cols'] = []
            elif search == SEARCH_STRIPPED_STRINGS:
                config['website']['cols'] = []
    return tf



