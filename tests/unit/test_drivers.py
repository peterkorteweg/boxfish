# test_drivers.py

import boxfish
from boxfish.utils import drivers
import requests
from selenium import webdriver
import time

PAGE_URL = 'http://books.toscrape.com'
PAGE_FILE = r'.\data\bookstoscrape.html'

CONFIG_SELENIUM = r'.\\configurations\config_bookstoscrape.json'


# Helper functions
def get_config(filename=CONFIG_SELENIUM):
    if filename is '':
        config = boxfish.config.create('')
    else:
        config = boxfish.config.read(filename)
    return config


def test_get_page():
    """ Test request_page for default driver

    Function tested:
    get_page

    Args:

    Returns:
    """
    url = PAGE_URL
    page = drivers.get_page(url)
    assert isinstance(page, str)


def test_request_page():
    """ Test request_page for specific driver

    Function tested:
    request_page

    Args:

    Returns:
        assert
    """
    config = get_config()

    params = config['driver']
    params['package'] = 'requests'

    adriver = drivers.driver_start(params)

    # Test URL HTTP
    url = PAGE_URL
    page = drivers.request_page(adriver, url)
    assert isinstance(page, str)

    # Test from file
    url = PAGE_FILE
    page = drivers.request_page(adriver, url)
    assert isinstance(page, str)

    drivers.driver_stop(adriver)


def test_request_page_selenium():
    """ Test request_page for specific driver

    Function tested:
    request_page

    Args:

    Returns:
        assert
    """
    config = get_config()

    config['driver']['headless'] = False
    config['driver']['package'] = 'selenium'

    params = config['driver']

    # Test URL HTTP
    url = PAGE_URL
    page = drivers.get_page(url=url, params=params)
    assert isinstance(page, str)


def test_request_page_sleep():
    config = get_config()

    params = config['driver']
    params['package'] = 'requests'
    params['sleep'] = {"1": 2}

    # Test URL HTTP
    url = PAGE_URL
    adriver = drivers.driver_start(params)
    start = time.time()
    drivers.request_page(adriver, url, params=params, count=1)
    end = time.time()
    drivers.driver_stop(adriver)

    assert end-start > 2


def test_create_params():
    params = drivers.create_params()
    pkeys = list(params.keys())
    assert pkeys == drivers.DRIVERKEYS


def test_driver_start_stop_requests():
    """ Test driver_start and driver_stop for package requests

    test_driver_start_stop_requests()
    Function tested:
    driver_start
    driver_stop

    Args:

    Returns:
        assert
    """
    config = get_config()

    params = config['driver']
    params['package'] = 'requests'

    adriver = drivers.driver_start(params)
    assert isinstance(adriver, requests.sessions.Session)
    drivers.driver_stop(adriver)


def test_driver_start_stop_selenium():
    """ Test driver_start and driver_stop for package selenium

    Function tested:
    driver_start
    driver_stop

    Args:

    Returns:
        assert
    """
    config = get_config()

    params = config['driver']
    params['package'] = 'selenium'

    adriver = drivers.driver_start(params)
    assert isinstance(adriver, webdriver.firefox.webdriver.WebDriver)
    drivers.driver_stop(adriver)


def test_driver_start_stop_selenium_headless_false():
    """ Test driver_start and driver_stop for package selenium in headless mode

    Function tested:
    driver_start
    driver_stop

    Args:

    Returns:
    """
    config = get_config()

    params = config['driver']
    params['package'] = 'selenium'
    params['headless'] = False

    adriver = drivers.driver_start(params)
    assert isinstance(adriver, webdriver.firefox.webdriver.WebDriver)
    drivers.driver_stop(adriver)
