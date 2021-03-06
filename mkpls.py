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

def process_bird(http, orig_title, page_url):
    log.info(page_url)
    resp = http.get(page_url)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    divs = soup('div', id='vue')
    if not divs:
        return
    else:
        items = json.loads(divs[0]['data-cams'])

    SAMPLE_ITEM = {
        "naam": "Binnencam",
        "mediaid": "media8",
        "order": 10,
        "url": "bosuil1",
        "file": "//rrr.sz.xlcdn.com/?account=bdl&file=bosuil1&type=live&service=wowza&output=player&autostart=1",
        "id": 8,
        "vogel": 22,
        "actief": 1
    }

    for item in items:
        process_player(
            http,
            '[%s] %s' % (item['naam'].strip(), orig_title),
            urljoin(
                page_url,
                item['file'],
            )
        )

if __name__ == '__main__':
    http = requests.Session()
    
    print('#EXTM3U')
    print('#EXTINF:0, ABN AMRO: binnen')
    print('http://streaming.avex.nl/live/valkbinnen/playlist.m3u8')
    print('#EXTINF:0, ABN AMRO: buiten')
    print('http://streaming.avex.nl/live/valkbuiten/playlist.m3u8')
    print('#EXTINF:0, ABN AMRO: buiten2')
    print('http://streaming.avex.nl/live/valkbuiten2/playlist.m3u8')

    page_url = 'https://www.vogelbescherming.nl/beleefdelente'
    resp = http.get(page_url)
    resp.raise_for_status()
    soup = bs4.BeautifulSoup(resp.text, 'html.parser')

    for a in soup('a', 'link-pijl'):
        process_bird(http, ' '.join(s.strip() for s in a.strings), urljoin(page_url, a['href']))
