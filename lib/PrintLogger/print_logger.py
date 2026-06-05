import logging
import sys


class PrintLogger:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)

    def print_critical(self, msg):
        self.logger.critical(msg)
        sys.stderr.write(msg)

    def print_error(self, msg):
        self.logger.error(msg)
        sys.stderr.write(msg)

    def print_warning(self, msg):
        self.logger.warning(msg)
        sys.stdout.write(msg)
