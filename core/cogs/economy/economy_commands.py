"""
This module contains the economy commands for the bot.
"""
from math import ceil
from discord.ext.commands import Cog, Context, hybrid_command
from core.tools import send_bot_embed, economy_handler, retrieve_application_emoji
from models import User
from controllers import get_command_timestamp, create_command_timestamp, update_command_timestamp, update_user
from random import randint
from config import DEFAULT_CLAIM_COOLDOWN
from datetime import datetime, timezone

__all__ = (
    'EconomyCommands',
)

class EconomyCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_command(name="balance", aliases=["bal"], description="Check your balance.")
    @economy_handler()
    async def balance(self, ctx: Context) -> None:
        """
        Allows users to check their balance.

        Args:
            None

        Returns:
            None
        """
        User = ctx.user_data
        await send_bot_embed(
            ctx, 
            thumbnail=ctx.author.display_avatar, title=f"{ctx.author.display_name}'s candies", 
            description=f"{await retrieve_application_emoji('candy', 1295095109645373474, True)} Wallet: **{User.balance}**"
            )
        
    @hybrid_command(name="booster", description="Claim your daily booster reward.")
    @economy_handler(booster_command=True)
    async def booster(self, ctx: Context) -> None:
        """
        Allows users to claim their daily booster reward.

        Args:
            None

        Returns:
            None
        """
        points_rewarded = await self.get_points_rewarded(500, 5000)
        await self.generic_timestamp_function(
            User, 
            ctx, 
            "booster", 
            f"{await retrieve_application_emoji(emoji_name='booster', emoji_id=1297349785442979881)} You have claimed your daily booster reward", 
            points_rewarded
            )
        
    @hybrid_command(name="candydrop", description="Claim your daily candy drop.")
    @economy_handler(booster_command=True)
    async def candy_drop(self, ctx: Context) -> None:
        points_rewarded = await self.get_points_rewarded(500, 5000)
        await self.generic_timestamp_function(
            ctx.user_data,
            ctx, 
            "candydrop", 
            f"{await retrieve_application_emoji('booster', 1297349785442979881)}You have claimed your daily candy drop and found **{points_rewarded}** candies.",
            points_rewarded
            )
        
    @hybrid_command(name="candy", description="Claim your daily candy reward.")
    @economy_handler()
    async def candy(self, ctx: Context) -> None:
        points_rewarded = await self.get_points_rewarded(300, 3000)
        await self.generic_timestamp_function(
            ctx.user_data, 
            ctx, 
            "candy", 
            f"{await retrieve_application_emoji('candy', 1295095109645373474, True)} You check your pockets and find **{points_rewarded}** candies.",
            points_rewarded
            )
        
    @hybrid_command(name="candyhunt", description="Claim your daily candy hunt reward.")
    @economy_handler()
    async def candy_hunt(self, ctx: Context) -> None:
        points_rewarded = await self.get_points_rewarded(500, 5000)
        await self.generic_timestamp_function(
            ctx.user_data, 
            ctx, 
            "candyhunt", 
            f"{await retrieve_application_emoji('candy', 1295095109645373474, True)} You’re on a mission to gather some delicious candies! You stumble upon a hidden stash in the forest finding **{points_rewarded}** candies.",
            points_rewarded
            )

    async def generic_timestamp_function(
            self, 
            user: User, 
            ctx: Context,
            command_name: str, 
            description: str, 
            points_rewarded: int,
            ):
        """
        Generic timestamp function for the economy commands.

        Args:
            User (User): The user data.
            ctx (Context): The context.
            description (str): The description to send.
            command_name (str): The command name.
        """
        is_first_time_claiming = False
        member = ctx.author
        
        timestamp = await get_command_timestamp(member.id, command_name)

        if not timestamp:
            is_first_time_claiming = True
            await create_command_timestamp(member.id, command_name)
            timestamp = await get_command_timestamp(member.id, command_name)

        time_difference = (datetime.now(timezone.utc) - timestamp).seconds
        time_remaining = DEFAULT_CLAIM_COOLDOWN - time_difference

        if timestamp and time_remaining > 0 and not is_first_time_claiming:
            return await send_bot_embed(ctx, description=f":no_entry_sign: You have already claimed this reward, please wait **{ceil((time_remaining) / 60)}** minutes.")
            
        await update_user(member.id, balance=user.balance + points_rewarded)
        await update_command_timestamp(member.id, command_name)
        await send_bot_embed(ctx, description=description)

    async def get_points_rewarded(self, initial_range: int, final_range: int) -> int:
        """
        Get the points rewarded for the command.

        Args:
            initial_range (int): The initial range.
            final_range (int): The final range.

        Returns:
            int: The points rewarded.
        """
        return randint(initial_range, final_range)

async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))