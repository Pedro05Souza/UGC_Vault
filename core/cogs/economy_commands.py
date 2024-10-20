"""
This module contains the economy commands for the bot.
"""
from math import ceil
from discord.ext.commands import Cog, Context, hybrid_command
from core.tools import send_bot_embed, economy_handler
from controllers import get_command_timestamp, create_command_timestamp, update_command_timestamp, update_user
from random import randint
from datetime import datetime, timezone

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
            thumbnail=ctx.author.display_avatar, title=f"{ctx.author.display_name}'s balance", 
            description=f"💼 Wallet: **{User.balance}**"
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
        initial_range = 500
        final_range = 5000

        User = ctx.user_data
        member = ctx.author
        
        timestamp = await get_command_timestamp(member.id, "booster")

        if not timestamp:
            await create_command_timestamp(member.id, "booster")
            timestamp = await get_command_timestamp(member.id, "booster")

        time_difference = (datetime.now(timezone.utc) - timestamp).seconds
        time_remaining = 1800 - time_difference

        if timestamp and time_remaining > 0:
            return await send_bot_embed(ctx, description=f":no_entry_sign: You have already claimed your daily booster reward, please wait **{ceil((time_remaining) / 60)}** minutes.")
                
        points_rewarded = randint(initial_range, final_range)
        await update_user(member.id, balance=User.balance + points_rewarded)
        await update_command_timestamp(member.id, "booster")
        await send_bot_embed(ctx, description=f"💰 You have claimed your daily booster reward of **{points_rewarded}**.")

                    
async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))