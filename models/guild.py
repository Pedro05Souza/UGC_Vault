from tortoise.models import Model
from tortoise import fields

__all__ = ['Guilds']

class Guilds(Model):
    id = fields.IntField(primary_key=True)
    allowed_channels = fields.JSONField()

    def __str__(self):
        return f'guild_id: {self.id}, allowed_channels: {self.allowed_channels}'