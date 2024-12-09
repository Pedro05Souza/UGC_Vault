"""
This module contains the settings for the application.
"""

# General settings

BOT_PREFIX = "$"  # The prefix for the bot commands
CAN_LOG = True  # Sets whether the bot can log messages or not
ADMIN_IDS = {
    668666843900149791,
    361197580815958026,
}  # The IDs of the bot administrators (separator: ,)


# Command settings

MAX_SLOTS = 3  # The maximum amount of slots that can be played at once
MAX_COINFLIP = 4000  # The maximum amount that can be bet on a coinflip
DEFAULT_CLAIM_COOLDOWN = 1800  # The default cooldown for claiming rewards (in seconds)

# Database settings

DEFAULT_PAGE_SIZE = 10  # The default page size for pagination
