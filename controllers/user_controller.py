from models import User, CommandsTimestamp
from typing import Optional
from datetime import datetime

__all__ = (
    'get_user',
    'create_user',
    'update_user',
    'get_user_balance',
    'get_command_timestamp',
    'create_command_timestamp',
    'update_command_timestamp'
)

async def get_user(id: int) -> Optional[User]:
    """
    Get user data from the database.

    Args:
        id (int): The user ID.

    Returns:
        User: The user data.
    """
    return await User.filter(id=id).first()

async def create_user(id: int) -> User:
    """
    Create a user in the database.

    Args:
        id (int): The user ID.

    Returns:
        bool: Whether the user was created.
    """
    await User.create(id=id)

async def update_user(id: int, **kwargs) -> bool:
    """
    Update a user in the database.

    Args:
        id (int): The user ID.
        **kwargs: The fields to update.

    Returns:
        bool: Whether the user was updated.
    """
    return await User.filter(id=id).update(**kwargs)

async def get_user_balance(id: int) -> Optional[int]:
    """
    Get the balance of a user.

    Args:
        id (int): The user ID.

    Returns:
        int: The balance.
    """
    user = await get_user(id)
    return user.balance if user else None

async def get_command_timestamp(user_id: int, command_name: str) -> None:
    """
    Gets the timestamp of a command.

    Args:
        user_id (int): The user ID.
        command_name (str): The command name.

    Returns:
        datetime: The timestamp.
    """
    querySet = await CommandsTimestamp.filter(user_id=user_id, command_name=command_name).first()

    if not hasattr(querySet, 'timestamp'):
        return None
    
    return querySet.timestamp

async def create_command_timestamp(user_id: int, command_name: str) -> None:
    """
    Creates a command timestamp.

    Args:
        user_id (int): The user ID.
        command_name (str): The command name.

    Returns:
        bool: Whether the command timestamp was created.
    """
    user = await get_user(user_id)
    await CommandsTimestamp.create(user_id=user, command_name=command_name)

async def update_command_timestamp(user_id: int, command_name: str) -> bool:
    """
    Updates a command timestamp.

    Args:
        user_id (int): The user ID.
        command_name (str): The command name.

    Returns:
        bool: Whether the command timestamp was updated.
    """
    return await CommandsTimestamp.filter(user_id=user_id, command_name=command_name).update(timestamp=datetime.now())