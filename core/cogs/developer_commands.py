"""
This module contains the developer commands for the bot.
"""
from discord.ext.commands import Cog, Context, hybrid_command, command
from discord import Member
from core.tools import admin_only, send_bot_embed, economy_handler, retrieve_application_emoji
from controllers import get_user, create_user, update_user, execute_transactions
from typing import Optional
from discord import Member

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

async def setup(bot):
    await bot.add_cog(DeveloperCommands(bot))