from tortoise.models import Model
from tortoise import fields

__all__ = ['Item']

class Item(Model):
    id = fields.BigIntField(pk=True)
    serial_number = fields.CharField(max_length=255, null=True)
