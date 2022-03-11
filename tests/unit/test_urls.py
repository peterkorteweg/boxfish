# test_urls.py

from boxfish.utils import urls


def test_set_components():
    """ Test set_components

    Function tested:
    set_components

    Args:

    Returns:
        assert
    """
    aurl = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    scheme = 'ftp'
    netloc = 'newloc.com'
    query = {'query1': 'arg1', 'query2': 'arg2'}
    path = '/p11/p22'
    path_no_backlash = 'p11/p22'
    cdict = {'scheme': scheme, 'netloc': netloc}
    ddict = {'scheme': scheme, 'netloc': netloc, 'nokey': 'no value'}

    # Replace single item
    aurl_new = urls.set_components(aurl, scheme=scheme)
    aurl_expected = 'ftp://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    assert aurl_new == aurl_expected

    aurl_new = urls.set_components(aurl, netloc=netloc)
    aurl_expected = 'http://newloc.com/p1;para/p2;para?query=arg#frag'
    assert aurl_new == aurl_expected

    # Replace two items
    aurl_new = urls.set_components(aurl, scheme=scheme, netloc=netloc)
    aurl_expected = 'ftp://newloc.com/p1;para/p2;para?query=arg#frag'
    assert aurl_new == aurl_expected

    # Replace query from dict
    aurl_new = urls.set_components(aurl, query=query)
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query1=arg1&query2=arg2#frag'
    assert aurl_new == aurl_expected

    # Replace path
    aurl_new = urls.set_components(aurl, path=path)
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p11/p22?query=arg#frag'
    assert aurl_new == aurl_expected

    # Replace path_no_backlash
    aurl_new = urls.set_components(aurl, path=path_no_backlash)
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p11/p22?query=arg#frag'
    assert aurl_new == aurl_expected

    # Replace items from dict
    aurl_new = urls.set_components(aurl, **cdict)
    aurl_expected = 'ftp://newloc.com/p1;para/p2;para?query=arg#frag'
    assert aurl_new == aurl_expected

    # Replace items from dict with unknown keys
    aurl_new = urls.set_components(aurl, **ddict)
    aurl_expected = 'ftp://newloc.com/p1;para/p2;para?query=arg#frag'
    assert aurl_new == aurl_expected


def test_get_components():
    """ Test get_components

    Function tested:
    get_components

    Args:

    Returns:
        assert
    """
    aurl = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    adict_expected = {'scheme': 'http',
                      'netloc': 'user:pwd@NetLoc.com:80',
                      'path': '/p1;para/p2;para',
                      'query': 'query=arg',
                      'fragment': 'frag',
                      }
    adict = urls.get_components(aurl)
    assert adict_expected == adict


def test_replace_subpath():
    """ Test replace_subpath

    Function tested:
    replace_subpath

    Args:

    Returns:
        assert
    """

    url_original = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    url_empty_path = 'http://user:pwd@NetLoc.com'
    subpath = 'p3'

    # Index 0
    index = 0
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p3/p2;para?query=arg#frag'
    aurl = urls.replace_subpath(url_original, subpath, index)
    assert aurl_expected == aurl

    # Index 1
    index = 1
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p1;para/p3?query=arg#frag'
    aurl = urls.replace_subpath(url_original, subpath, index)
    assert aurl_expected == aurl

    # Non-existing level
    index = 2
    aurl_expected = url_original
    aurl = urls.replace_subpath(url_original, subpath, index)
    assert aurl_expected == aurl

    # Index 0, subpath with multiple paths
    index = 0
    subpath = 'p3/p4'
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p3/p4/p2;para?query=arg#frag'
    aurl = urls.replace_subpath(url_original, subpath, index)
    assert aurl_expected == aurl

    #Index 0, original path is empty
    index = 0
    subpath = '/catalogue/page.html'
    aurl_expected = url_empty_path + subpath
    aurl = urls.replace_subpath(url_empty_path, subpath, index)
    assert aurl_expected == aurl

    #Index 0, original path is empty
    index = 0
    subpath = 'page.html'
    aurl_expected = url_empty_path + '/' + subpath
    aurl = urls.replace_subpath(url_empty_path, subpath, index)
    assert aurl_expected == aurl


def test_replace_subquery():
    """ Test replace_subquery

    Function tested:
    replace_subquery

    Args:

    Returns:
        assert
    """

    url_original = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query1=arg1&query2=arg2&query3=arg3#frag'

    # Existing query with single item
    subquery = 'query1=arg11'
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query1=arg11&query2=arg2&query3=arg3#frag'
    aurl = urls.replace_subquery(url_original, subquery)
    assert aurl_expected == aurl

    # Existing query with multiple items
    subquery = 'query1=arg11&query3=arg33'
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query1=arg11&query2=arg2&query3=arg33#frag'
    aurl = urls.replace_subquery(url_original, subquery)
    assert aurl_expected == aurl

    # New query
    subquery = 'query4=arg4'
    aurl_expected = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query1=arg1&query2=arg2&query3=arg3&query4=arg4#frag'
    aurl = urls.replace_subquery(url_original, subquery)
    assert aurl_expected == aurl


