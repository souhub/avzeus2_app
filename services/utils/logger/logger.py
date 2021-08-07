import logging
import os
import yaml
from utils.env import APP_ENV


def get_logger(name: str = '', log_dir: str = '/var/log/app'):
    base = os.path.dirname(os.path.abspath(__file__))

    # 環境によって読み込ませる設定ファイルを変更
    if APP_ENV == 'development':
        conf_file = os.path.join(base, 'logger.dev.yml')
    else:
        conf_file = os.path.join(base, 'logger.yml')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        logfile = f'{log_dir}/app.log'
        open(logfile, 'w')

    with open(conf_file, 'r') as f:
        logging.config.dictConfig(yaml.safe_load(f))

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    return logger
