"""
This module contains the error handler for the bot.
"""
from discord.ext.commands import Cog, CommandError, CommandNotFound


class ErrorHandler(Cog):

    def __init__(self, bot):
        self.bot = bot


    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandError) and not isinstance(error, CommandNotFound):
            await ctx.send(f"An error occurred: {error}")
            raise error

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))