from discord.ext.commands import Cog, Context, hybrid_command, hybrid_group
from discord import app_commands
from core.tools import (
    send_bot_embed,
    economy_handler,
    color_autocomplete,
    coinflip_autocomplete,
)
from models import User
from random import choices, randint
from controllers import update_user
from math import ceil
from collections import Counter
from typing import Union
from config import MAX_SLOTS, MAX_COINFLIP

__all__ = ("BetCommands",)


class BetCommands(Cog):

    def __init__(self, bot):
        self.bot = bot

    @hybrid_group(name="slots", description="Bet on the slot machine.")
    @economy_handler()
    async def slots(self, ctx: Context, bet_amount) -> None:
        """
        Test command.

        Args:
            None

        Returns:
            None
        """
        User = ctx.user_data

        bet_amount = await self.bet_validator(ctx, User, bet_amount)

        if bet_amount == -1:
            return

        await self.slots_handler(ctx, User, bet_amount)

    @hybrid_command(name="jackpots", description="Check the jackpot values.")
    async def jackpots(self, ctx: Context) -> None:
        """
        Allows users to check the jackpot values.

        Args:
            None

        Returns:
            None
        """
        jackpots = await self.get_jackpots()
        title = "🎰 Jackpots 🎰"
        description = "``"
        description += "\n".join(
            [f"{emoji} = {value} 💸" for emoji, value in jackpots.items()]
        )
        description += "``"
        footer_description = "All combinations that can be won in the slot machine, followed by how many times the bet amount you will win."
        await send_bot_embed(
            ctx, title=title, footer_text=footer_description, description=description
        )

    @hybrid_command(
        name="roulette", aliases=["rl"], description="Bet on a color in roulette."
    )
    @app_commands.autocomplete(color_picked=color_autocomplete)
    @economy_handler()
    async def roulette(self, ctx: Context, bet_amount, color_picked: str) -> None:
        """
        Roulette command for the betting system.

        Args:
            None

        Returns:
            None
        """
        bet_amount = await self.bet_validator(ctx, ctx.user_data, bet_amount)

        if bet_amount == -1:
            return

        total_chances = 37
        bet_multiplier = 2
        random_value = randint(0, total_chances)
        red_color = ceil((total_chances - 1) / 2)
        red_color = list(range(1, red_color))
        rng_color = None

        user = ctx.user_data

        if random_value == 0:
            rng_color = "Green"
            bet_multiplier = 14

        elif random_value in red_color:
            rng_color = "Red"

        else:
            rng_color = "Black"

        if color_picked.lower() == rng_color.lower():
            user.balance += bet_amount * bet_multiplier
            description = f"🎉 **{ctx.author.display_name}** has won **{bet_amount * bet_multiplier}**."
        else:
            user.balance -= bet_amount
            description = f"😢 **{ctx.author.display_name}** has lost **{bet_amount}** The color picked was **{rng_color}**"

        if await update_user(user.id, balance=user.balance):
            await send_bot_embed(ctx, description=description)

    @hybrid_command(
        name="coinflip", aliases=["cf"], description="Bet on a side in a coinflip."
    )
    @app_commands.autocomplete(side=coinflip_autocomplete)
    @economy_handler()
    async def coinflip(self, ctx: Context, bet_amount, side: str) -> None:
        """
        Coinflip command for the betting system.

        Args:
            bet_amount (int): The amount to bet.
            side (str): The side to bet on.
        """
        User = ctx.user_data
        bet_amount = await self.bet_validator(ctx, User, bet_amount)

        if bet_amount == -1:
            return

        if bet_amount > MAX_COINFLIP:
            return await send_bot_embed(
                ctx,
                description=f":no_entry_sign: The maximum bet amount is **{MAX_COINFLIP}**.",
            )

        coin_sides = ["heads", "tails"]
        rng_side = choices(coin_sides)[0]

        if side.lower() == rng_side:
            User.balance += bet_amount
            description = f"🎉 **{ctx.author.display_name}** has won **{bet_amount}**."
        else:
            User.balance -= bet_amount
            description = f"😢 **{ctx.author.display_name}** has lost **{bet_amount}**. The side was **{rng_side}**."

        await update_user(User.id, balance=User.balance)
        await send_bot_embed(ctx, description=description)

    async def bet_validator(
        self, ctx: Context, User: User, bet_amount: Union[str, int]
    ) -> int:
        """
        Validates the bet amount. Reducing

        Args:
            bet_amount (Union[str, int]): The bet amount.

        Returns:
            bool: The validation status.
        """
        if bet_amount.isdigit():
            bet_amount = int(bet_amount)

        elif bet_amount.lower() == "all":
            bet_amount = User.balance

        else:
            await send_bot_embed(ctx, description="Please enter a valid number.")
            return -1

        if bet_amount > User.balance or bet_amount < 0:
            await send_bot_embed(
                ctx, description="You do not have enough money to bet."
            )
            return -1

        return bet_amount

    async def slots_handler(self, ctx: Context, User, bet_amount) -> None:
        User.balance -= bet_amount
        fruits = await self.get_fruits()
        random_fruits = choices(fruits, k=MAX_SLOTS)

        title = "🎰 Slot Machine 🎰"
        row1 = "| {} | {} | {} |".format(*choices(fruits, k=3))
        row2 = "| {} | {} | {} | <".format(*random_fruits)
        row3 = "| {} | {} | {} |".format(*choices(fruits, k=3))
        description = "```\n{}\n{}\n{}\n```".format(row1, row2, row3)

        fruits_freq = Counter(random_fruits)
        possible_jackpots = await self.get_jackpots()

        if len(fruits_freq) == 1:
            fruit = fruits_freq.most_common(1)[0][0]
            fruit = fruit * 3
            jackpot = possible_jackpots[fruit]
            User.balance += jackpot * bet_amount
            description += f"\n🎉 **{ctx.author.display_name}** hit the jackpot! They won **{jackpot * bet_amount}**."

        elif len(fruits_freq) == 2:
            fruit = fruits_freq.most_common(1)[0][0]
            fruit = fruit * 2
            jackpot = possible_jackpots[fruit]
            User.balance += int(jackpot * bet_amount)
            description += f"\n💰 **{ctx.author.display_name}** has won **{int(jackpot * bet_amount)}**."

        else:
            description += (
                f"\n😢 **{ctx.author.display_name}** has lost **{bet_amount}**."
            )

        if await update_user(User.id, balance=User.balance):
            await send_bot_embed(ctx, title=title, description=description)

    async def get_jackpots(self) -> dict:
        """
        Returns the jackpot values for the casino.

        Args:
            None

        Returns:
            dict: The jackpot values.
        """
        return {
            "🍇🍇🍇": 12,
            "🍋🍋🍋": 9,
            "🍒🍒🍒": 7,
            "🍊🍊🍊": 5,
            "🍉🍉🍉": 3,
            "🍇🍇": 1.5,
            "🍋🍋": 1.4,
            "🍒🍒": 1.3,
            "🍊🍊": 1.2,
            "🍉🍉": 1.1,
        }

    async def get_fruits(self) -> list:
        """
        Returns the fruits for the casino.

        Args:
            None

        Returns:
            list: The fruits.
        """
        return ["🍇", "🍋", "🍒", "🍊", "🍉"]


async def setup(bot):
    await bot.add_cog(BetCommands(bot))
