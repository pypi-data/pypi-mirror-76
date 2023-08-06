import logging
from logging.handlers import RotatingFileHandler
import traceback
import datetime


class RLogger(object):

    logger = logging.getLogger('rlogger')
    log_level = logging.INFO
    logger.setLevel(logging.INFO)

    log_file_handler = None
    log_stream_handler = None

    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    @classmethod
    def init(cls,
             log_file,
             enable_screen=True,
             log_level='INFO',
             max_bytes=1e8,
             backup_count=1):
        if log_level == 'DEBUG':
            cls.set_level(cls.DEBUG)
        elif log_level == 'INFO':
            cls.set_level(cls.INFO)
        elif log_level == 'WARNING':
            cls.set_level(cls.WARNING)
        elif log_level == 'ERROR':
            cls.set_level(cls.ERROR)

        if cls.log_file_handler not in cls.logger.handlers:
            formatter = logging.Formatter(
                '%(name)s-%(levelname)s %(asctime)s: %(message)s')
            cls.log_file_handler = RotatingFileHandler(
                log_file,
                mode='a',
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8',
            )
            cls.log_file_handler.setFormatter(formatter)
            cls.logger.addHandler(cls.log_file_handler)
        if enable_screen is True:
            if cls.log_stream_handler not in cls.logger.handlers:
                cls.log_stream_handler = logging.StreamHandler()
                cls.log_stream_handler.setFormatter(formatter)
                cls.logger.addHandler(cls.log_stream_handler)
        cls.logger.propagate = False

    @classmethod
    def set_level(cls, level):
        cls.logger.setLevel(level)

    @classmethod
    def log(cls, message, level=None):
        name = traceback.extract_stack()[-2][0]
        cls.logger.name = name.split('/')[-1][:-3]
        if level is None:
            cls.logger.log(cls.INFO, message)
        else:
            cls.logger.log(level, message)

    @classmethod
    def close(cls):
        handlers = cls.logger.handlers[:]
        for handler in handlers:
            cls.logger.removeHandler(handler)
