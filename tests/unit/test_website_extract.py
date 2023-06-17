# test_website.py

import boxfish

CONFIG_NARREN = r".\\configurations\config_narrenschip_test.json"
CONFIG_BOOKS = r".\\configurations\config_bookstoscrape.json"


# Helper functions
def get_config(filename=CONFIG_BOOKS):
    return boxfish.config.read(filename)


# Main functions
def test_extract_books():
    # Books. Standard
    config = get_config(CONFIG_BOOKS)
    config["html"]["page"] = {}
    data = boxfish.website.extract(config["html"]["url"], config)
    assert len(data) > 0
