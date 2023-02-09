import os
import logging

log_path = "logs/"


def configure_logger(log_filename):

    # Create the directory structure if it doesn't exist
    log_dir = os.path.dirname(log_filename)
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
