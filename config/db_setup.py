from tortoise import Tortoise
from dotenv import load_dotenv
from core.tools import log_info
import os

__all__ = ['init']

async def init():

    config = await retrieve_tortoise_config()
    await Tortoise.init(config)
    await Tortoise.generate_schemas()
    log_info("Database connection established from Tortoise ORM")

async def retrieve_tortoise_config() -> dict:
    load_dotenv()
    credentials = await retrieve_credentials()
    user = credentials['user']
    password = credentials['password']

    config = {
        "connections": {
            "default": f"postgres://{user}:{password}@localhost:5432/UgcBot"
        },
        "apps": {
            "models": {
                "models": ["models.user", "models.guild", "models.codes", "models.item"],
                "default_connection": "default"
            }
        }
    }

    return config

async def retrieve_credentials() -> dict:
    load_dotenv()
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    return {
        "user": user,
        "password": password
    }