# urllibrary.py
# Created 11-10-2020
# Author P. Korteweg

""" Urllibrary contains functions to parse url strings """

from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from scrape.utils.utils import extract_dict_values
from scrape.utils.strings import rstrip_endswith


def create_from_parts(**kwargs):
    """ Create an url from parts

        url = create_from_parts(url, path, query, remove_existing_path, remove_existing_query):

        Args:
            **kwargs:
                url (str): url
                path (dict): path
                query (dict): query
                remove_existing_path (bool):  Removes existing path if true
                remove_existing_query (bool):  Removes existing query if true

        Returns:
            url (str): url
    """

    [url, path, query,
     remove_existing_path,
     remove_existing_query
     ] = extract_dict_values(kwargs, ['url', 'path', 'query',
                                      'remove_existing_path',
                                      'remove_existing_query'])

    url = set_path(url, path, remove_existing_path)
    url = set_query(url, query, remove_existing_query)

    return url


def set_path(url, path, remove_existing=False, keys_allowed=None):
    """ Set path in url

        url = set_path(url, path, remove_existing=False, keys_allowed=None)

        Args:
            url (str): url
            path (dict or string): {'hello': 'world'} or '/world'
            remove_existing (bool):  Removes existing path if true,
                                     appends to existing path if false
            keys_allowed (bool):  Dictionary with allowed keys

        Returns:
            url (str): url
    """

    if path is not None:
        if type(path) == str:
            path = _path_to_dict(path)
            keys_allowed = None

        if type(path) == dict:
            if keys_allowed is not None:
                path = {key: value for key, value in path.items() if key in keys_allowed}

        pr = urlparse(url)
        if remove_existing:
            new_path = _dict_to_path(path)
        else:
            new_path = rstrip_endswith(pr.path, '/') + _dict_to_path(path)

        pr = pr._replace(path=new_path)
        url = urlunparse(pr)
    return url


def set_query(url, query, remove_existing=False, keys_allowed=None):
    """ Set query in url

        url = set_query(url, query, remove_existing=False, keys_allowed=None)

        Args:
            url (str): url
            query (dict or string). {'hello': 'world'} or '/world'
            remove_existing (bool):  Removes existing query if true,
                                     appends to existing query if false
            keys_allowed (bool):  Dictionary with allowed keys

        Returns:
            url (str): url
    """

    if query is not None:
        if type(query) == str:
            query = dict(parse_qsl(query))

        if type(query) == dict:
            if keys_allowed is not None:
                query = {key: value for key, value in query.items() if key in keys_allowed}

            pr = urlparse(url)

            if remove_existing:
                query_curr = query
            else:
                query_curr = dict(parse_qsl(pr.query))
                query_curr.update(query)

            query_new = urlencode(query_curr)

            pr = pr._replace(query=query_new)
            url = urlunparse(pr)
    return url


def get_path(url):
    """ Get path from url

        path = get_path(url)

        Args:
            url (str): url

        Returns:
            path (dict): path
        """

    pr = urlparse(url)
    return _path_to_dict(pr.path)


def get_query(url):
    """ Get query from url

        query = get_query(url)

        Args:
            url (str): url

        Returns:
            query (dict): path
    """

    pr = urlparse(url)
    return dict(parse_qsl(pr.query))


def add_scheme_and_netloc(url, from_url):
    """ Adds schema and netloc from from_url to url

        url = add_scheme_and_netloc(url, from_url)

        Args:
            url (str): url
            from_url (str): url

        Returns:
            url (str): url with scheme and netloc of from_url
    """

    pr = urlparse(url)
    pr_from = urlparse(from_url)

    pr = pr._replace(netloc=pr_from.netloc)
    pr = pr._replace(scheme=pr_from.scheme)

    return urlunparse(pr)


def contains_scheme_and_netloc(url):
    """ Boolean indicator if url contains scheme and netloc

        tf = contains_scheme_and_netloc(url)

        Args:
            url (str): url

        Returns:
            tf (bool): True if url contains scheme and netloc
    """
    pr = urlparse(url)
    return (pr.scheme != '') and (pr.netloc != '')


# Private functions
def _dict_to_path(adict):
    """ Convert a dict to a url path

        path = _dict_to_path(adict)

        Args:
            adict (dict): key-value pairs

        Returns:
            path (str): url path /value1/value2 based on values in adict
    """
    path = ''
    if type(adict) == dict:
        for value in adict.values():
            path = path + '/' + value
        if len(adict) > 0:
            path = path + '/'
    return path


def _path_to_dict(path, keys=None):
    """ Convert a url path to a dict

        adict = _path_to_dict(path, keys=None)

        Args:
            path (str): url path /value1/value2
            keys (list): list of key strings or None

        Returns:
            adict (dict): key-value pairs for each element in path
    """
    adict = {}
    if type(path) == str:
        values = list(filter(None, path.split('/')))
        elems = len(values)

        if keys is None:
            keys = ["{}".format(i) for i in range(elems)]
        if len(keys) == elems:
            for i in range(elems):
                adict[keys[i]] = values[i]
    return adict
