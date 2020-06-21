from .store import Store
from .utils import get_logger
from .config import LOG_DIR
from .state import *
import uuid


logger = get_logger(__name__, '{}/{}.log'.format(LOG_DIR, __name__))


class ConnectManager:
    def __init__(self):
        self.store = Store()

    @staticmethod
    def reg(msg):
        # 注册接口，接收到注册信息如何处理数据？心跳信息中有注册的信息，在心跳信息中存入agent相关信息
        logger.info('{} {} registration success'.format(msg['payload']['id'], msg['payload']['hostname']))
        return 'ack {}'.format(msg)

    def heartbeat(self, msg: dict):
        # 心跳接口，接收到心跳信息如何处理？需要维护一个客户端的列表
        self.store.agent_handler(msg['payload'])
        return 'ack {}'.format(msg)

    def result(self, result: dict):
        """agent脚本执行结果接口"""
        # {
        #     "type": "result",
        #     "payload": {
        #         "task_id": task_id,
        #         "agent_id": self.id,
        #         "code": code,
        #         "output": output
        #     }
        # }
        payload = result['payload']
        task_id = payload['task_id']
        agent_id = payload['agent_id']
        code = payload['code']
        output = payload['output']
        state = SUCCEED if code == 0 else FAILED

        task = self.store.get_task_by_task_id(task_id)
        agent_info = task.targets[agent_id]
        agent_info['output'] = output
        agent_info['state'] = state
        return "ack result."

    def get_task(self, agent_id):
        # 前端增加任务后，开放获取任务接口。
        # 一个agent要获取自己的任务，需要把agent自己的id传递过来
        # 返回什么？ 1. 任务的id, 2.执行的脚本，3. 执行脚本的超时时间
        info = self.store.get_task_by_agent_id(agent_id)
        if info:
            task, target = info
            task.state = RUNNING  # 修改任务状态
            target['state'] = RUNNING  # 修改当前agent获取到任务后的状态
            return {
                'task_id': task.task_id,
                'script': task.script,
                'timeout': task.timeout
            }

    def get_agents(self):
        # 返回所有已注册的agent
        return self.store.get_agents()

    def add_task(self, task):
        task['task_id'] = uuid.uuid4().hex
        return self.store.add_task(task)




