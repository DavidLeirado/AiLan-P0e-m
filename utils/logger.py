import logging.config

import logging
import os

from dotenv import load_dotenv


class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    # Color codes
    green = "\033[0;32m"
    purple = "\033[0;35m"
    yellow = "\033[1;33m"
    red = "\033[0;31m"
    bold_red = "\033[1;31m"
    reset = "\x1b[0m"

    # Lines to format
    format = "%(asctime)s - %(levelname)s - %(message)s"

    # Custom format dictionary
    FORMATS = {
        logging.DEBUG: purple + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        """ Method to return the specific format"""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class Logger:
    """
    My custom Logger class
    """
    # Instantiate the formatter and retrieving logger
    load_dotenv()
    formatter = CustomFormatter()

    logger = logging.getLogger(__name__)

    debug = bool(int(os.environ.get("DEBUG", 0)))

    # Setting debug level
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # Getting stream handler
    ch = logging.StreamHandler()

    # Setting SH debug lvl
    if debug:
        ch.setLevel(logging.DEBUG)
    else:
        ch.setLevel(logging.INFO)

    # Setting formatter and adding SH to logger
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    @classmethod
    def debug(cls, msg, module=__file__):
        """Print debug msg"""
        cls.logger.debug(msg)

    @classmethod
    def info(cls, msg):
        """Print info msg"""
        cls.logger.info(msg)

    @classmethod
    def warning(cls, msg):
        """Print warning msg"""
        cls.logger.warning(msg)

    @classmethod
    def error(cls, msg):
        """Print error msg"""
        cls.logger.error(msg)

    @classmethod
    def critical(cls, msg):
        """Print critical error msg"""
        cls.logger.critical(msg)


if __name__ == "__main__":
    Logger.debug("Aquí funciona")
    Logger.info("Aquí va")