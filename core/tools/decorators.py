from config import retrieve_connection_pool, CAN_LOG, ADMIN_IDS
from core.tools.lib import send_bot_embed
from discord.ext.commands import check

__all__ = (
    'extract_connection_pool',
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
    from controller import get_user, create_user

    async def predicate(ctx):
        if user_data:
            user = await get_user(ctx.author.id)

            if not user:
                await send_bot_embed(ctx, description=f":no_entry_sign: **{ctx.author.display_name}** is not registered. Try any command again.")
                await create_user(ctx.author.id)

            ctx.user_data = user

        return True
    return check(predicate)

def extract_connection_pool():
    """
    Decorator that extracts the connection pool.

    Returns:
        callable: The wrapper.
    """
    def wrapper(func):
        async def wrapped(*args, **kwargs):
            conn = await retrieve_connection_pool()
            return await func(*args, conn=conn, **kwargs)
        return wrapped
    return wrapper

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
