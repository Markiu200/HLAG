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

    def set_level(self, level: int):
        self.logger.setLevel(level)

    def set_level_by_name(self, level: str):
        if level.lower() == "debug":
            self.set_level(10)
        elif level.lower() == "info":
            self.set_level(20)
        elif level.lower() == "warning":
            self.set_level(30)
        elif level.lower() == "error":
            self.set_level(40)
        elif level.lower() == "critical":
            self.set_level(50)

    def critical(self, *args):
        self.logger.critical(*args)

    def error(self, *args):
        self.logger.error(*args)

    def warning(self, *args):
        self.logger.warning(*args)

    def info(self, *args):
        self.logger.info(*args)

    def debug(self, *args):
        self.logger.debug(*args)


if __name__ == '__main__':
    logger = PrintLogger()
    logger.info("Info")
    logger.critical("Critical")
    logger.warning("Warning")
    logger.error("Error")
