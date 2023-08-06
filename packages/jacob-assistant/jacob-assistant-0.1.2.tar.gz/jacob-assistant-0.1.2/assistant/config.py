import os
import configparser
import logging
import sys

"""
项目配置
"""
log = logging.getLogger(__name__)

_log_level = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR
}


class BaseConfig:
    """
    配置类，根据环境变量 'assistant_env' 切换开发环境(prod)与部署环境(dev)配置文件
    """

    def __init__(self):
        try:
            self.env = os.getenv('assistant_env', 'dev')
            self.basedir = os.path.dirname(__file__)
            self.config_path = self.conf_path()
            config = configparser.ConfigParser()
            config.read(self.config_path)

            self.bot_token = config.get('telegram', 'bot_token')
            self.proxy_on = config.getboolean('proxy', 'proxy')
            self.proxy_url = config.get('proxy', 'url')
            self.log_level = _log_level[config['general']['log_level']]
            self.announce_channel_id = config.get('telegram', 'announce_channel_id')
            self.admin_id = config.get('telegram', 'admin_id')

        except Exception as e:
            log.critical('配置文件读取失败，退出', e)
            log.error('配置文件路径: ' + self.config_path)

    def conf_path(self, path=None):
        """
        :param path: 命令行输入的路径
        :return: 根据生产环境和开发环境返回路径
        """
        if path:
            return path
        else:
            if self.env == 'prod':
                default_path = '/etc/jacob-assistant/prod.ini'
                if os.path.exists(default_path):
                    return default_path
                else:
                    log.critical('配置文件未找到 请配置 /etc/jacob-assistant/prod.ini')
                    sys.exit(2)
            else:
                # 开发环境配置文件路径
                return os.path.join(self.basedir, 'conf', 'dev.ini')

    def proxy(self, tg=True):
        if self.proxy_on:
            if tg:
                # 给TG的代理
                return {'proxy_url': self.proxy_url}
            else:
                # 给requests的代理
                return {
                    'http': self.proxy_url,
                    'https': self.proxy_url
                }


CONFIG = BaseConfig()
