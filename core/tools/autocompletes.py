from discord import Interaction, app_commands
from repositories import get_all_items_with_codes

__all__ = ["color_autocomplete", "coinflip_autocomplete", "ugc_item_auto_complete"]


async def color_autocomplete(
    interaction: Interaction, current_choice: str
) -> list[app_commands.Choice]:
    colors = ["Red", "Black", "Green"]
    return [
        app_commands.Choice(name=color, value=color)
        for color in colors
        if current_choice.lower() in color.lower()
    ]

async def coinflip_autocomplete(
    interaction: Interaction, current_choice: str
) -> list[app_commands.Choice]:
    sides = ["Heads", "Tails"]
    return [
        app_commands.Choice(name=side, value=side)
        for side in sides
        if current_choice.lower() in side.lower()
    ]
    
async def ugc_item_auto_complete(
    interaction: Interaction, current_choice: str
) -> list[app_commands.Choice]:
    items = await get_all_items_with_codes()
    return [
        app_commands.Choice(name=item["item_name"], value=str(item["item_id"]))
        for item in items
        if current_choice.lower() in item["item_name"].lower()
    ]