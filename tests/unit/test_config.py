# test_config.py


import boxfish
from boxfish.utils import drivers

FILE_BOOKS = r'.\data\bookstoscrape.html'
STR_BOOKS_TITLE1 = 'A Light in the ...'
STR_BOOKS_PRICE1 = '£51.77'
STR_BOOKS_TITLE2 = 'Tipping the Velvet'
STR_BOOKS_PRICE2 = '£53.74'

CONFIG_BOOKS_ELEM = 'li'
CONFIG_BOOKS_CLASS = ['col-xs-6', 'col-sm-4', 'col-md-3', 'col-lg-3']


# Helper functions
def get_query(tf):
    if tf:
        aquery = {'key': 'key_new_value'}
    else:
        aquery = 10
    return aquery


# Initialization
def test_create_all_keys():
    aconfig = boxfish.config.create()
    assert sorted(list(aconfig.keys())) == sorted(boxfish.config.CONFIGKEYS)


def test_create_all_keys_sub():
    aconfig = boxfish.config.create()
    keys_sub = {'driver': drivers.DRIVERKEYS,
                'website': boxfish.config.WEBSITEKEYS,
                'dataset': boxfish.config.DATASETKEYS}
    for key in list(aconfig.keys()):
        if key in list(keys_sub.keys()):
            actual_keys_sub = list(aconfig[key].keys())
            expected_keys_sub = keys_sub[key]
            assert sorted(actual_keys_sub) == sorted(expected_keys_sub)


# I/O
# passed

# Editing configurations
def test_build():
    config = boxfish.config.create('')
    aurl = FILE_BOOKS

    # Build two titles
    astr1 = STR_BOOKS_TITLE1
    astr2 = STR_BOOKS_TITLE2
    boxfish.config.build(config, url=aurl, rows=[astr1, astr2])
    adict = config['website']['rows']
    assert adict is not None
    assert 'elem' in adict and 'class' in adict
    assert config['website']['rows']['elem'] == CONFIG_BOOKS_ELEM
    assert config['website']['rows']['class'] == CONFIG_BOOKS_CLASS

    # Build two prices
    astr1 = STR_BOOKS_PRICE1
    astr2 = STR_BOOKS_PRICE2
    boxfish.config.build(config, url=aurl, rows=[astr1, astr2])
    adict = config['website']['rows']
    assert adict is not None
    assert 'elem' in adict and 'class' in adict
    assert config['website']['rows']['elem'] == CONFIG_BOOKS_ELEM
    assert config['website']['rows']['class'] == CONFIG_BOOKS_CLASS

    # Build 1 title and 1 price
    astr1 = STR_BOOKS_TITLE1
    astr2 = STR_BOOKS_PRICE2
    boxfish.config.build(config, url=aurl, rows=[astr1, astr2])
    adict = config['website']['rows']
    assert adict is not None
    assert 'elem' in adict and 'class' in adict
    assert config['website']['rows']['elem'] == CONFIG_BOOKS_ELEM
    assert config['website']['rows']['class'] == CONFIG_BOOKS_CLASS

# Private functions
def test_process_missing_keys():
    aconfig = boxfish.config.create()
    aconfig.pop('url', None)
    boxfish.config._process(aconfig)
    assert sorted(list(aconfig.keys())) == sorted(boxfish.config.CONFIGKEYS)


def test_process_non_keys():
    aconfig = boxfish.config.create()
    aconfig['non_key'] = 'Not a key'
    boxfish.config._process(aconfig)
    assert sorted(list(aconfig.keys())) == sorted(boxfish.config.CONFIGKEYS)
