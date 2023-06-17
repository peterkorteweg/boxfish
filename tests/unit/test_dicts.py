# test_dicts.py

from boxfish.utils import dicts


def test_get_subset():
    """Test test_get_subset

    Function tested:
    test_get_subset

    Args:

    Returns:
        assert
    """
    adict = dict()
    value1 = "value1"
    value2 = "value2"
    adict["key1"] = value1
    adict["key2"] = value2
    akeys = list(adict.keys())
    ckeys = ["key1", "key3"]

    bkeys_expected = list(set(akeys) & set(ckeys))

    bdict = dicts.get_subset(adict, ckeys)
    bkeys = list(bdict.keys())
    assert bkeys == bkeys_expected


def test_extract_values():
    """Test extract_values

    Function tested:
    extract_values

    Args:

    Returns:
        assert
    """
    adict = dict()
    value1 = "value1"
    value2 = "value2"
    adict["key1"] = value1
    adict["key2"] = value2
    [output1, output2, output3] = dicts.extract_values(adict, ["key1", "key2", "key3"])
    assert output1 == value1 and output2 == value2 and output3 is None
    pass


def test_append():
    """Test append

    Function tested:
    append

    """
    adict = {"key1": "val1", "key2": "val2"}
    bdict = {"key1": "bval1", "key3": "val3"}
    cdict = dicts.append(adict, bdict)

    # keys
    keys = list(cdict.keys())
    keys_expected = ["key1", "key2", "key3"]
    assert keys == keys_expected

    # values
    values = list(cdict.values())
    values_expected = ["bval1", "val2", "val3"]
    assert values == values_expected


def test_remove_nones():
    """Test remove_nones

    Function tested:
    remove_nones

    """
    adict = {"key1": "val1", "key2": None, "key3": "val3"}
    bdict_expected = {"key1": "val1", "key3": "val3"}
    bdict = dicts.remove_nones(adict)
    assert bdict == bdict_expected


def test_loads():
    # Single item
    adict = {"name": "John", "age": 30, "city": "New York"}
    ajson = '{"name": "John", "age": 30, "city": "New York"}'
    adict2 = dicts.loads(ajson)
    assert adict == adict2

    # List
    ajson = '{"name": "John", "age": 30, "city": "New York"}'
    bjson = '{"name": "Jane", "age": 28, "city": "New Jersey"}'
    json_list = [ajson, bjson]
    alist = dicts.loads(json_list)
    assert isinstance(alist, list)
    assert alist[0] == adict


def test_dumps():
    # Single item
    adict = {"name": "John", "age": 30, "city": "New York"}
    ajson = '{"name": "John", "age": 30, "city": "New York"}'
    ajson2 = dicts.dumps(adict)
    assert ajson == ajson2

    # List
    adict = {"name": "John", "age": 30, "city": "New York"}
    bdict = {"name": "Jane", "age": 28, "city": "New Jersey"}
    dict_list = [adict, bdict]
    alist = dicts.dumps(dict_list)
    assert isinstance(alist, list)
    assert alist[0] == ajson


def test_set_():
    adict = {"name": "John", "age": 30, "city": "New York"}
    bdict = {"name": "Jane", "age": 28, "city": "New Jersey"}
    cdict = {"name": "Cal", "age": 32, "city": "San Francisco"}

    dict_list = [bdict, adict, adict, bdict, cdict]
    dict_set = dicts.set_(dict_list)
    assert len(dict_set) == 3
