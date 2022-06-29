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
def get_config(filename=CONFIG_BOOKS):
    if filename is '':
        config = boxfish.config.create('')
    else:
        config = boxfish.config.read(filename)
    return config


def get_page(filename=''):
    if filename is '':
        page = PAGE_DORMOUSE
    else:
        page = utils.read(filename)
    return page


# Main functions
def test_extract_from_file():
    # Happy flow from file
    config = get_config(CONFIG_BOOKS)
    url = FILE_BOOKS
    data = boxfish.website.extract(url, config)
    assert len(data) > 0


def test_extract_data_from_file():
    # Happy flow from file
    config = get_config(CONFIG_BOOKS)
    url = FILE_BOOKS
    data = boxfish.website.extract_data(url, config)
    assert isinstance(data, list)
    assert len(data) > 0


def test_extract_data_errors_from_file():
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


def test_extract_url_next_page():
    # Extract relative URL
    config = get_config(CONFIG_BOOKS)

    url = config['html']['url']
    params = config['html']['page']

    page = drivers.get_page(config['html']['url'])

    url_next = boxfish.website.extract_url_next_page(page, params, url)
    assert url_next == 'http://books.toscrape.com/catalogue/page-2.html'


def test_save():
    assert True


# Private functions
def test__extract_data_from_driver_live():
    # Happy flow, single page
    # data = _extract_data_from_driver(url, config, adriver)
    config = get_config(CONFIG_BOOKS)
    url = config['html']['url']
    adriver = drivers.driver_start(config['driver'])
    data = boxfish.website._extract_data_from_driver(url, config, adriver)
    drivers.driver_stop(adriver)
    assert len(data) > 0


def test__get_data_from_driver_errors_live():
    # Non-Happy flows
    pass
