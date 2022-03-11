# test_website.py

import boxfish
from boxfish.utils import drivers, utils

FILE_DORMOUSE = r'.\data\dormouse.html'
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

FILE_NARREN = r'.\data\narren.html'
CONFIG_NARREN = r'.\\configurations\config_narrenschip_test.json'

FILE_BOOKS = r'.\data\bookstoscrape.html'
CONFIG_BOOKS = r'.\\configurations\config_bookstoscrape.json'


# Helper functions
def get_config(filename=CONFIG_BOOKS, live=False):
    if filename is '':
        config = boxfish.config.create('')
    else:
        config = boxfish.config.read(filename)
        if not live:
            config['html']['url'] = FILE_BOOKS
    return config


def get_page(filename=FILE_DORMOUSE):
    if filename is '':
        page = PAGE_DORMOUSE
    else:
        page = utils.read(filename)
    return page


def get_page_live(url=''):
    return drivers.get_page(url)


# Main functions
def test_extract():
    # Happy flow from file
    config = get_config(CONFIG_BOOKS)
    url = config['html']['url']
    data = boxfish.website.extract(url, config)
    assert len(data) > 0


def test_get_data():
    # Happy flow from file
    config = get_config(CONFIG_BOOKS)
    url = config['html']['url']
    data = boxfish.website.get_data(url, config)
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_data_errors():
    # Non-Happy flow
    # TODO
    pass


# Beautiful Soup functions
def test_extract_table():
    # Happy flow
    page = get_page(FILE_BOOKS)
    config = get_config(CONFIG_BOOKS)
    ptable = config['html']['table']
    atable = boxfish.website.extract_table(page, ptable)
    assert len(atable) > 0


def test_extract_table_empty_page():
    # Empty page
    page = ''
    config = get_config(CONFIG_BOOKS)
    ptable = config['html']['table']
    atable = boxfish.website.extract_table(page, ptable)
    assert len(atable) == 0


def test_extract_table_incorrect_page():
    # Incorrect page string
    page = 'Incorrect'
    config = get_config(CONFIG_BOOKS)
    html = config['html']
    atable = boxfish.website.extract_table(page, html)
    assert len(atable) == 0


def test_extract_table_incorrect_website():
    # Incorrect website parameters
    # TODO Exception handling
    # page = 'Incorrect'
    # config = get_config(CONFIG_BOOKS)
    # website = config['html']
    # atable = boxfish.website.extract_table(page, website)
    # assert len(atable) == 0
    assert True


def test_get_url_next_page():
    config = get_config(CONFIG_BOOKS, live=True)

    url_base = config['html']['url']
    params = config['html']['page']
    page = get_page_live(config['html']['url'])

    url_next = boxfish.website.get_url_next_page(page, params, url_base)
    assert url_next == url_base + '/catalogue/page-2.html'


def test_save():
    assert True


# Private functions
def test__get_data_from_driver():
    # Happy flow, single page
    # data = _get_data_from_driver(url, config, adriver)
    config = get_config(CONFIG_BOOKS)
    url = config['html']['url']
    adriver = drivers.driver_start(config['driver'])
    data = boxfish.website._get_data_from_driver(url, config, adriver)
    drivers.driver_stop(adriver)
    assert len(data) > 0


def test__get_data_from_driver_errors():
    # Non-Happy flows
    pass
