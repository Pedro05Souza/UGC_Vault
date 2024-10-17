"""
This module contains the decorators for the core of the application.
"""
from config import CAN_LOG, ADMIN_IDS
from core.tools.lib import send_bot_embed
from discord.ext.commands import check
from controllers import get_user, create_user

__all__ = (
    'economy_handler',
    'check_logging',
    'admin_only',
)

def economy_handler(user_data = False, guild_config_data = False):
    """
    Decorator that handles the economy data.

    Args:
        user_data (bool): Whether the function requires user data.
        guild_config_data (bool): Whether the function requires guild config data.

        They will both be queried from the database and passed as arguments to the function.

    Returns:
        Decorator: The decorator.
    """
    async def predicate(ctx):
        if user_data:
            user = await get_user(ctx.author.id)

            if not user:
                user = await create_user(ctx.author.id)

            ctx.user_data = user

        return True
    return check(predicate)

def check_logging():
    def wrapper(func):
        async def wrapped(*args, **kwargs):
            if CAN_LOG:
                return await func(*args, **kwargs)
        return wrapped
    return wrapper

def admin_only():
    """
    Decorator that checks if the user is an admin.

    Returns:
        Decorator: The decorator.
    """
    def predicate(ctx):
        if ctx.author.id in ADMIN_IDS:
            return True
        return False
    return check(predicate)
