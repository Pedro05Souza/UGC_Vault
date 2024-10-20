from models.guild import Guilds

__all__ = (
    'get_guild',
    'create_guild',
    'update_guild'
)

async def get_guild(guild_id: int):
    """
    Get guild data from the database.

    Args:
        id (int): The guild ID.

    Returns:
        Guild: The guild data.
    """
    return await Guilds.filter(id=guild_id).first()

async def create_guild(guild_id: int):
    """
    Create a guild in the database.

    Args:
        id (int): The guild ID.

    Returns:
        bool: Whether the guild was created.
    """
    await Guilds.create(id=guild_id)

async def update_guild(guild_id: int, **kwargs):
    """
    Update a guild in the database.

    Args:
        id (int): The guild ID.
        **kwargs: The fields to update.

    Returns:
        bool: Whether the guild was updated.
    """
    return await Guilds.filter(id=guild_id).update(**kwargs)