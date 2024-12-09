from discord.ext.commands import Bot
from core.tools import log_info
from pathlib import Path
from discord import Intents
from config.db_setup import init
from tortoise import run_async
from config import BOT_PREFIX
from dotenv import load_dotenv
import os

__all__ = ["UgcBot"]


class UgcBot(Bot):

    def __init__(self):
        super().__init__(
            command_prefix=self.setup_prefix(), intents=self.setup_intents()
        )

    def setup_intents(self) -> Intents:
        """
        This function sets up the intents for the bot.

        Returns:
            Intents: The intents that the bot will use.
        """
        intents = Intents.default()
        intents.members = True
        intents.voice_states = True
        intents.messages = True
        intents.message_content = True
        intents.guilds = True
        return intents

    def setup_prefix(self) -> str:
        """
        This function sets up the prefix for the bot.

        Returns:
            str: The prefix that the bot will use
        """
        return BOT_PREFIX

    async def setup_hook(self) -> None:
        """
        Load the cogs when the bot is ready.
        """
        log_info(f"Logged in as {self.user.name} ({self.user.id})")
        await self.load_cogs(self)

    async def load_cogs(self, bot: Bot) -> None:
        """
        This function loads the cogs for the bot.

        Args:
            bot (Bot): The bot object.
        """
        cogs_dir = Path("./core/cogs")
        for filepath in cogs_dir.rglob("*.py"):

            if filepath.stem == "__init__":
                continue

            module_path = (
                filepath.relative_to(cogs_dir)
                .with_suffix("")
                .as_posix()
                .replace("/", ".")
            )
            await bot.load_extension(f"core.cogs.{module_path}")
            log_info(f"Loaded cog: {module_path}")

    def setup_token(self) -> str:
        """
        This function retrieves the bot token from the environment.

        Returns:
            str: The bot token.
        """
        load_dotenv()
        return os.getenv("DISCORD_TOKEN")

    def run(self) -> None:
        """
        This function runs the bot.
        """
        log_info("Bot is starting...")
        run_async(init())
        super().run(self.setup_token())
