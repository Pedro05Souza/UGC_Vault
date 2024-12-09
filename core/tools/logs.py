"""
This module contains functions for logging messages.
"""

from core.tools.log_setup import bot_logger


def log_info(message: str) -> None:
    """
    Log an info message.

    Args:
        message (str): The message to log.
    """
    bot_logger.info(message)


def log_error(message: str, exception: Exception) -> None:
    """
    Log an error message.

    Args:
        message (str): The message to log.
    """
    bot_logger.error(message, exc_info=exception)


def log_warning(message: str) -> None:
    """
    Log a warning message.
    """
    bot_logger.warning(message)


def log_critical(message: str) -> None:
    """
    Log a critical message.
    """
    bot_logger.critical(message)
