from models import Item, Codes
from asyncio import Lock

lock = Lock()

__all__ = (
    "get_item_by_roblox_id",
    "create_item",
    "delete_item",
    "add_item_code",
    "get_code_count",
    "update_item_price",
    "get_code_from_item",
    'get_all_items_with_codes'
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


async def create_item(
    item_id: int,
    item_name: str,
    item_description: str,
    item_price: int,
    item_category: str,
):
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
    await Item.create(
        item_id=item_id,
        item_name=item_name,
        item_description=item_description,
        item_price=item_price,
        item_category=item_category,
    )
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


async def get_code_count(item_id: int) -> int:
    """
    Function that counts the number of active codes in a specific item.

    Args:
        item_id (int): The ID of the item.

    Returns:
        int: The number of active codes.
    """
    return await Codes.filter(item_id=item_id).count()


async def update_item_price(item_id: int, new_price: int) -> None:
    """
    Function that updates the price of an item.

    Args:
        item_id (int): The ID of the item.
        new_price (int): The new price of the item.

    Returns:
        None
    """
    await Item.filter(item_id=item_id).update(item_price=new_price)

async def get_code_from_item(item_id: int) -> str:
    """
    Function that retrieves a code from an item.

    Args:
        item_id (int): The ID of the item.

    Returns:
        str: The code.
    """
    async with lock:
        code_record = await Codes.filter(item_id=item_id).first().values()
        
        if code_record:
            code = code_record['code']
            await Codes.filter(item_id=item_id, code=code).delete()
            return code
        await Item.filter(item_id=item_id).delete()
        return None
    
async def get_all_items_with_codes():
    """
    Function that retrieves all items with codes.

    Returns:
        list: The items with codes.
    """
    return await Item.filter(codes__isnull=False).distinct().values("item_id", "item_name", "item_price", "item_category")

