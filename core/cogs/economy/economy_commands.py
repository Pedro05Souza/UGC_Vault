"""
This module contains the economy commands for the bot.
"""

from math import ceil
from discord.ext.commands import Cog, Context, hybrid_command
from discord import Interaction, app_commands, Member
from tortoise.transactions import in_transaction
from core.tools import (
    send_bot_embed,
    economy_handler,
    retrieve_application_emoji,
    ugc_item_auto_complete,
    confirmation_popup,
    embed_builder,
)
from models import User
from controllers import (
    get_command_timestamp,
    create_command_timestamp,
    update_command_timestamp,
    update_user,
    get_user,
    get_code_from_item,
    get_item_by_roblox_id,
)
from random import randint
from config import DEFAULT_CLAIM_COOLDOWN
from datetime import datetime, timezone

__all__ = ("EconomyCommands",)


class EconomyCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_command(name="balance", aliases=["bal"], description="Check your balance.")
    @economy_handler()
    async def balance(self, ctx: Context, user: Member = None) -> None:
        """
        Allows users to check their balance.

        Args:
            None

        Returns:
            None
        """
        discord_user = ctx.author if not user else user

        internal_user = ctx.user_data if not user else await get_user(user.id)

        if user and not internal_user:
            return await send_bot_embed(
                ctx,
                description="The user you are trying to check the balance for does not have an account yet.",
            )

        await send_bot_embed(
            ctx,
            thumbnail=discord_user.display_avatar,
            title=f"{discord_user.display_name}'s candies",
            description=f"{await retrieve_application_emoji('candy', 1295095109645373474, True)} Wallet: **{internal_user.balance}**",
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
            points_rewarded,
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
            points_rewarded,
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
            points_rewarded,
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
            points_rewarded,
        )

    async def generic_timestamp_function(
        self,
        user: User,
        ctx: Context,
        command_name: str,
        description: str,
        points_rewarded: int,
    ) -> None:
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
            return await send_bot_embed(
                ctx,
                description=f":no_entry_sign: You have already claimed this reward, please wait **{ceil((time_remaining) / 60)}** minutes.",
            )

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

    @app_commands.command(
        name="searchitem", description="Search for an item in the shop."
    )
    @app_commands.autocomplete(item=ugc_item_auto_complete)
    async def search_ugc_item(
        self,
        interaction: Interaction,
        item: str,
    ) -> None:
        """
        Allows users to search for items in the shop.

        Args:
            item_name (str): The name of the item.
            item_price (int): The price of the item.
            item_category (str): The category of the item.

        Returns:
            None
        """
        item_id = int(item)

        item = await get_item_by_roblox_id(item_id)

        if not item:
            return await send_bot_embed(
                interaction,
                description="❌ The item you are looking for does not exist.",
                ephemeral=True,
            )

        user = await get_user(interaction.user.id)

        if not user:
            return await send_bot_embed(
                interaction,
                description="❌ You do not have an account yet.",
                ephemeral=True,
            )

        confirmation_embed = await embed_builder(
            title=f"Are you sure you want to purchase the following item?",
            description=f"**{item['item_name']}**\n\n**Description:** {item['item_description']}\n\n**Price:** {item['item_price']} candies",
        )
        
        result = await confirmation_popup(interaction, confirmation_embed, is_dm=True)
        
        if not result:
            return
        
        await self.dispatch_item_codes(interaction, item, user)

    async def dispatch_item_codes(
        self, interaction: Interaction, chosen_item, user: User
    ) -> None:
        """
        Dispatch the item codes to the user who purchased the items

        Args:
            chosen_items (list): The items that the user has chosen to purchase
        """
        async with in_transaction():
            failure_error_message = "❌ Oops! Something went wrong and i couldn't send you the codes. Don't worry, your money has been refunded and you can buy the items again."
            await update_user(
                user.id, balance=user.balance - chosen_item["item_price"]
            )

            item_code = await get_code_from_item(chosen_item["item_id"])

            if not item_code:
                failure_error_message = "❌ Oops! Someone else bought the items before you did. Don't worry, your money has been refunded and you can buy the items again."

                return await send_bot_embed(
                    interaction,
                    description=failure_error_message,
                    ephemeral=True,
                )

            await send_bot_embed(
                interaction,
                title="✅ Purchase successful",
                description=f"You have successfully purchased the following item:\n\n"
                + f"**{chosen_item['item_name']}**\n\n**Description:** {chosen_item['item_description']}\n\n**Price:** {chosen_item['item_price']} candies\n\n**Code:** {item_code}",
                is_dm=True,
                dm_failure_error_message=failure_error_message,
            )

async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))
