from .task import Task
from .state import *


class Store:
    """
    存储客户端,任务
    """
    def __init__(self):
        self.agents = {}
        self.tasks = {}

    def agent_handler(self, payload: dict):
        self.agents[payload['id']] = {
            'hostname': payload['hostname'],
            'ip': payload['ip']
        }

    def add_task(self, task: dict):  # 从前端界面增加任务到相应的agent
        t = Task(**task)
        self.tasks[t.task_id] = t  # t是一个实例对象，使用实例属性存放任务
        return t.task_id  # 返回给前端任务的id

    def iter_tasks(self, states=None):
        if states is None:
            states = {WAITING, RUNNING}  # 获取任务，只有任务状态为WAITING和RUNNING才尝试去获取
        yield from (task for task in self.tasks.values() if task.state in states)

    def get_task_by_agent_id(self, agent_id):
        for task in self.iter_tasks():
            if agent_id in task.targets.keys():
                target = task.targets[agent_id]   # {agent_id: {'state': WAITING, 'output':' '}
                if target['state'] == WAITING:
                    return task, target

    def get_task_by_task_id(self, task_id):
        return self.tasks[task_id]

    def get_agents(self):
        # 返回agent列表
        return self.agents













