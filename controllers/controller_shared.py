from tortoise.transactions import in_transaction
from core.tools import log_error

__all__ = ['execute_transactions']

async def execute_transactions(*callbacks) -> bool:
    """
    Execute a series of transactions.

    Args:
        *callbacks: The callbacks to execute

    Returns:
        bool: Whether the transactions were successful.
    """
    async with in_transaction() as conn:
        try:
            for callback in callbacks:
                await callback()
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            log_error(f"An error occurred while executing transactions: {e}")
            return False
