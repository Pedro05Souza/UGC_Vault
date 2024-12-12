"""
This module contains the decorators for the core of the application.
"""

from config import CAN_LOG, ADMIN_IDS
from core.tools.lib import send_bot_embed, retrieve_application_emoji
from discord.ext.commands import check
from contextlib import suppress
from repositories import get_user, create_user, get_guild, create_guild

__all__ = (
    "economy_handler",
    "check_logging",
    "admin_only",
)

def economy_handler(user_data=True, guild_data=True, booster_command=False):
    """
    Decorator that handles the economy data.

    Args:
        user_data (bool): Whether the function requires user data.
        guild_config_data (bool): Whether the function requires guild config data.
        booster_command (bool): Whether the function is a booster command.

    Returns:
        Decorator: The decorator.
    """

    async def predicate(ctx):

        if guild_data:
            guild_config = await get_guild(ctx.guild.id)

            if not guild_config:
                guild_config = await create_guild(ctx.guild.id)

            if ctx.channel.id not in guild_config.allowed_channels:
                return False

        if user_data:
            user = await get_user(ctx.author.id)

            if not user:
                user = await create_user(ctx.author.id)

            if booster_command:
                if not ctx.author.premium_since:
                    await send_bot_embed(
                        ctx,
                        description=f"{await retrieve_application_emoji(emoji_name='booster', emoji_id='1297349785442979881')} You must be a server booster to claim this reward.",
                    )
                    return False

            ctx.user_data = user
        return True

    with suppress(Exception):
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
