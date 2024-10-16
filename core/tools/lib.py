"""
This module contains the tools that are used in the bot.
"""
from discord import Embed
from discord import Interaction
from discord.ext.commands import Context

__all__ = (
    'send_bot_embed',
    'retrieve_application_emoji',
)

async def send_bot_embed(ctx: Context, thumbnail = None, footer_text: str = "", color="FFC5D3", ephemeral=False, **kwargs) -> None:
    """
    Function that makes the application send an embed message.

    Args:
        ctx (Context): The context of the command.
        thumbnail (str): The URL of the thumbnail.
        footer_text (str): The text that will be displayed in the footer.
        ephemeral (bool): Whether the message should be ephemeral or not.
        **kwargs: The keyword arguments that will be passed to the embed builder.

    Returns:
        None
    """
    embed = await embed_builder(**kwargs)
    embed.color = int(color, 16)
    
    if footer_text != "":
        embed.set_footer(text=footer_text)

    if isinstance(ctx, Interaction):
        if not ctx.response.is_done():
            return await ctx.response.send_message(embed=embed, ephemeral=ephemeral)
        return await ctx.followup.send(embed=embed, ephemeral=ephemeral)
    return await ctx.send(embed=embed)

async def retrieve_application_emoji(emoji_name: str, emoji_id, is_animated=False) -> str:
    """
    Function that retrieves an emoji from the bot's application.

    Args:
        emoji_name (str): The name of the emoji.
        emoji_id (int): The ID of the emoji.
        is_animated (bool): Whether the emoji is animated or not.

    Returns:
        str: The emoji.
    """
    if is_animated:
        return f"<a:{emoji_name}:{emoji_id}>"
    return f"<:{emoji_name}:{emoji_id}>"

async def embed_builder(**kwargs):
    return Embed(**kwargs)