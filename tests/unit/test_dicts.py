# test_dicts.py

import scrape


def test_get_subset():
    """ Test test_get_subset

    Function tested:
    test_get_subset

    Args:

    Returns:
        assert
    """
    adict = dict()
    value1 = 'value1'
    value2 = 'value2'
    adict['key1'] = value1
    adict['key2'] = value2
    akeys = list(adict.keys())
    ckeys = ['key1', 'key3']

    bkeys_expected = list(set(akeys) & set(ckeys))

    bdict = scrape.utils.dicts.get_subset(adict, ckeys)
    bkeys = list(bdict.keys())
    assert bkeys == bkeys_expected


def test_extract_values():
    """ Test extract_values

    Function tested:
    extract_values

    Args:

    Returns:
        assert
    """
    adict = dict()
    value1 = 'value1'
    value2 = 'value2'
    adict['key1'] = value1
    adict['key2'] = value2
    [output1, output2, output3] = scrape.utils.dicts.extract_values(adict, ['key1', 'key2', 'key3'])
    assert output1 == value1 and output2 == value2 and output3 is None
    pass


def test_append():
    """ Test append

    Function tested:
    append

    """
    adict = {'key1': 'val1', 'key2': 'val2'}
    bdict = {'key1': 'bval1', 'key3': 'val3'}
    cdict = scrape.utils.dicts.append(adict, bdict)

    # keys
    keys = list(cdict.keys())
    keys_expected = ['key1', 'key2', 'key3']
    assert keys == keys_expected

    # values
    values = list(cdict.values())
    values_expected = ['bval1', 'val2', 'val3']
    assert values == values_expected


def test_remove_nones():
    """ Test remove_nones

    Function tested:
    remove_nones

    """
    adict = {'key1': 'val1', 'key2': None, 'key3': 'val3'}
    bdict_expected = {'key1': 'val1', 'key3': 'val3'}
    bdict = scrape.utils.dicts.remove_nones(adict)
    assert bdict == bdict_expected
