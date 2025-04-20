from tortoise import fields
from tortoise.models import Model

class Todo(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    completed = fields.BooleanField(default=False)

    class Meta:
        table = "todos"
