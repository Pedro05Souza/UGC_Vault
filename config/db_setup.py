from tortoise import Tortoise, run_async
from dotenv import load_dotenv
import os

async def init():
    load_dotenv()
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    await Tortoise.init(
        db_url=f'postgres://{user}:{password}@localhost:5432/UgcBot',
        modules={'models': ['models.user', 'models.guild', 'models.codes', 'models.item']}
    )

    await Tortoise.generate_schemas()


async def get_tortoise_config() -> dict:
    config = {
        'connections': {
            'default': 'postgres://postgres:postgres@localhost:5432/UgcBot'
        },
        'apps': {
            'pnwapi': {
                'models': ['models.__init__'],
                'default_connection': 'default'
            }
        }

    }

run_async(init())