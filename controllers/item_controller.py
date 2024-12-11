from config import DEFAULT_PAGE_SIZE
from models import Item, Codes
from tortoise.functions import Count
from asyncio import Lock
from core.tools import log_info

lock = Lock()

__all__ = (
    "get_item_by_roblox_id",
    "create_item",
    "delete_item",
    "add_item_code",
    "get_code_count",
    "update_item_price",
    "search_item",
    "get_code_from_item",
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

async def search_item(
    item_name: str = None,
    item_price: int = None,
    item_category: str = None,
    pageIdx: int = 0,
) -> tuple[list[dict], bool]:
    """
    Function that searches for an item by its name, price or category.

    Args:
        item_name (str): The name of the item.
        item_price (int): The price of the item.
        item_category (str): The category of the item.
        pageIdx (int): The page index.

    Returns:
        dict: The item.
    """
    offset = pageIdx * DEFAULT_PAGE_SIZE
    
    filters = {}
    
    if item_name is not None:
        filters['item_name'] = item_name
    if item_price is not None:
        filters['item_price__lte'] = item_price
    if item_category is not None:
        filters['item_category'] = item_category
        
    item_list = (
        await Item.filter(**filters)
        .annotate(code_count=Count("codes"))
        .filter(code_count__gt=0)
        .offset(offset)
        .limit(DEFAULT_PAGE_SIZE + 1)
        .values("item_id", "item_name", "item_description", "item_price", "item_category", "code_count")
    )
    
    has_more = False
    
    if len(item_list) > DEFAULT_PAGE_SIZE:
        has_more = True
        item_list = item_list[:-1]

        
    return item_list, has_more

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
        return None