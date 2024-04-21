# Cabin Zhu, 2023

import logging
import inspect
import datetime
from pathlib import Path

# LOG_FMT_MSG = '[{asctime}][{levelname:<8}][{filename}][{funcName}()] {message}'
LOG_FMT_MSG = '[%(asctime)s][%(levelname)-8s][%(filename)s][%(funcName)s()] %(message)s'
LOG_FMT_TIMESTAMP = '%Y-%m-%d %H:%M:%S'

# Define ANSI escape sequences for different colors
COLORS = {
    'black': '\033[0;30m',
    'red': '\033[0;31m',
    'green': '\033[0;32m',
    'yellow': '\033[0;33m',
    'blue': '\033[0;34m',
    'magenta': '\033[0;35m',
    'cyan': '\033[0;36m',
    'white': '\033[0;37m',
    'reset': '\033[0m'
}

# Define a dictionary mapping logging levels to colors
LEVEL_COLORS = {
    logging.DEBUG: COLORS['blue'],
    logging.INFO: COLORS['reset'],
    logging.WARNING: COLORS['yellow'],
    logging.ERROR: COLORS['red'],
    logging.CRITICAL: COLORS['magenta']
}


# Create a custom formatter class for colorized logging
class ColorFormatter(logging.Formatter):
    def format(self, record):
        # Get the color associated with the log level
        level_color = LEVEL_COLORS.get(record.levelno, COLORS['reset'])
        # Colorize the log msg
        return level_color + super().format(record)


def get_logger(name=None, level='INFO', dump_dir=None):
    """Retrieve a colorized python built-in logging logger (with optional file dump).

    Args:
        name (str): Name of the logger,
            which will also be used as a part of the dump file name.
        level (str): Logging level of the logger, case-agnostic. Default as 'INFO'
        dump_dir (str): Path to the dump file of the log.
            Default as None, meaning that no dump file will be generated.
    """

    def _get_logging_lv(s_lv):
        s2level = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        s_lv = s_lv.upper()
        if s_lv in s2level:
            return s2level[s_lv]
        else:
            raise ValueError(f'Invalid string for logging level: "{s_lv}"')

    # Decode args.
    if name is None:
        frame = inspect.currentframe().f_back
        name = inspect.getmodule(frame).__name__
    level = _get_logging_lv(level)
    # Create a logger for configuration.
    configured_logger = logging.getLogger(name)
    configured_logger.setLevel(level)
    # Create a colorized formatter and set it on the console handler
    color_formatter = ColorFormatter(fmt=LOG_FMT_MSG, datefmt=LOG_FMT_TIMESTAMP)
    # Handlers.
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)
    configured_logger.addHandler(console_handler)
    if dump_dir is not None:
        dump_dir = Path(dump_dir)
        if not dump_dir.is_dir():
            if not dump_dir.exists():
                configured_logger.warning(f'The given log directory path does NOT exist: {dump_dir.absolute()}')
            else:
                configured_logger.warning(f'The given log directory path is NOT a dir: {dump_dir.absolute()}')

            dump_dir = Path('./log')
            dump_dir.mkdir(exist_ok=True)
            configured_logger.warning(f'Redirected the log directory to {dump_dir.absolute()}')
        time_stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        log_file = dump_dir / f'{configured_logger.name}-{time_stamp}.log'
        log_file.touch()
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(fmt=LOG_FMT_MSG, datefmt=LOG_FMT_TIMESTAMP))
        configured_logger.addHandler(file_handler)
        
        configured_logger.dump_path = log_file

    return configured_logger


if __name__ == '__main__':
    logger = get_logger()
    # Log messages with different levels
    logger.debug("This is a debug message")
    logger.info(f"The logger name is : {logger.name}")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    