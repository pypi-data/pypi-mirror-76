import logging
import time
import re
from assistant.spider.request import get_soup

log = logging.getLogger(__name__)


class ShtSite:
    base_url = 'www.sehuatang.org'
    tags = {
        'cnSubVideo': '中文字幕',
    }


class CnSubtitleBoard:
    """ 中文字幕板块 """

    def __init__(self, url):
        self._tmp_content = get_soup(url)
        self.page_num = self.get_page_num()  # 当前页码
        self.page_movie_list = self.get_page_movie_list()  # 当前页码url
        self.movie_num = 0  # 电影总数
        self.next_page = self.get_next_page()

    def get_page_num(self):
        try:
            page_num = self._tmp_content.select_one('div.pg strong').text
            log.debug(f'page num : {page_num}')
            return int(page_num)
        except Exception as e:
            log.error('page num parsing failed!!', e)

    def get_next_page(self):
        try:
            next_page = self._tmp_content.select_one('div.pg a.nxt')['href']
            log.debug(f'next page : {next_page}')
            return next_page
        except Exception as e:
            log.error('next page parsing failed!!', e)

    def get_page_movie_list(self):
        try:
            li = [thread.select_one('a[href^=thread]')['href']
                  for thread in self._tmp_content.select('tbody[id^="normalthread_"]')]
            log.debug(f'page movie list : {li}')
            return li
        except Exception as e:
            log.error(f'page movie list parsing failed!!', e)

    def start_crawl(self):
        while self.next_page:
            log.info('collecting cnSub index page: '+self.next_page)
            log.info(self.page_num)
            # for detail_page in self.page_movie_list:
            #     detail = CnSubtitleThread(f'http://{ShtSite.base_url}/{detail_page}')


class CnSubtitleThread:
    """ 中文字幕电影 """

    def __init__(self, url):
        log.debug('=' * 16)
        log.debug(f'crawling {url}')
        self.tmp_content = get_soup(url)
        self.post_id = self.get_post_id()
        self.title = self.get_title()
        self.url = url
        self.actor = self.get_actor()
        self.post_time = self.get_post_time()
        self.mag_link = self.get_mag_link()
        self.tag = self.get_tag()
        self.heat = self.get_heat()
        log.debug('=' * 16)
        log.info(self.__str__())

    def __str__(self):
        info = '\n========= cn sub video info ========= \n'
        for k, v in self.__dict__.items():
            if k != 'tmp_content':
                if not k == 'post_time':
                    info += f'{k:<10} : {v:<100} \n'
                else:
                    info += f'{k:<10} : {time.strftime("%Y-%m-%d %H:%M:%S", v):<100} \n'
        info += '======================================='
        return info

    def get_post_id(self):
        try:
            post_id = str.split(self.tmp_content.select_one('div[id^=post_]')['id'], '_')[-1]
            log.debug(f'post id : {post_id}')
            return post_id
        except Exception as e:
            log.error("post id parsing failed", e)

    def get_title(self):
        try:
            title = self.tmp_content.select_one('#thread_subject').text
            log.debug(f"title: {title}")
            return title
        except Exception as e:
            log.error('title parsing failed!!', e)

    def get_post_time(self):
        try:
            time_str = self.tmp_content.select_one(f'#authorposton{self.post_id} span')['title']
            post_time = time.strptime(time_str, '%Y-%m-%d %H:%M:%S')
            log.debug(f'post time : {time.strftime("%Y-%m-%d %H:%M:%S", post_time)}')
            return post_time
        except Exception as e:
            log.error('post time parsing failed!!', e)

    def get_tag(self):
        try:
            tag = self.tmp_content.select_one('h1.ts a').text.replace('[', '').replace(']', '')
            log.debug(f'tag : {tag}')
            return tag
        except Exception as e:
            log.error('tag parsing failed!!', e)

    def get_mag_link(self):
        try:
            mag_link = self.tmp_content.select_one('div[id^="code_"] li').text
            log.debug(f'mag link : {mag_link}')
            return mag_link
        except Exception as e:
            log.error('mag link parsing error!!', e)

    def get_heat(self):
        try:
            heat = self.tmp_content.select_one('span.xi1').text
            log.debug(f'heat : {heat}')
            return int(heat)
        except Exception as e:
            log.error('heat parsing error!!', e)

    def get_actor(self):
        try:
            post = self.tmp_content.select_one(f'#postmessage_{self.post_id}').text.split('\n')
            actor = [line.split("：")[-1].strip() for line in post if re.search("女优", line)][0]
            log.debug(f'actor : {actor}')
            return actor
        except Exception as e:
            log.error('actor parsing error', e)


if __name__ == '__main__':
    pass
