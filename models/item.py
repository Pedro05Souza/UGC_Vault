from tortoise.models import Model
from tortoise import fields

__all__ = ['Item']

class Item(Model):
    item_id = fields.BigIntField(pk=True)
    item_name = fields.CharField(max_length=255)
    item_description = fields.TextField()
    item_price = fields.IntField()
