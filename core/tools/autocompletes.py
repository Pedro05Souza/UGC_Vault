from discord import Interaction, app_commands
from repositories import get_all_items_with_codes_and_quantity

__all__ = ["color_autocomplete", "ugc_item_auto_complete"]

async def color_autocomplete(
    interaction: Interaction, current_choice: str
) -> list[app_commands.Choice]:
    colors = ["Red", "Black", "Green"]
    return [
        app_commands.Choice(name=color, value=color)
        for color in colors
        if current_choice.lower() in color.lower()
    ]
    
async def ugc_item_auto_complete(
    interaction: Interaction, current_choice: str
) -> list[app_commands.Choice]:
    items = await get_all_items_with_codes_and_quantity()
    return [
        app_commands.Choice(
            name=f"{item["item_name"]}: {item["item_price"]} candies, 📦 stock: {len(item["codes__code"])}",
            value=str(item["item_id"]))
        for item in items
        if current_choice.lower() in item["item_name"].lower()
    ]
    