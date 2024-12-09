"""
This module contains the tools that are used in the bot.
"""

from discord import Embed, File, Interaction, Member, ButtonStyle
from discord.ext.commands import Context
from discord.ui import Button, View

__all__ = (
    "send_bot_embed",
    "retrieve_application_emoji",
    "embed_builder",
    "button_builder",
    "view_button_builder",
    "confirmation_popup",
)

async def send_bot_embed(
    ctx: Context | Interaction,
    thumbnail: File = None,
    footer_text: str = "",
    color="FFC5D3",
    ephemeral=False,
    is_dm=False,
    dm_failure_error_message="❌ Something went wrong while sending the DM.",
    **kwargs,
) -> None:
    """
    Function that makes the application send an embed message.

    Args:
        ctx (Context): The context of the command.
        thumbnail (str): The URL of the thumbnail.
        footer_text (str): The text that will be displayed in the footer.
        color (str): The color of the embed.
        ephemeral (bool): Whether the message should be ephemeral or not.
        is_dm (bool): Whether the message should be sent to the user's DMs.
        dm_failure_error_message (str): The error message that will be displayed if the DM fails.
        **kwargs: The keyword arguments that will be passed to the embed builder.

    Returns:
        None
    """
    embed = await embed_builder(
        embed_color=color, footer_text=footer_text, thumbnail=thumbnail, **kwargs
    )
    if is_dm:
        return await send_user_dm(ctx, dm_failure_error_message, embed)
    
    if isinstance(ctx, Interaction):
        if not ctx.response.is_done():
            return await ctx.response.send_message(embed=embed, ephemeral=ephemeral)
        return await ctx.followup.send(embed=embed, ephemeral=ephemeral)
    return await ctx.send(embed=embed)


async def send_user_dm(ctx: Context | Interaction, dm_failure_error_message: str, embed: Embed) -> None:
    """
    Function that sends a DM to a user.

    Args:
        ctx (Context): The context of the command.
        **kwargs: The keyword arguments that will be passed to the embed builder.

    Returns:
        None
    """
    is_interaction = isinstance(ctx, Interaction)
    
    try:
        if is_interaction:
            return await ctx.user.send(embed=embed)
        
        return await ctx.author.send(embed=embed)
    except Exception as e:
        error_embed = await embed_builder(description=dm_failure_error_message)
        
        if is_interaction:
            await ctx.followup.send(embed=error_embed, ephemeral=True)
        else:
            await ctx.send(embed=error_embed)
        
        raise e # This is necessary due to the fact this function could be called in a database transaction context.
        
async def retrieve_application_emoji(
    emoji_name: str, emoji_id: int, is_animated=False
) -> str:
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


async def embed_builder(embed_color="FFC5D3", footer_text=None, thumbnail=None, **kwargs):
    """
    Function that builds an embed.

    Args:
        embed_color (str): The color of the embed.
        footer_text (str): The text that will be displayed in the footer.
        thumbnail (str): The URL of the thumbnail.
        **kwargs: The keyword arguments that will be passed to the embed builder.

    Returns:
        Embed: The embed.
    """
    embed = Embed(**kwargs)
    
    embed.color = int(embed_color, 16)
    
    if footer_text:
        embed.set_footer(text=footer_text)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    return embed


async def button_builder(**kwargs) -> Button:
    """
    Function that creates a button.

    Args:
        **kwargs: The keyword arguments that will be passed to the button builder.

    Returns:
        Button: The button.
    """
    return Button(**kwargs)


async def view_button_builder(*buttons) -> View:
    """
    Function that creates a view with buttons.

    Args:
        *buttons: The buttons that will be added to the view.

    Returns:
        View: The view.
    """
    view = View()
    for button in buttons:
        if not isinstance(button, Button):
            raise TypeError("All buttons must be of type Button.")
        view.add_item(button)
    return view


async def confirmation_popup(
    ctx: Context | Interaction, embed: Embed, ephemeral=False
) -> bool:
    """
    Function that creates a confirmation popup.
    
    Args:
        ctx (Context): The context of the command.
        embed (Embed): The embed that will be sent.
        ephemeral (bool): Whether the message should be ephemeral or not.
    """
    cancel_button = await button_builder(
        label="Cancel", style=ButtonStyle.red, custom_id="cancel"
    )
    confirm_button = await button_builder(
        label="Confirm", style=ButtonStyle.green, custom_id="confirm"
    )
    view = await view_button_builder(cancel_button, confirm_button)

    if isinstance(ctx, Interaction):
        if not ctx.response.is_done():
            await ctx.response.send_message(embed=embed, ephemeral=ephemeral)
        await ctx.followup.send(embed=embed, ephemeral=ephemeral, view=view)
    else:
        await ctx.send(embed=embed, view=view, ephemeral=ephemeral)

    client = ctx.client if isinstance(ctx, Interaction) else ctx.bot
    author = ctx.user if isinstance(ctx, Interaction) else ctx.author
    
    try:
        interaction = await client.wait_for(
            "interaction", check=lambda i: i.user.id == author.id, timeout=60
        )
        await interaction.response.defer()

        if interaction.data["custom_id"] == "confirm":
            return True
        return False
    except TimeoutError:
        return False
