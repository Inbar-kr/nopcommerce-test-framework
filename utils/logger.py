import logging
import os


def setup_logger(log_file="test_log.log", log_level=logging.DEBUG):
    """Set up a logger with both file and console handlers."""
    logger = logging.getLogger("TestLogger")

    # Avoid adding duplicate handlers
    if logger.hasHandlers():
        return logger

    logger.setLevel(log_level)

    # Create a file handler to log messages to a file
    log_file_path = os.getenv("LOG_FILE_PATH", log_file)
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level)

    # Create a console handler to display messages on the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create a formatter and attach it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger