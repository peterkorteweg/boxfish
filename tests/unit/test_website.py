# test_website.py
# Created 8-11-2020
# Author P. Korteweg

import scrape
from scrape.utils import drivers

FILE_DORMOUSE = r'.\data\dormouse.html'
FILE_NARREN = r'.\data\narren.html'
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

CONFIG_NARREN = r'.\\configurations\config_narrenschip_test.json'


# Helper functions
def get_config(filename=CONFIG_NARREN):
    if filename is '':
        config = scrape.config.create('')
    else:
        config = scrape.config.read(filename)
        config["url"] = FILE_NARREN
    return config


def get_page(filename=FILE_DORMOUSE):
    if filename is '':
        page = PAGE_DORMOUSE
    else:
        page = scrape.utils.utils.read(filename)
    return page


# def get_page_links(label='narrenschip'):
#     config = get_config(label=label)
#     page = get_page(label=label)
#     params = config['website']['page']
#
#     links = scrape.website.process_page_links(page, params)
#     return links


# Main functions
def test_get_website():
    # Happy flow from file
    config = get_config(CONFIG_NARREN)
    url = config["url"]
    df = scrape.website.get_website(url, config)
    assert len(df) > 0


def test_get_data():
    # Happy flow from file
    config = get_config(CONFIG_NARREN)
    url = config["url"]
    data, colnames = scrape.website.get_data(url, config)
    assert isinstance(data, list)
    assert isinstance(colnames, list)
    assert len(data) > 0
    assert len(colnames) > 0


def test_get_data_errors():
    # Non-Happy flow
    pass


# Beautiful Soup functions
def test_get_table():
    # Happy flow
    page = get_page(FILE_NARREN)
    config = get_config(CONFIG_NARREN)
    website = config["website"]
    atable = scrape.website.get_table(page, website)
    assert len(atable) > 0


def test_get_table_empty_page():
    # Empty page
    page = ''
    config = get_config(CONFIG_NARREN)
    website = config["website"]
    atable, _ = scrape.website.get_table(page, website)
    assert len(atable) == 0


def test_get_table_incorrect_page():
    # Incorrect page string
    page = 'Incorrect'
    config = get_config(CONFIG_NARREN)
    website = config["website"]
    atable, _ = scrape.website.get_table(page, website)
    assert len(atable) == 0


def test_get_table_incorrect_website():
    # Incorrect website parameters
    # TODO Exception handling
    # page = 'Incorrect'
    # config = get_config(CONFIG_NARREN)
    # website = config["website"]
    # atable = scrape.website.get_table(page, website)
    # assert len(atable) == 0
    assert True


def test_get_url_next_page():
    #     label = 'narrenschip'
    #     config = get_config(label)
    #     page = get_page(label)
    #
    #     url_base = config['urlparts']['url']
    #     params = config['website']['page']
    #     # url_next = scrape.website.get_url_next_page(page, params, url_base)
    #
    # TODO
    assert True

# Function process_next_page(page, website, url)
# filename = 'config_funda.json'
# config = scrape.config.read(filename)
# website = config['website']
# url = 'https://www.funda.nl/koop/bergen-nh/beschikbaar/'
#
# config['driver']['package'] = 'selenium'
# adriver = scrape.website.driver_start(config['driver'],headless=False)
#
# page = scrape.website.request_page(adriver, config['driver'], url, cnt=0)
#
# scrape.website.driver_stop(adriver)

# def test_process_page_links():
#     # labels = 'monster'
#     # first_links = 'https://www.monster.com/jobs/search?page=2'
#     labels = 'narrenschip'
#     first_links = '/collections/amsterdam?page=2'
#
#     links = get_page_links(label=labels)
#     print(links)
#
#     assert isinstance(links, list)
#     assert links[0] == first_links


def test_save():
    assert True


# Private functions
def test__get_data_from_driver():
    # Happy flow, single page
    # data = _get_data_from_driver(url, config, adriver)
    config = get_config(CONFIG_NARREN)
    url = config["url"]
    adriver = drivers.driver_start(config['driver'])
    data = scrape.website._get_data_from_driver(url, config, adriver)
    drivers.driver_stop(adriver)
    assert len(data) > 0


def test__get_data_from_driver_errors():
    # Non-Happy flows
    pass
