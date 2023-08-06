from bs4 import BeautifulSoup
import requests
import logging
import os
from urllib.parse import urlparse
from assistant.config import CONFIG

proxy_site = ['sehuatang.org']
log = logging.getLogger(__name__)


def get_soup(url):
    file_name = urlparse(url).path
    if not file_name:
        file_name = f'{urlparse(url).netloc}.html'
    buffer_path = os.path.join(os.path.dirname(CONFIG.basedir), 'cache', file_name)
    if not os.path.exists(buffer_path):
        log.debug(f'缓存路径:{buffer_path}')
        content = _get_content_http(url)
        with open(buffer_path, 'w', encoding='utf-8') as f:
            f.write(content.decode('utf-8'))
        return BeautifulSoup(content, 'html.parser')
    else:
        log.debug('buffer found，open file')
        return BeautifulSoup(open(buffer_path, encoding='utf-8'), 'html.parser')


def _get_content_http(url):
    """ :return  soup"""
    for site in proxy_site:
        # 检测是否在需要代理的范围中
        if site in url:
            log.debug(f'site need proxy: {url}')
            return requests.get(url, proxies=CONFIG.proxy(tg=False)).content
        else:
            log.debug('starting http request with no proxy')
            return requests.get(url).content

