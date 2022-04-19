# logging tool for module debug

from datetime import datetime
import logging
import logging.handlers
import os
import pathlib

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s:%(message)s')


def get_timestamp():
    return (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))


def log_init(
        name=__name__,
        loglevel=logging.DEBUG,
        handler=logging.StreamHandler()):
    handler.setFormatter(formatter)
    _logger = logging.getLogger(name)
    _logger.addHandler(handler)
    _logger.setLevel(loglevel)
    return _logger


def get_logger(
    log_path: str,
    log_level: str = logging.INFO,
    log_files: int = 2,
    log_size: int = 10,
):
    ret_path = os.path.split(log_path)
    pathlib.Path(ret_path[0]).mkdir(
        parents=True,
        exist_ok=True
    )
    handlers = logging.handlers.RotatingFileHandler(
        log_path, mode='a',
        maxBytes=log_size*1024*1024, backupCount=log_files)
    logger = log_init(loglevel=log_level, handler=handlers)
    return logger
