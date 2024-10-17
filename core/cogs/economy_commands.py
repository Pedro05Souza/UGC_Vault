"""
This module contains the economy commands for the bot.
"""
from discord.ext.commands import Cog, Context, hybrid_command
from core.tools import send_bot_embed, economy_handler
from controllers import update_user
from config import MAX_SLOTS
import random
from collections import Counter

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
        
    @hybrid_command(name="slot", aliases=["slots"], description="Slot machine.")
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

        if bet_amount in ("all", "ALL"):
            bet_amount = User.balance
        else:
            bet_amount = int(bet_amount)

        if User.balance < bet_amount:
            await send_bot_embed(ctx, description="You do not have enough money to bet.")
            return
        
        await self.slots_handler(ctx, User, bet_amount)
             
    @hybrid_command(name="jackpots", aliases=["jp"], description="Check the jackpot values.")
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

    async def slots_handler(self, ctx: Context, User, bet_amount) -> None:
        User.balance -= bet_amount
        fruits = await self.get_fruits()
        random_fruits = random.choices(fruits, k=MAX_SLOTS)

        title = "🎰 Slot Machine 🎰"
        row1 = "| {} | {} | {} |".format(*random.choices(fruits, k=3))
        row2 = "| {} | {} | {} | <".format(*random_fruits)
        row3 = "| {} | {} | {} |".format(*random.choices(fruits, k=3))
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