"""
This module sets up the logger for the bot.
"""
from colorlog import ColoredFormatter
import logging

__all__ = ['bot_logger']

def setup_logging() -> logging.Logger:
    """
    Setup the logger for the bot.

    Returns:
        logging.Logger: The logger object.
    """
    logger = logging.getLogger('bot')
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s - %(levelname)-8s%(reset)s - %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "purple",
            },
        )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

bot_logger = setup_logging()