import datetime
import json
import logging
from assistant.config import CONFIG
import requests
from telegram.ext import Updater, CommandHandler, CallbackContext

log = logging.getLogger(__name__)


class NXFetchError(Exception):
    pass


def help_command(update, context: CallbackContext):
    """[help命令]

    Args:
        update ():
        context (CallbackContext]): [bot context]
    """
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='''
    指南：
    /nxcx - 检测今天是否打卡
    /chat_id - 检测当前聊天id(仅限管理员)
    /spider - 爬虫管理
    ''')
    log.info('help 命令 执行')


def check_clock_in_command(update, context: CallbackContext):
    if _remind_clock_in():
        context.bot.send_message(chat_id=update.effective_chat.id, text="已经打卡了！")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="还没有打卡！")


def check_chat_id_command(update, context: CallbackContext):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=f'当前chat_id: {chat_id}')


def remind_clock_in_schedule(context: CallbackContext):
    """[宁夏出行打卡提醒]

    Args:
        context (CallbackContext]): [bot_context]
    """
    try:
        if not _remind_clock_in():
            context.bot.send_message(chat_id=CONFIG.announce_channel_id, text='我的宁夏 今天没有打卡哦')

    except Exception as e:
        log.error("我的宁夏打卡信息获取失败", e)
        context.bot.send_message(chat_id=CONFIG.announce_channel_id, text='我的宁夏打卡信息获取失败！！')


def _remind_clock_in():
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; Redmi K30 5G Build/QKQ1.191222.002; wv) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) Version/4.0 Chrome/84.0.4147.111 Mobile Safari/537.36 '
                      'wdnx-android_v1.21.0.0/1.0 ',
        'Content-Type': 'application/json'
    }
    post_data = {"userId": "2a1e10b9-896b-4233-a263-c6bb7e109a1b"}
    url = 'https://hcp.zwfw.nx.gov.cn/gjjkm/business/api/query/records?_t=1597228066&cid='
    response = requests.post(url,
                             data=json.dumps(post_data), verify=False, headers=headers)
    if response.status_code == 200:
        j = response.json()
        return _is_clock_in(j)
    else:
        log.error('我的宁夏打卡信息获取失败')
        raise NXFetchError('我的宁夏打卡信息获取失败！')


def _is_clock_in(res: dict):
    """判断今天的日期是否在已打卡数据中

    :param res 接收到的打卡信息，字典形式:
    :return: bool
    """
    for result in res['result']:
        today = str(datetime.date.today())
        if result['time'] == today:
            log.info('已经打卡了: ' + today)
            return True
        else:
            return False


def init_bot(token: str, proxy: dict = None):
    """
    初始化机器人
    :param token: 机器人密钥
    :param proxy: 本地socks代理
    :return:
    """
    updater = Updater(token=token, use_context=True,
                      request_kwargs=proxy)
    dispatcher = updater.dispatcher
    handlers = {
        'help_handler': CommandHandler('help', help_command),
        'check_clock_in': CommandHandler('nxcx', check_clock_in_command),
        'chat_id': CommandHandler('chat_id', check_chat_id_command)
    }
    for h in handlers:
        dispatcher.add_handler(handlers[h])
    job = updater.job_queue
    job.run_repeating(remind_clock_in_schedule, interval=60 * 60 * 6, first=datetime.datetime(2020, 8, 14))
    updater.start_polling()
