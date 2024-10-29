from models import Item, Codes

__all__ = (
    'get_item_by_roblox_id',
    'create_item',
    'delete_item',
    'add_item_code'
)

async def get_item_by_roblox_id(item_id: int):
    """
    Function that retrieves an item by its roblox ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        dict: The item.
    """
    return await Item.filter(item_id=item_id).first().values()

async def create_item(item_id: int, item_name: str, item_description: str, item_price: int):
    """
    Function that creates an item to the database.

    Args:
        item_id (int): The ID of the item.
        item_name (str): The name of the item.
        item_description (str): The description of the item.
        item_price (int): The price of the item.

    Returns:
        None
    """
    await Item.create(item_id=item_id, item_name=item_name, item_description=item_description, item_price=item_price)
    return

async def delete_item(item_id: int):
    """
    Function that deletes an item from the database.

    Args:
        item_id (int): The ID of the item.

    Returns:
        None
    """
    await Item.filter(item_id=item_id).delete()
    return

async def add_item_code(item_id: int, codes: list[str]):
    """
    Function that adds a code to an item.

    Args:
        item_id (int): The ID of the item.
        code (list[str]): The code.

    Returns:
        None
    """
    item = await Item.filter(item_id=item_id).first()

    if item:
        code_objects = [Codes(item=item, code=code) for code in codes]
        await Codes.bulk_create(code_objects)
    return