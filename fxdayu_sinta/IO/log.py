from fxdayu_sinta.IO.config import get_storage, FILES, LOG
import logging
import logging.handlers
import os


root = os.path.join(get_storage()[FILES], LOG)


def log_file(name):
    return os.path.join(root, name)


def get_logger(formatter):
    logger = logging.Logger("logger", logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    return logger


def get_time_rotate(name):
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(module)s %(message)s",
                                  "%Y-%m-%dT%H:%M:%S")

    logger = get_logger(formatter)
    memory = logging.handlers.TimedRotatingFileHandler(log_file(name), 'midnight', backupCount=30)
    memory.setFormatter(formatter)
    logger.addHandler(memory)
    return logger


def get_rotate(name, maxBytes=1024*32):
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(module)s %(message)s",
                                  "%Y-%m-%dT%H:%M:%S")

    logger = get_logger(formatter)
    memory = logging.handlers.RotatingFileHandler(log_file(name), maxBytes=maxBytes)
    memory.setFormatter(formatter)
    logger.addHandler(memory)
    return logger


class TimeRotateLoggerInterface(object):

    NAME = "Log"

    @property
    def logger(self):
        try:
            return globals()[self.NAME]
        except KeyError:
            return globals().setdefault(self.NAME, get_time_rotate(self.NAME))

