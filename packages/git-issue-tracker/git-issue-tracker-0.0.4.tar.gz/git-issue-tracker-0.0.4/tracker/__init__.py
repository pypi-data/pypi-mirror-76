import logging
import logging.config
import os

import yaml


def setup_logging(
        default_path='/logging.yaml',
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration\n
    To override path on env define LOG_CFG properties with absolute path
    """
    path = os.getcwd() + default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


setup_logging()
