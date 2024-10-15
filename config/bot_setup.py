from discord import Intents
from dotenv import load_dotenv
from config.settings import BOT_PREFIX
from discord.ext.commands import Bot
from pathlib import Path
from core.tools import log_info
import os

__all__ = (
    'setup_intents',
    'setup_prefix',
    'setup_token',
    'setup_bot',
    'load_cogs'
)

def setup_intents() -> Intents:
    """
    This function sets up the intents for the bot.

    Returns:
        Intents: The intents that the bot will use.
    """
    intents = Intents.default()
    intents.members = True
    intents.voice_states = True
    intents.messages = True
    intents.message_content = True
    intents.guilds = True
    return intents

def setup_prefix() -> str:
    """
    This function sets up the prefix for the bot.

    Returns:
        str: The prefix that the bot will use
    """
    return BOT_PREFIX

def setup_token() -> str:
    """
    This function retrieves the bot token from the environment.

    Returns:
        str: The bot token.
    """
    load_dotenv()
    return os.getenv('DISCORD_TOKEN')

def setup_bot() -> Bot:
    """
    This function sets up the bot.

    Returns:
        Bot: The bot object.
    """
    return Bot(command_prefix=setup_prefix(), intents=setup_intents())

async def load_cogs(bot: Bot) -> None:
    """
    This function loads the cogs for the bot.

    Args:
        bot (Bot): The bot object.
    """
    cogs_dir = Path('./core/cogs')

    for filepath in cogs_dir.rglob('*.py'):

        if filepath.stem == '__init__':
            continue

        module_path = filepath.relative_to(cogs_dir).with_suffix('').as_posix().replace('/', '.')
        await bot.load_extension(f'core.cogs.{module_path}')
        log_info(f'Loaded cog: {module_path}')