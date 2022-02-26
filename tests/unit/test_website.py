# test_website.py

import boxfish
from boxfish.utils import drivers

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
        config["website"]["url"] = FILE_BOOKS
    return config


def get_page(filename=FILE_DORMOUSE):
    if filename is '':
        page = PAGE_DORMOUSE
    else:
        page = boxfish.utils.utils.read(filename)
    return page


# def get_page_links(label='books'):
#     config = get_config(label=label)
#     page = get_page(label=label)
#     params = config['website']['page']
#
#     links = boxfish.website.process_page_links(page, params)
#     return links


# Main functions
def test_get_website():
    # Happy flow from file
    config = get_config(CONFIG_BOOKS)
    url = config["website"]["url"]
    df = boxfish.website.get_website(url, config)
    assert len(df) > 0


def test_get_data():
    # Happy flow from file
    config = get_config(CONFIG_BOOKS)
    url = config["website"]["url"]
    data, colnames = boxfish.website.get_data(url, config)
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
    page = get_page(FILE_BOOKS)
    config = get_config(CONFIG_BOOKS)
    website = config["website"]
    atable = boxfish.website.get_table(page, website)
    assert len(atable) > 0


def test_get_table_empty_page():
    # Empty page
    page = ''
    config = get_config(CONFIG_BOOKS)
    website = config["website"]
    atable, _ = boxfish.website.get_table(page, website)
    assert len(atable) == 0


def test_get_table_incorrect_page():
    # Incorrect page string
    page = 'Incorrect'
    config = get_config(CONFIG_BOOKS)
    website = config["website"]
    atable, _ = boxfish.website.get_table(page, website)
    assert len(atable) == 0


def test_get_table_incorrect_website():
    # Incorrect website parameters
    # TODO Exception handling
    # page = 'Incorrect'
    # config = get_config(CONFIG_BOOKS)
    # website = config["website"]
    # atable = boxfish.website.get_table(page, website)
    # assert len(atable) == 0
    assert True


def test_get_url_next_page():
    #     label = 'books'
    #     config = get_config(label)
    #     page = get_page(label)
    #
    #     url_base = config['urlparts']['url']
    #     params = config['website']['page']
    #     # url_next = boxfish.website.get_url_next_page(page, params, url_base)
    #
    # TODO
    assert True


def test_save():
    assert True


# Private functions
def test__get_data_from_driver():
    # Happy flow, single page
    # data = _get_data_from_driver(url, config, adriver)
    config = get_config(CONFIG_BOOKS)
    url = config["website"]["url"]
    adriver = drivers.driver_start(config['driver'])
    data = boxfish.website._get_data_from_driver(url, config, adriver)
    drivers.driver_stop(adriver)
    assert len(data) > 0


def test__get_data_from_driver_errors():
    # Non-Happy flows
    pass
