from tortoise.models import Model
from tortoise import fields

__all__ = ['Item']

class Item(Model):
    id = fields.UUIDField(primary_key=True)
    name = fields.CharField(max_length=255)
    image = fields.CharField(max_length=255)