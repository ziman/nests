#!/usr/bin/env python3

import bs4
import requests
import logging
import json
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse

logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)

def process_player(http, title, page_url):
    url = urlparse(page_url)
    qs = {k: v[0] for k,v in parse_qs(url.query).items()}
    qs['output'] = 'playlist.m3u8'
    qs['format'] = 'jsonp'
    del qs['autostart']

    resp = http.get(urlunparse(url._replace(query=urlencode(qs))))
    doc = json.loads(resp.text.strip('()'))

    print('#EXTINF:0,', title)
    print(doc['data'])

def process_bird(http, title, page_url):
    log.info(page_url)
    resp = http.get(page_url)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    for a in soup.select('ul[role=tablist] a[role=tab]'):
        if not a.get('data-file'):
            continue

        process_player(
            http,
            title + ': ' + a['title'],
            urljoin(
                page_url,
                a['data-file'],
            )
        )

if __name__ == '__main__':
    http = requests.Session()
    
    page_url = 'https://www.vogelbescherming.nl/beleefdelente'
    resp = http.get(page_url)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    print('#EXTM3U')
    print('#EXTINF:0, ABN AMRO: binnen')
    print('http://91.142.248.190:1935/live/binnen/playlist.m3u8')
    print('#EXTINF:0, ABN AMRO: buiten')
    print('http://91.142.248.190:1935/live/buiten/playlist.m3u8')
    print('#EXTINF:0, ABN AMRO: buiten2')
    print('http://91.142.248.190:1935/live/buiten2/playlist.m3u8')

    for a in soup('a', 'link-pijl'):
        process_bird(http, ' '.join(s.strip() for s in a.strings), urljoin(page_url, a['href']))
