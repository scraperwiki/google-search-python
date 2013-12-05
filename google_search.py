#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import logging
import urllib
import urlparse

import json
from collections import OrderedDict

import requests


def _decode_response(json_string):
    response = json.loads(json_string)

    meta = {key: value for key, value in response.items() if key != 'items'}
    if int(meta['searchInformation']['totalResults']) == 0:
        logging.info("INFO: no search results.")
        logging.info(json.dumps(response, indent=4))
        return []

    for item in response['items']:
        item['meta'] = meta

    return response['items']


def _strip_protocol(url):
    """
    >>> _strip_protocol('http://foo.bar/blah.x?baz=10&bob=15;x')
    u'foo.bar/blah.x?baz=10&bob=15;x'
    """
    p = urlparse.urlparse(url)
    new_url = urlparse.urlunparse(
        ('', p.netloc, p.path, p.params, p.query, p.fragment))
    return new_url.lstrip('/')


class GoogleCustomSearch(object):
    def __init__(self, search_engine_id, api_key):
        self.search_engine_id = search_engine_id
        self.api_key = api_key

    def search(self, keyword, site=None, max_results=10):
        assert isinstance(keyword, basestring)

        url = self._make_url(keyword, site)

        response = requests.get(url)
        if response.status_code == 403:
            logging.info(response.content)
        response.raise_for_status()
        for search_result in _decode_response(response.content):
            yield search_result

    def _make_url(self, keyword, restrict_to_site):

        if restrict_to_site is not None:
            keyword = 'site:{} {}'.format(_strip_protocol(restrict_to_site),
                                          keyword)

        params = OrderedDict([
            ('cx', self.search_engine_id),
            ('key', self.api_key),
            ('rsz', '10'),
            ('num', '10'),
            ('googlehost', 'www.google.com'),
            ('gss', '.com'),
            ('q', keyword),
            ('oq', keyword),
            ('filter', '0'),  # duplicate content filter, 1 | 0
            ('safe', 'off'),  # strict | moderate | off
        ])
        #if restrict_to_site is not None:
        #    params['siteSearch'] = _strip_protocol(restrict_to_site)

        return 'https://www.googleapis.com/customsearch/v1?{}'.format(
            urllib.urlencode(params))
