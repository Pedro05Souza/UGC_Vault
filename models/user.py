from tortoise.models import Model
from tortoise import fields

__all__ = ['User']
class User(Model):
    id = fields.IntField(primary_key=True, default=0)
    balance = fields.IntField()

    def __str__(self):
        return f'user_id: {self.id}, balance: {self.balance}'
