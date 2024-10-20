
from discord import Interaction, app_commands

__all__ = [
    "color_autocomplete", "coinflip_autocomplete"
    ]


async def color_autocomplete(
        interaction: Interaction, current_choice: str
    ) -> list[app_commands.Choice]:
    colors = ["Red", "Black", "Green"]
    return [
        app_commands.Choice(name=color, value=color)
        for color in colors if current_choice.lower() in color.lower()
    ]

async def coinflip_autocomplete(
        interaction: Interaction, current_choice: str
    ) -> list[app_commands.Choice]:
    sides = ["Heads", "Tails"]
    return [
        app_commands.Choice(name=side, value=side)
        for side in sides if current_choice.lower() in side.lower()
    ]