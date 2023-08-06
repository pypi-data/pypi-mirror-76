import logging
import os

from pyunique import LOGGER_NAME


def get_logger():
    return logging.getLogger(LOGGER_NAME)


def get_number_of_files(folder: str) -> int:
    count = 0
    for root, directories, files in os.walk(folder):
        count += len(files)
    return count
