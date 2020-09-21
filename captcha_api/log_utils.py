import logging
import sys


def configure_logging():
    """Logging setup"""
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s"
    )

    # adds console handler to logger instance the first time this code is called
    # avoids adding extra handlers to the instance, which causes duplicate logs msgs
    if not len(logger.handlers):
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        logger.addHandler(console)

    # Requests logs some stuff at INFO that we don't want
    # unless we have DEBUG
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.ERROR)
    return logger
