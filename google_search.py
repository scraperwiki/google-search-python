#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import logging
import urllib
import urlparse

import json
from collections import OrderedDict

import requests

LOG = logging.getLogger('sw.google_search')


def _decode_response(json_string):
    response = json.loads(json_string)

    meta = {key: value for key, value in response.items() if key != 'items'}
    num_results = int(meta['searchInformation']['totalResults'])
    if num_results == 0:
        LOG.info("No search results.")
        LOG.info(json.dumps(response, indent=4))
        return []
    else:
        LOG.info("{} results.".format(num_results))

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

    def search(self, keyword, site=None, max_results=100):
        assert isinstance(keyword, basestring)

        for start_index in range(1, max_results, 10):  # 10 is max page size
            url = self._make_url(start_index, keyword, site)
            logging.info(url)

            response = requests.get(url)
            if response.status_code == 403:
                LOG.info(response.content)
            response.raise_for_status()
            for search_result in _decode_response(response.content):
                yield search_result
                if 'nextPage' not in search_result['meta']['queries']:
                    print("No more pages...")
                    return

    def _make_url(self, start_index, keyword, restrict_to_site):

        if restrict_to_site is not None:
            keyword = 'site:{} {}'.format(_strip_protocol(restrict_to_site),
                                          keyword)
        # https://developers.google.com
        # /custom-search/json-api/v1/reference/cse/list
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
