# config.py
# Created 11-10-2020
# Author P. Korteweg

"""Config is a module that contains functions for scrape configuration

"""

import os
import re
import shutil
from scrape.data import soups
from scrape.utils.utils import read_json, write_json, flip
from scrape import utils


CONFIGKEYS = ['url', 'driver', 'website', 'dataset']
WEBSITEKEYS = ['parser', 'id', 'rows', 'columns', 'page']
DATASETKEYS = ['filename', 'date_format', 'overwrite']

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

    config['url'] = url

    config['driver'] = utils.drivers.create_params(package='requests',
                                                   headers=HEADERS,
                                                   timeout=10,
                                                   filename='',
                                                   log='',
                                                   sleep={'1': 1, '200': 3600},
                                                   headless=True)

    config['website'] = dict.fromkeys(WEBSITEKEYS, {})
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


def build_rows(config, url='', slist=None):
    """ Build configuration rows
        Function builds a rows filter based on a match on two strings in url

            build_rows(config, url= '', slist = None)

            Args:
                config (dict): configuration
                url (str): Url
                slist (list): string list with two strings
                
            Returns:
                None
    """
    # TODO Error handling

    slist = [] if slist is None else slist

    if len(slist) == 2:
        [pparams] = utils.dicts.extract_values(config, ['params'])
        page = utils.drivers.get_page(url=url, params=pparams)
        soup = soups.get_soup(page)

        if soup:
            str1 = re.compile(slist[0])
            aitem1 = soups.find_item(soup, astr=str1)
            str2 = re.compile(slist[1])
            aitem2 = soups.find_item(soup, astr=str2)
            aparent = soups.find_common_parent(aitem1, aitem2)
            if aparent:
                adescendants = soups.find_descendants(aparent, aitem1)
                aitem = adescendants[0]

                if aitem:
                    afilter = soups.get_filter(aitem)
                    config['website']['rows'] = afilter
