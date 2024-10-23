import aiohttp

async def get_item_by_id(id: int):
    """
    Gets a roblox item's information by its ID.

    Args:
        id (int): The item ID.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://economy.roblox.com/v2/assets/{id}/details") as response:
            return await response.json()
        
async def get_item_image_by_id(id: int):
    """
    Gets a roblox item's image by its ID.

    Args:
        id (int): The item ID.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={id}&size=150x150&format=Png&isCircular=false") as response:
            return await response.json()