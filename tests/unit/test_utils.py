# test_utils.py

import os
import time

from boxfish.utils import utils


# Files
def test_makedir():
    pass


def test_create_folder_if_not_exist():
    pass


def test_read_file_text():
    """Test read_file

    Function tested:
    read_file

    Args:

    Returns:
        assert
    """
    filename = r".\data\read_text.txt"
    text = utils.read(filename)
    assert isinstance(text, str)
    assert len(text) > 0


def test_read_json():
    filename = r".\data\read_json.json"

    # General
    text = utils.read(filename, filetype="json")
    assert isinstance(text, dict)

    # Specific function
    text = utils.read_json(filename)
    assert isinstance(text, dict)


def test_write_file_text():
    """Test write_file

    Function tested:
    read_file

    Args:

    Returns:
        assert
    """
    filename = r".\data\read_text.txt"
    text = utils.read(filename)
    assert isinstance(text, str)
    assert len(text) > 0

    filename_to = r".\data\write_text.txt"
    if os.path.exists(filename_to):
        os.remove(filename_to)
        time.sleep(2)
    utils.write(filename_to, text)
    assert os.path.exists(filename_to)
