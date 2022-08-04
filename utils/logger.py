import logging.config

import logging


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
    format = "%(asctime)s - %(name)s [%(levelname)s]: %(message)s"

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
    def __init__(self, debug=False, name=""):

        # Instantiate the formatter and retrieving logger
        self.formatter = CustomFormatter()
        self.logger = logging.getLogger(name)

        # Setting debug level
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        # Getting stream handler
        self.ch = logging.StreamHandler()

        # Setting SH debug lvl
        if debug:
            self.ch.setLevel(logging.DEBUG)
        else:
            self.ch.setLevel(logging.INFO)

        # Setting formatter and adding SH to logger
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)

    def debug(self, msg):
        """Print debug msg"""
        self.logger.debug(msg)

    def info(self, msg):
        """Print info msg"""
        self.logger.info(msg)

    def warning(self, msg):
        """Print warning msg"""
        self.logger.warning(msg)

    def error(self, msg):
        """Print error msg"""
        self.logger.error(msg)

    def critical(self, msg):
        """Print critical error msg"""
        self.logger.critical(msg)


if __name__ == "__main__":
    logger = Logger(name="Prueba", debug=True)
    logger.debug("Aquí funciona")