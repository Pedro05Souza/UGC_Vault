"""
This module contains the economy commands for the bot.
"""
from discord.ext.commands import Cog, Context, hybrid_command, hybrid_group
from core.tools import send_bot_embed, economy_handler
from controllers import update_user
from config import MAX_SLOTS
from collections import Counter
from random import randint, choices
from typing import Union 
from models import User

class EconomyCommands(Cog):
    def __init__(self, bot):
        self.bot = bot

    @hybrid_command(name="balance", aliases=["bal"], description="Check your balance.")
    @economy_handler(user_data=True)
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
        
    @hybrid_group(fallback="bet")
    async def bet(self, ctx: Context) -> None:
        """
        Allows users to bet on the slot machine.

        Args:
            None

        Returns:
            None
        """
        pass
        
    @bet.command(name="slots", description="Bet on the slot machine.")
    @economy_handler(user_data=True)
    async def slots(self, ctx: Context, bet_amount) -> None:
        """
        Test command.

        Args:
            None

        Returns:
            None
        """
        User = ctx.user_data

        if not await self.bet_validator(ctx, User, bet_amount):
            return
        
        await self.slots_handler(ctx, User, bet_amount)
             
    @bet.command(name="jackpots", description="Check the jackpot values.")
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
        description += "\n".join([f"{emoji} = {value} 💸" for emoji, value in jackpots.items()])
        description += "``"
        footer_description = "All combinations that can be won in the slot machine, followed by how many times the bet amount you will win."
        await send_bot_embed(ctx, title=title, footer_text=footer_description, description=description)

    @bet.command(name="roulette", description="Bet on the roulette table.")
    @economy_handler(user_data=True)
    async def roulette(self, ctx: Context, bet_amount, color_picked: str) -> None:
        """
        Roulette command for the betting system.

        Args:
            None

        Returns:
            None
        """
        if not await self.bet_validator(ctx, ctx.user_data, bet_amount):
            return

        total_chances = 37
        bet_multiplier = 2
        random_value = randint(0, total_chances)
        red_color = total_chances - 1 // 2
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
        
    async def bet_validator(self, ctx: Context, User: User, bet_amount: Union[str, int]) -> bool:
        """
        Validates the bet amount. Reducing

        Args:
            bet_amount (Union[str, int]): The bet amount.

        Returns:
            bool: The validation status.
        """
        if bet_amount in ("all", "ALL"):
            bet_amount = User.balance
        else:
            bet_amount = int(bet_amount)

        if User.balance < bet_amount:
            await send_bot_embed(ctx, description="You do not have enough money to bet.")
            return False

        return True      

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
            jackpot = possible_jackpots[random_fruits[0]]
            User.balance += jackpot * bet_amount
            description += f"\n🎉 **{ctx.author.display_name}** hit the jackpot! They won **{jackpot * bet_amount}**."

        elif len(fruits_freq) == 2:
            fruit = fruits_freq.most_common(1)[0][0]
            fruit = fruit * 2
            jackpot = possible_jackpots[fruit]
            User.balance += jackpot * bet_amount
            description += f"\n💰 **{ctx.author.display_name}** has won **{jackpot * bet_amount}**."

        else:
            description += f"\n😢 **{ctx.author.display_name}** has lost **{bet_amount}**."

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
            "🍇🍇": 2,
            "🍋🍋": 1.75,
            "🍒🍒": 1.5,
            "🍊🍊": 1.5,
            "🍉🍉": 1.25,
        }
    
    async def get_fruits(self) -> list:
        """
        Returns the fruits for the casino.

        Args:
            None

        Returns:
            list: The fruits.
        """
        return [
            "🍇",
            "🍋",
            "🍒",
            "🍊",
            "🍉"
        ]
                    
async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))