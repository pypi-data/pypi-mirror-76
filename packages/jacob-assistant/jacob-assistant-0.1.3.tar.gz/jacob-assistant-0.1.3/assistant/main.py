import logging
from assistant.bot import assistant_bot
from assistant.spider import sht
from assistant.config import CONFIG

log = logging.getLogger(__name__)


def start_crawl():
    board = sht.CnSubtitleBoard('https://www.sehuatang.org/forum-103-1.html')


def main():
    logging.basicConfig(level=CONFIG.log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    assistant_bot.init_bot(CONFIG.bot_token, CONFIG.proxy())


if __name__ == '__main__':
    main()