def test_create_url_list():
    """ Test create_url_list

    Function tested:
    create_url_list

    Args:

    Returns:
        assert
    """

    # Single url, single query, no path
    url_original = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    query = 'query1=arg1'
    aurl_list_expected = ['http://user:pwd@NetLoc.com:80/p1;para/p2;para?query1=arg1#frag']
    aurl_list = urls.create_url_list(url_original, query=query)
    assert aurl_list == aurl_list_expected

    # Single url, no query, single path
    url_original = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    path = '/p3/p4'
    aurl_list_expected = ['http://user:pwd@NetLoc.com:80/p3/p4?query=arg#frag']
    aurl_list = urls.create_url_list(url_original, path=path)
    assert aurl_list == aurl_list_expected

    # Single url, two queries, no path
    url_original = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    query = ['query1=arg1', 'query2=arg2']
    aurl_list_expected = ['http://user:pwd@NetLoc.com:80/p1;para/p2;para?query1=arg1#frag',
                          'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query2=arg2#frag',
                          ]
    aurl_list = urls.create_url_list(url_original, query=query)
    assert aurl_list == aurl_list_expected

    # Single url, two queries, single path
    url_original = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    query = ['query1=arg1', 'query2=arg2']
    path = '/p3/p4'
    aurl_list_expected = ['http://user:pwd@NetLoc.com:80/p3/p4?query1=arg1#frag',
                          'http://user:pwd@NetLoc.com:80/p3/p4?query2=arg2#frag',
                          ]
    aurl_list = urls.create_url_list(url_original, query=query, path=path)
    assert aurl_list == aurl_list_expected

    # Single url, two queries, two paths
    url_original = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    query = ['query1=arg1', 'query2=arg2']
    path = ['/p3/p4', '/p5/p6']
    aurl_list_expected = ['http://user:pwd@NetLoc.com:80/p3/p4?query1=arg1#frag',
                          'http://user:pwd@NetLoc.com:80/p5/p6?query2=arg2#frag',
                          ]
    aurl_list = urls.create_url_list(url_original, query=query, path=path)
    assert aurl_list == aurl_list_expected

    # Two urls, two queries, two paths
    url_original = ['http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag',
                    'ftp://newloc.com/p11;para/p22;para?query11=arg11#frag2']
    query = ['query1=arg1', 'query2=arg2']
    path = ['/p3/p4', '/p5/p6']
    aurl_list_expected = ['http://user:pwd@NetLoc.com:80/p3/p4?query1=arg1#frag',
                          'ftp://newloc.com/p5/p6?query2=arg2#frag2',
                          ]
    aurl_list = urls.create_url_list(url_original, query=query, path=path)
    assert aurl_list == aurl_list_expected

    # Single url, two queries, three paths
    url_original = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    query = ['query1=arg1', 'query2=arg2']
    path = ['/p3/p4', '/p5/p6', '/p7/p8']
    aurl_list_expected = []
    aurl_list = urls.create_url_list(url_original, query=query, path=path)
    assert aurl_list == aurl_list_expected


def test_valid_http():
    url_http = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    url_https = 'http://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    url_no_http = 'ftp://user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    url_no_scheme = 'user:pwd@NetLoc.com:80/p1;para/p2;para?query=arg#frag'
    assert urls.valid_http(url_http)
    assert urls.valid_http(url_https)
    assert not urls.valid_http(url_no_http)
    assert not urls.valid_http(url_no_scheme)


# Private functions
def test__dict_to_path():
    """ Test get_components

    Function tested:
    get_components

    Args:

    Returns:
        assert
    """

    # Path without filename
    adict = {'path_a': 'path1', 'path_b': 'path2'}
    path_expected = r'/path1/path2'
    path = urls._dict_to_path(adict)
    assert path_expected == path

    # Path with filename
    adict = {'path_a': 'path1', 'path_b': 'path2', 'path_c': 'filename.html'}
    path_expected = r'/path1/path2/filename.html'
    path = urls._dict_to_path(adict)
    assert path_expected == path

    # Path with extra start backslashes
    adict = {'path_a': '/path1', 'path_b': '/path2', 'path_c': '/filename.html'}
    path_expected = r'/path1/path2/filename.html'
    path = urls._dict_to_path(adict)
    assert path_expected == path


def test__path_to_dict():
    """ Test _path_to_dict

    Function tested:
    _path_to_dict

    Args:

    Returns:
        assert
    """

    # Path without filename
    path = r'/path1/path2/'
    adict_expected = {'0': 'path1', '1': 'path2'}
    adict = urls._path_to_dict(path)
    assert adict_expected == adict

    # Path with filename
    path = r'/path1/path2/filename.html'
    adict_expected = {'0': 'path1', '1': 'path2', '2': 'filename.html'}
    adict = urls._path_to_dict(path)
    assert adict_expected == adict

    # Path with extra backslashes
    path = r'//path1//path2//filename.html'
    adict_expected = {'0': 'path1', '1': 'path2', '2': 'filename.html'}
    adict = urls._path_to_dict(path)
    assert adict_expected == adict


def test__dict_to_query():
    """ Test _dict_to_query

    Function tested:
    _dict_to_query

    Args:

    Returns:
        assert
    """

    # Query wihtout special characters
    adict = {'query1': 'arg1', 'query2': 'arg2'}
    query_expected = r'query1=arg1&query2=arg2'
    query = urls._dict_to_query(adict)
    assert query_expected == query

    # Query with spaces
    adict = {'query1': 'arg1a arg1b', 'query2': 'arg2'}
    query_expected = r'query1=arg1a+arg1b&query2=arg2'
    query = urls._dict_to_query(adict)
    assert query_expected == query


def test__query_to_dict():
    """ Test _query_to_dict

    Function tested:
    _query_to_dict

    Args:

    Returns:
        assert
    """

    # Query without special characters
    query = r'query1=arg1&query2=arg2'
    adict_expected = {'query1': 'arg1', 'query2': 'arg2'}
    adict = urls._query_to_dict(query)
    assert adict_expected == adict

    # Query with spaces
    query = r'query1=arg1a+arg1b&query2=arg2'
    adict_expected = {'query1': 'arg1a arg1b', 'query2': 'arg2'}
    adict = urls._query_to_dict(query)
    assert adict_expected == adict
