# create_url.py
# Syntax: [url] = create_url()
#
# =====================================
# Input:
# site          string      Url of website
# kwargs
# Output:
# url           string      Url of website
#
# =====================================
# Created 27-9-2020
# Author P. Korteweg

def shout2():
    print('Hello World')

def create_url(**kwargs):
    site = kwargs['site']
    if site=='monster.com':
        url = create_url_monster(**kwargs)
    elif site=='padi.com':
        url = create_url_padi(**kwargs)
    else:
        url = ''
    return url


def create_url_monster(**kwargs):
    job = kwargs['job']
    location = kwargs['location']

    url = 'https://www.monster.com/jobs/search/?' + \
          'q=' + job.replace(' ', '-') + \
          '&where=' + location.replace(' ', '-')

    return url


def create_url_padi(**kwargs):
    url = ''
    return url


