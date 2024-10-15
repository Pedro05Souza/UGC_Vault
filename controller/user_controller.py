"""
This module contains the functions that interact with the database to create, retrieve and update user data.
"""
from models import User
from typing import overload, Optional, Callable, Awaitable
from core.tools import extract_connection_pool, log_warning
from asyncpg.pool import Pool

__all__ = (
    'create_user',
    'get_user',
    'get_user_balance',
    'update_user',
    'execute_transaction',
)

@overload
async def create_user(user_id: int) -> bool:
    """
    Creates a new user in the database.

    Args:
        user_id (int): The user's ID.

    Returns:
        bool: True if the user was created successfully, False otherwise.
    """

@extract_connection_pool()
async def create_user(user_id: int, conn: Pool) -> bool:
    if await is_user_registered(user_id):
        return
    
    async with conn.acquire() as connection:
        result = await connection.execute(
            "INSERT INTO users (user_id, balance) VALUES ($1, 0)",
            user_id
        )
        return result

@extract_connection_pool()
async def is_user_registered(user_id: int, conn: Pool) -> bool:
    """
    Checks if a user is already registered in the database.

    Args:
        user_id (int): The user's ID.
        conn (Pool): The connection pool.

    Returns:
        bool: True if the user is registered, False otherwise.
    """
    async with conn.acquire() as connection:
        result = await connection.fetchval(
            "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = $1)",
            user_id
        )
        return result
    
@overload
async def get_user(user_id: int) -> Optional[User]:
    """
    Retrieves a user from the database.

    Args:
        user_id (int): The user's ID.

    Returns:
        User: The user object.
    """

@extract_connection_pool()
async def get_user(user_id: int, conn: Pool) -> Optional[User]:
    if not await is_user_registered(user_id):
        return
    
    async with conn.acquire() as connection:
        result = await connection.fetchrow(
            "SELECT * FROM users WHERE user_id = $1",
            user_id
        )
        return User(user_id, result['balance'])
    
@overload
async def get_user_balance(user_id: int) -> int:
    """
    Retrieves a user's balance from the database.

    Args:
        user_id (int): The user's ID.

    Returns:
        int: The user's balance.
    """
    
@extract_connection_pool()
async def get_user_balance(user_id: int, conn: Pool) -> int:
    """
    Retrieves a user's balance from the database.

    Args:
        user_id (int): The user's ID.
        conn (Pool): The connection pool.

    Returns:
        int: The user's balance.
    """
    async with conn.acquire() as connection:
        result = await connection.fetchval(
            "SELECT balance FROM users WHERE user_id = $1",
            user_id
        )
        return result
    
@overload
async def update_user(user_id: int, **kwargs) -> bool:
    """
    Updates a user in the database.

    Args:
        user_id (int): The user's ID.
        **kwargs: The fields to update and their new values.

    Returns:
        bool: True if the user was updated successfully, False otherwise.
    """
    
@extract_connection_pool()
async def update_user(user_id: int, conn: Pool, **kwargs):
    if not await is_user_registered(user_id):
        return

    if not await param_validator(**kwargs):
        log_warning(f"Invalid parameters for update_user. Parameters: {kwargs}")
        return
    
    print(kwargs)

    async with conn.acquire() as connection:
        query = "UPDATE users SET "
        query += ', '.join([f"{param} = ${index + 2}" for index, param in enumerate(kwargs.keys())])
        query += f" WHERE user_id = $1"

        result = await connection.execute(
            query,
            user_id,
            *kwargs.values()
        )
        return result

async def param_validator(**kwargs):
    """
    Validates the parameters of the update_user function.

    Args:
        **kwargs: The fields to update and their new values.

    Returns:
        bool: True if the parameters are valid, False otherwise.
    """
    valid_params = User.__slots__
    valid_params = [param.strip('__') for param in valid_params]
    valid_params.remove('user_id')
    return all(param in valid_params for param in kwargs.keys())

@overload
async def execute_transaction(*callbacks: Callable[[], Awaitable[None]]) -> bool:
    """
    Executes a transaction with the given functions.

    Args:
        *callbacks: The functions to execute

    Returns:
        bool: True if the transaction was successful, False otherwise.
    """

@extract_connection_pool()
async def execute_transaction(*callbacks: Callable[[], Awaitable[None]], conn: Pool) -> bool:
    async with conn.acquire() as connection:
        async with connection.transaction():
            for func in callbacks:
                await func()
            return True
    return False