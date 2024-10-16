"""
This module contains the function to retrieve the connection pool for the database.
"""
import asyncpg
import os
import dotenv

dotenv.load_dotenv()

__all__ = ['retrieve_connection_pool']

password = os.getenv('DB_PASSWORD')

conn = None

async def retrieve_connection_pool() -> asyncpg.pool.Pool:
    """
    This function retrieves the connection pool for the database.

    Returns:
        asyncpg.pool.Pool: The connection pool
    """
    global conn

    if not conn:
        conn = await asyncpg.create_pool(
            host='localhost',
            database='ugc_database',
            user='postgres',
            password=password,
            port=5432
        )
    return conn