import os
from dotenv import load_dotenv
import logging

load_dotenv()

PATH_LOG = os.getenv("LOG_PATH")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with a given name.

    The logger will have a StreamHandler that logs to the console, and a FileHandler
    that logs to the file at the path specified in the LOG_PATH environment variable.
    The logger will log at the INFO level, and the log messages will have the format
    "[%(asctime)-19s] %(levelname)-8s : [%(name)s] : %(message)s".

    Parameters
    ----------
    name : str
        The name of the logger.

    Returns
    -------
    logger : logging.Logger
        The logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(PATH_LOG, mode="w")
    formatter = logging.Formatter(
        "[%(asctime)-19s] %(levelname)-8s : [%(name)s] : %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
