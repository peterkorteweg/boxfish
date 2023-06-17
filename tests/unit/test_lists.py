# test_lists.py

import os

from boxfish.utils import lists


# General
def test_is_empty_true():
    """Test is_empty, input True

    Function tested:
    is_empty

    Args:

    Returns:
        assert
    """
    alist = []
    assert lists.is_empty(alist) is True
    alist.append("")
    assert lists.is_empty(alist) is True
    alist.append(None)
    assert lists.is_empty(alist) is True


def test_is_empty_false():
    """Test is_empty, input False

    Function tested:
    is_empty

    Args:

    Returns:
        assert
    """
    alist = ["Hello"]
    assert lists.is_empty(alist) is False
    alist = ["", "Hello"]
    assert lists.is_empty(alist) is False


def test_flatten():
    """Test flatten

    Function tested:
    flatten

    Args:

    Returns:
        assert
    """
    alist = []
    blist = [1, 2, 3]
    clist = ["Hello", "World"]
    alist.append(blist)
    alist.append(clist)
    flist = lists.flatten(alist)
    assert (flist[0 : len(blist)] == blist) and (flist[len(blist) :] == clist)


def test_unique():
    """Test unique

    Function tested:
    unique

    Args:

    Returns:
        assert
    """
    alist = [1, 2, 3, 3, 4, 5]
    ulist_expected = [1, 2, 3, 4, 5]
    ulist = lists.unique(alist)
    assert ulist == ulist_expected


def test_is_equal_length():
    """Test is_equal_length

    Function tested:
    is_equal_length

    Args:

    Returns:
        assert
    """
    alist = [1, 2, 3, 4, 5]
    blist = [2, 4, 6, 8, 10]
    clist = [2, 4, 6, 8, 12]
    dlist = [2, 4, 6, 8]
    tf = lists.is_equal_length(alist, blist, clist)
    assert tf

    tf = lists.is_equal_length(alist, blist, clist, dlist)
    assert not tf


# Sets
def test_intersect():
    """Test intersect

    Function tested:
    intersect

    Args:

    Returns:
        assert
    """
    alist = [1, 2, 3, 3, 4, 5]
    blist = [2, 4, 6]
    clist_expected = [2, 4]
    clist = lists.intersect(alist, blist)
    assert clist == clist_expected


def test_union():
    """Test union

    Function tested:
    union

    Args:

    Returns:
        assert
    """
    alist = [1, 2, 3, 3, 4, 5]
    blist = [2, 4, 6]
    clist_expected = [1, 2, 3, 4, 5, 6]
    clist = lists.union(alist, blist)
    assert clist == clist_expected


def test_difference():
    """Test difference

    Function tested:
    difference

    Args:

    Returns:
        assert
    """
    alist = [1, 2, 3, 3, 4, 5]
    blist = [2, 4, 6]
    clist_expected = [1, 3, 5]
    clist = lists.difference(alist, blist)
    assert clist == clist_expected


def test_is_subset():
    """Test is_subset

    Function tested:
    is_subset

    Args:

    Returns:
        assert
    """
    alist = [1, 2, 3]
    blist = [1, 2, 3, 4, 5, 6]
    tf = lists.is_subset(alist, blist)
    assert tf

    clist = [1, 2, 4, 5, 6]
    tf = lists.is_subset(alist, clist)
    assert not tf


def test_is_disjoint():
    """Test is_disjoint

    Function tested:
    is_disjoint

    Args:

    Returns:
        assert
    """
    alist = [1, 2, 3]
    blist = [4, 5, 6]
    tf = lists.is_disjoint(alist, blist)
    assert tf

    clist = [1, 2, 3, 4, 5, 6]
    tf = lists.is_disjoint(alist, clist)
    assert not tf


# I/O functions
def test_to_csv_from_csv():
    alist = []
    blist = [1, 2, 3]
    clist = ["Hello", "World"]
    alist.append(blist)
    alist.append(clist)
    header = ["Col1", "Col2", "Col3"]
    filename = r".\results\test_to_csv.csv"

    # 1A. Write data. Example without date and header
    fullname = lists.to_csv(alist, filename, date_format="", overwrite=True, header=[])
    assert fullname == filename
    assert os.path.exists(fullname)

    # 1B. Read data
    alist_read = lists.from_csv(filename)
    assert alist_read == alist

    # 2A. Write data. Example without date and with header
    fullname = lists.to_csv(
        alist, filename, date_format="", overwrite=True, header=header
    )
    # 2B. Read data
    alist_read = lists.from_csv(filename)
    header_read = alist_read.pop(0)
    assert alist_read == alist
    assert header_read == header

    # 3A. Write data. Append.
    fullname = lists.to_csv(alist, filename, date_format="", overwrite=False, header=[])
    # 3B. Read data
    alist_read = lists.from_csv(filename)
    alist_read.pop(0)
    assert len(alist_read) == 2 * len(alist)

    # 4A. Write list of dicts based on internal header
    alist = []
    blist = {"Col1": 1, "Col2": 2, "Col3": 3}
    clist = {"Col1": 2, "Col2": 4, "Col3": 6}
    alist.append(blist)
    alist.append(clist)
    fullname = lists.to_csv(
        alist, filename, date_format="", overwrite=True, header=header
    )

    # 4A. Write list of dicts based with extended header
    header = ["Col1", "Col2", "Col3", "Col4"]
    fullname = lists.to_csv(
        alist, filename, date_format="", overwrite=True, header=header
    )

    # Clean up
    if os.path.exists(fullname):
        os.remove(fullname)

    # Example with date
    # See test_filename_append_date in tests_strings
