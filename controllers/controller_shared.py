from tortoise.transactions import in_transaction

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
            return False
