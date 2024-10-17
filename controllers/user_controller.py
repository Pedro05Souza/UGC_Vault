from models.user import User
from typing import Optional


__all__ = (
    'get_user',
    'create_user',
    'update_user',
    'get_user_balance',
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