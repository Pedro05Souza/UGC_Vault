"""
This module contains the developer commands for the bot.
"""
from discord.ext.commands import Cog, Context, command
from discord import Member
from core.tools import admin_only, send_bot_embed, economy_handler, retrieve_application_emoji
from core.routes import get_item_by_id, get_item_image_by_id
from controllers import get_user, create_user, update_user, execute_transactions, create_guild, get_guild, update_guild
from typing import Optional
from discord import Member

__all__ = (
    'DeveloperCommands',
)

class DeveloperCommands(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="givepoints", aliases=["gp"], description="Give points to a user.")
    @admin_only()
    async def give_points(self, ctx: Context, amount: int, user: Optional[Member] = None) -> None:
        """
        Gives points to a user.

        Args:
            amount (int): The amount of points to give.
            user (Optional[Member]): The user to give the points to. Defaults to the author.

        Returns:
            None
        """
        if not user:
            user = ctx.author

        if amount < 0:
            return await ctx.send("You can't give negative points.")

        user_data = await get_user(user.id)

        if not user_data:
            await create_user(user.id)
            user_data = await get_user(user.id)

        await update_user(user.id, balance=user_data.balance + amount)
        await send_bot_embed(ctx, title="Success", description=f":white_check_mark: You have given **{amount}** points to **{user.display_name}**.")

    @command(name="donate", aliases=["give"], description="Donate money to another user.")
    @economy_handler(user_data=True)
    @admin_only()
    async def donate(self, ctx: Context, user: Member, amount: int):
        author_data = ctx.user_data
        user_data = await get_user(user.id)
        paw_emoji = await retrieve_application_emoji("paw", 1295095109645373474)

        if author_data.balance < amount and amount > 0:
            return await send_bot_embed(ctx, description=f"{paw_emoji} You don't have enough money to donate.")
        
        if not user_data:
            return await send_bot_embed(ctx, description=f"{paw_emoji} **{user.display_name}** is not registered.")
        
        user_callback = lambda: update_user(user.id, balance=user_data.balance + amount)
        author_callback = lambda: update_user(ctx.author.id, balance=author_data.balance - amount)

        has_donated = await execute_transactions(user_callback, author_callback)

        if has_donated:
            candy_emoji = await retrieve_application_emoji("candy", 1295095109645373474, is_animated=True)
            await send_bot_embed(ctx, description=f"{candy_emoji} {ctx.author.display_name} has sucessfully donated **{amount}** candies to **{user.display_name}**.")
        else:
            await send_bot_embed(ctx, title="Error", description="An error occurred while donating.")

    @command(name="sync", description="Sync the bot's hybrid commands.")
    @admin_only()
    async def sync(self, ctx: Context) -> None:
        """
        Syncs the bot's hybrid commands.

        Args:
            None

        Returns:
            None
        """
        await self.bot.tree.sync()
        await ctx.send("Hybrid commands have been synced.")

    @command(name="registerchannel", aliases=["rc"], description="Register a channel for the bot to listen to.")
    @admin_only()
    async def register_channel(self, ctx: Context) -> None:
        """
        Registers a channel for the bot to listen to.

        Args:
            None

        Returns:
            None
        """
        guild_config = await get_guild(ctx.guild.id)

        if not guild_config:
            guild_config = await create_guild(ctx.guild.id)
            return await send_bot_embed(ctx, description=":no_entry_sign: This guild is not registered. Try again.")
        
        if guild_config.allowed_channels is None:
            await update_guild(ctx.guild.id, allowed_channels=[ctx.channel.id])
            return await send_bot_embed(ctx, description=":white_check_mark: This channel has been registered.")

        if ctx.channel.id in guild_config.allowed_channels:
            return await send_bot_embed(ctx, description=":no_entry_sign: This channel is already registered.")
        
        await update_guild(ctx.guild.id, allowed_channels=guild_config.allowed_channels + [ctx.channel.id])
        await send_bot_embed(ctx, description=":white_check_mark: This channel has been registered.", footer_text="This channel is now wishlisted for the bot to use.")

    @command(name="unregisterchannel", aliases=["urc"], description="Unregister a channel for the bot to listen to.")
    @admin_only()
    async def unregister_channel(self, ctx: Context) -> None:
        """
        Unregisters a channel for the bot to listen to.

        Args:
            None

        Returns:
            None
        """
        guild_config = await get_guild(ctx.guild.id)

        if not guild_config:
            return await send_bot_embed(ctx, description=":no_entry_sign: This guild is not registered. Try again.")
        
        if guild_config.allowed_channels is None:
            return await send_bot_embed(ctx, description=":no_entry_sign: This channel is not registered.")
        
        if ctx.channel.id not in guild_config.allowed_channels:
            return await send_bot_embed(ctx, description=":no_entry_sign: This channel is not registered.")
        
        guild_config.allowed_channels.remove(ctx.channel.id)
        
        await update_guild(ctx.guild.id, allowed_channels=guild_config.allowed_channels)
        await send_bot_embed(ctx, description=":white_check_mark: This channel has been unregistered.", footer_text="This channel is no longer wishlisted for the bot to use.")

    @command(name="registeritem", aliases=["ri"], description="Register an item in the bot's database.")
    async def register_item(self, ctx: Context, item_id: int):
        item_info = await get_item_by_id(item_id)

        if 'errors' in item_info:
            await self.parse_error_message(ctx, item_info)
            return
        
        item_image = await get_item_image_by_id(item_id)

        item_image = item_image['data'][0]
        item_image = item_image['imageUrl']
        item_name = item_info['Name']
        item_description = item_info['Description']
        item_price = item_info['PriceInRobux']

        
        description = (
            f"🏷️ **Item name** {item_name}\n"
            f"📜 **Item description** {item_description}\n"
            f"💰 **Price** {item_price} robux"
        )

        await send_bot_embed(ctx, title="💻 Item Information", description=description, thumbnail=item_image)

    async def parse_error_message(self, ctx: Context, item_info: dict):
        code = item_info['errors'][0]
        code = code['code']

        if code == 0:
            return await send_bot_embed(ctx, description=":no_entry_sign: Slow down!")
        elif code == 20:
            return await send_bot_embed(ctx, description=":no_entry_sign: The item ID you provided is invalid.")
        else:
            return await send_bot_embed(ctx, description=":no_entry_sign: An unknown error occurred while registering the item.")

async def setup(bot):
    await bot.add_cog(DeveloperCommands(bot))