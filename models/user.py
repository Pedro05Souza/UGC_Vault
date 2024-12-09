from tortoise.models import Model
from tortoise import fields

__all__ = ["User"]


class User(Model):
    id = fields.BigIntField(primary_key=True)
    balance = fields.IntField(default=0)

    def __str__(self):
        return f"user_id: {self.id}, balance: {self.balance}"
