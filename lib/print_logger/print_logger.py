import logging
import sys


class PrintLogger:
    def __init__(self):
        self.stream_stdout_handler = logging.StreamHandler(sys.stdout)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            handlers=[
                logging.FileHandler("logs.log"),
                self.stream_stdout_handler,
            ]
        )
        self.logger = logging.getLogger(__name__)

    def critical(self, *args):
        self.logger.critical(*args)

    def error(self, *args):
        self.logger.error(*args)

    def warning(self, *args):
        self.logger.warning(*args)

    def info(self, *args):
        self.logger.info(*args)


if __name__ == '__main__':
    logger = PrintLogger()
    logger.info("Info")
    logger.critical("Critical")
    logger.warning("Warning")
    logger.error("Error")
