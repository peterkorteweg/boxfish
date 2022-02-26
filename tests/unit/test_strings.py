# strings.py

import boxfish


# General
def test_rstrip_endswith():
    """ Test rstrip_endswith

    Function tested:
    rstrip_endswith()
    """

    # 1 character
    astr = boxfish.utils.strings.rstrip_endswith('Hello', 'o')
    assert astr == 'Hell'
    # 2 multiple characters
    astr = boxfish.utils.strings.rstrip_endswith('Hello', 'llo')
    assert astr == 'He'
    # 3 all characters
    astr = boxfish.utils.strings.rstrip_endswith('Hello', 'Hello')
    assert astr == ''


def test_replace_newlines():
    """ Test replace_newlines

    Function tested:
    replace_newlines()
    """
    # 1 \n
    astr = boxfish.utils.strings.replace_newlines('Hello \nWorld', '')
    assert astr == 'Hello World'
    # 2 \r\n
    astr = boxfish.utils.strings.replace_newlines('Hello \r\nWorld', '')
    assert astr == 'Hello World'
    # 3 \r\n with '-'
    astr = boxfish.utils.strings.replace_newlines('Hello\r\nWorld', '-')
    assert astr == 'Hello-World'


def test_to_int():
    # String with int
    astr = '-4'
    aint = boxfish.utils.strings.to_int(astr)
    assert isinstance(aint, int)

    # String with float
    astr = '-4.2'
    aint = boxfish.utils.strings.to_int(astr)
    assert isinstance(aint, int)

    # String non numeric
    astr = '-4.2s'
    aint = boxfish.utils.strings.to_int(astr)
    assert aint is None


def test_to_float():
    # String with int
    astr = '-4'
    aint = boxfish.utils.strings.to_float(astr)
    assert isinstance(aint, float)

    # String with float
    astr = '-4.2'
    aint = boxfish.utils.strings.to_float(astr)
    assert isinstance(aint, float)

    # String non numeric
    astr = '-4.2s'
    aint = boxfish.utils.strings.to_float(astr)
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
    filename_ext = boxfish.utils.strings.filename_append_extension(filename, default_extension)
    filename_expected = 'filename.py'
    assert filename_ext == filename_expected

    filename = r'D:\filename'
    default_extension = '.py'
    filename_ext = boxfish.utils.strings.filename_append_extension(filename, default_extension)
    filename_expected = r'D:\filename.py'
    assert filename_ext == filename_expected
