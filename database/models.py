from tortoise import fields
from tortoise.models import Model
import asyncio

class AutoSaveMixin:
    _save_task = None
    
    async def auto_save(self, delay=5):
        """Авто-сохранение с задержкой"""
        if self._save_task:
            self._save_task.cancel()
        
        async def delayed_save():
            await asyncio.sleep(delay)
            await self.save()
        
        self._save_task = asyncio.create_task(delayed_save())
    
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if hasattr(self, 'id') and self.id and name not in ['_save_task']:
            # Автоматически запускаем сохранение при изменении полей
            asyncio.create_task(self.auto_save())


class Zombis(Model):
    uuid=fields.UUIDField(primary_key=True)
    tasks: fields.ReverseRelation["Task"] 
    # tasks=fields.ReverseRelation('models.Task', related_name='zombie')

# class Task(Model):
#     zombie: fields.ForeignKeyField()
#     type_task=fields.CharField(max_length=128)
#     data=fields.CharField(max_length=255, null=True)

class Task(Model):
    id=fields.UUIDField(primary_key=True)
    zombie=fields.ForeignKeyField("models.Zombis", related_name="tasks")
    type_task=fields.CharField(max_length=128)
    data=fields.CharField(max_length=255, null=True)