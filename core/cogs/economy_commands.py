from discord.ext.commands import Cog, Context, hybrid_command
from core.tools import send_bot_embed, economy_handler, retrieve_application_emoji
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
        
        User.balance -= bet_amount
        fruits = await self.get_fruits()
        random_fruits = random.choices(fruits, k=MAX_SLOTS)
        possible_jackpots = await self.get_jackpots()

        title = f"{random_fruits}"
        description = ""

        fruits_freq = Counter(random_fruits)

        if len(fruits_freq) == 1:
            jackpot = possible_jackpots[random_fruits[0]]
            User.balance += jackpot * bet_amount
            description = f"You won the jackpot {jackpot}x your bet amount."

        elif len(fruits_freq) == 2:
            fruit = fruits_freq.most_common(1)[0][0]
            fruit = fruit * 2
            jackpot = possible_jackpots[fruit]
            User.balance += jackpot * bet_amount
            description = f"You won {jackpot}x your bet amount."

        else:
            description = "You lost."

        await send_bot_embed(ctx, title=title, description=description)
             
    @hybrid_command(name="jackpots", aliases=["jp"], description="Check the jackpot values.")
    async def jackpots(self, ctx: Context) -> None:
        """
        Allows users to check the jackpot values.

        Args:
            None

        Returns:
            None
        """
        candy_emoji = await retrieve_application_emoji("candy", 1295095109645373474, is_animated=True)
        jackpots = await self.get_jackpots()
        jackpots_str = "\n".join([f"{key}: {value} {candy_emoji}" for key, value in jackpots.items()])
        await send_bot_embed(ctx, title="Jackpots:", description=jackpots_str)
        
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