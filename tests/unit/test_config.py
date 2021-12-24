# test_config.py
# Created 1/1/2021
# Author P. Korteweg

import scrape
from scrape.utils import drivers

FILE_NARREN = r'.\data\narren.html'
STR_NARREN1 = 'Amsterdam Aanzicht vanaf het IJ'
STR_NARREN2 = 'Amsterdam Stadsplattegrond in vogelvluchtperspectief'


# Helper functions
def get_query(tf):
    if tf:
        aquery = {'key': 'key_new_value'}
    else:
        aquery = 10
    return aquery


# Initialization
def test_create_all_keys():
    aconfig = scrape.config.create()
    assert sorted(list(aconfig.keys())) == sorted(scrape.config.CONFIGKEYS)


def test_create_all_keys_sub():
    aconfig = scrape.config.create()
    keys_sub = {'driver': drivers.DRIVERKEYS,
                'website': scrape.config.WEBSITEKEYS,
                'dataset': scrape.config.DATASETKEYS}
    for key in list(aconfig.keys()):
        if key in list(keys_sub.keys()):
            actual_keys_sub = list(aconfig[key].keys())
            expected_keys_sub = keys_sub[key]
            assert sorted(actual_keys_sub) == sorted(expected_keys_sub)


# I/O
# passed

# Editing configurations
def test_process_missing_keys():
    aconfig = scrape.config.create()
    aconfig.pop('url', None)
    scrape.config.process(aconfig)
    assert sorted(list(aconfig.keys())) == sorted(scrape.config.CONFIGKEYS)


def test_process_non_keys():
    aconfig = scrape.config.create()
    aconfig['non_key'] = 'Not a key'
    scrape.config.process(aconfig)
    assert sorted(list(aconfig.keys())) == sorted(scrape.config.CONFIGKEYS)


def test_build_rows():
    config = scrape.config.create('')
    aurl = FILE_NARREN
    astr1 = STR_NARREN1
    astr2 = STR_NARREN2
    scrape.config.build_rows(config, url=aurl, slist=[astr1, astr2])
    adict = config['website']['rows']
    assert adict is not None
    assert 'elem' in adict and 'class' in adict
    assert config['website']['rows']['elem'] == 'li'
