"""
Module for escape repeating code, creating loggers in another modules.
Log files are created in the folder named 'logs' by default.

Message format:
[{logger_name}:{level}:{func_name}:{time}] {message}

Date format:
day.month.year hours:minutes:seconds

"""

__all__ = (
    'create_logger', 'create_formatter',
    'create_file_handler', 'create_stream_handler')

import logging
from pathlib import Path


DEFAULT_MSG_FMT = "[{name}:{levelname}:{funcName}:{asctime}] {message}"
DEFAULT_DATE_FMT = "%d.%m.%Y %H:%M:%S"

LOG_FOLDER = Path('logs')
try:
    LOG_FOLDER.mkdir()
except FileExistsError:
    pass


def create_formatter(message_format: str = DEFAULT_MSG_FMT,
                     date_format: str = DEFAULT_DATE_FMT,
                     style: str = '{') -> logging.Formatter:
    """ Create message formatter.

    :param message_format: str, way to format message.
    :param date_format: str, way to format date.
     Str with %, because it needed for time.strftime()
    :param style: str, % or {. Whether message_format
     contains % or { way to format.
    :return: logging.Formatter.
    """
    formatter = logging.Formatter(
        fmt=message_format,
        datefmt=date_format,
        style=style
    )
    return formatter


def create_stream_handler(level=logging.WARNING,
                          formatter=None) -> logging.StreamHandler:
    """ Create stream handler.

    :param level: handler level. WARNING by default.
    :param formatter: message formatter. None by default.
    :return: stream handler.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    formatter = formatter or create_formatter()
    stream_handler.setFormatter(formatter)

    return stream_handler


def create_file_handler(level=logging.DEBUG,
                        log_path: str = None,
                        formatter=None,
                        **kwargs) -> logging.FileHandler:
    """ Create file handler.

    :param level: handler level.
    :param log_path: str, log file path.
    :param formatter: message formatter.
    :param kwargs: params to FileHandler constructor.
    :keyword delay: bool, whether file'll not be opened
     until the first logger calling. True by default.
    :keyword encoding: str, file encoding. utf-8 by default.
    :return: file handler.
    """
    delay = kwargs.pop('delay', True)
    encoding = kwargs.pop('encoding', 'utf-8')

    file_handler = logging.FileHandler(
        log_path, delay=delay, encoding=encoding, **kwargs)
    file_handler.setLevel(level)
    formatter = formatter or create_formatter()
    file_handler.setFormatter(formatter)

    return file_handler


def create_logger(module_name: str,
                  level=logging.DEBUG,
                  *handlers) -> logging.Logger:
    """ Create logger.

    :param module_name: str, name of logger.
    :param level: level of logger.
    :param handlers: handlers to be added to the logger.
    :return: logger.
    """
    logger = logging.getLogger(module_name)
    logger.setLevel(level)

    path = LOG_FOLDER / f"{module_name}.log"

    default_handlers = [
        create_stream_handler(),
        create_file_handler(log_path=path)
    ]
    handlers = handlers or default_handlers

    for handler in handlers:
        logger.addHandler(handler)

    return logger
