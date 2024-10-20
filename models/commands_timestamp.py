from tortoise.models import Model
from tortoise import fields

__all__ = ['CommandsTimestamp']

class CommandsTimestamp(Model):
    user_id = fields.ForeignKeyField('models.User', related_name='commands_timestamps')
    command_name = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField(auto_now=True)

    class Meta:
        unique_together = ('user_id', 'command_name')

    def __str__(self):
        return f'{self.command_name} - {self.timestamp}'