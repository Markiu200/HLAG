import logging
import sys


class PrintLogger(logging.Logger):
    def __init__(self, *args):
        super().__init__(*args)

    def critical(self, msg: str, *args):
        super().critical(msg, *args)
        sys.stderr.write(msg)

    def error(self, msg: str, *args):
        super().error(msg, *args)
        sys.stderr.write(msg)

    def warning(self, msg: str, *args):
        super().warning(msg, *args)
        sys.stdout.write(msg)

    def info(self, msg: str, *args):
        super().info(msg, *args)
        sys.stdout.write(msg)