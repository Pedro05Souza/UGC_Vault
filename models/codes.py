from tortoise.models import Model
from tortoise import fields

__all__ = ['Codes']

class Codes(Model):
    id = fields.IntField(primary_key=True)
    item = fields.ForeignKeyField('models.Item', related_name='codes')
    code = fields.CharField(max_length=255)