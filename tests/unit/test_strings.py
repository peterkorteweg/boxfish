# strings.py

import scrape


# General
def test_rstrip_endswith():
    """ Test rstrip_endswith

    Function tested:
    rstrip_endswith()
    """

    # 1 character
    astr = scrape.utils.strings.rstrip_endswith('Hello', 'o')
    assert astr == 'Hell'
    # 2 multiple characters
    astr = scrape.utils.strings.rstrip_endswith('Hello', 'llo')
    assert astr == 'He'
    # 3 all characters
    astr = scrape.utils.strings.rstrip_endswith('Hello', 'Hello')
    assert astr == ''


def test_replace_newlines():
    """ Test replace_newlines

    Function tested:
    replace_newlines()
    """
    # 1 \n
    astr = scrape.utils.strings.replace_newlines('Hello \nWorld', '')
    assert astr == 'Hello World'
    # 2 \r\n
    astr = scrape.utils.strings.replace_newlines('Hello \r\nWorld', '')
    assert astr == 'Hello World'
    # 3 \r\n with '-'
    astr = scrape.utils.strings.replace_newlines('Hello\r\nWorld', '-')
    assert astr == 'Hello-World'


def test_to_int():
    # String with int
    astr = '-4'
    aint = scrape.utils.strings.to_int(astr)
    assert isinstance(aint, int)

    # String with float
    astr = '-4.2'
    aint = scrape.utils.strings.to_int(astr)
    assert isinstance(aint, int)

    # String non numeric
    astr = '-4.2s'
    aint = scrape.utils.strings.to_int(astr)
    assert aint is None


def test_to_float():
    # String with int
    astr = '-4'
    aint = scrape.utils.strings.to_float(astr)
    assert isinstance(aint, float)

    # String with float
    astr = '-4.2'
    aint = scrape.utils.strings.to_float(astr)
    assert isinstance(aint, float)

    # String non numeric
    astr = '-4.2s'
    aint = scrape.utils.strings.to_float(astr)
    assert aint is None


# Filenames
def test_filename_append_date():
    """ Test filename_append_date

    Function tested:
    filename_append_date

    """
    pass


def test_filename_append_extension():
    """ Test filename_append_extension

    Function tested:
    filename_append_extension

    """
    filename = 'filename'
    default_extension = '.py'
    filename_ext = scrape.utils.strings.filename_append_extension(filename, default_extension)
    filename_expected = 'filename.py'
    assert filename_ext == filename_expected

    filename = r'D:\filename'
    default_extension = '.py'
    filename_ext = scrape.utils.strings.filename_append_extension(filename, default_extension)
    filename_expected = r'D:\filename.py'
    assert filename_ext == filename_expected
