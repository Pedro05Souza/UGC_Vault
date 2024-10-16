"""
This module contains the main entry point for the bot.
"""
from config import setup_bot, setup_token, load_cogs
from core.tools import log_info

bot = setup_bot()

@bot.event
async def on_ready():
    log_info(f"Logged in as {bot.user.name} ({bot.user.id})")
    await load_cogs(bot)

if __name__ == '__main__':
    bot.run(setup_token())