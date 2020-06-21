import zerorpc
import threading
from .config import HEARTBEAT_INTERVAL, MASTER_URL, LOG_DIR
from .msg import Message
from .utils import get_logger
from .state import *
from .executor import Executor


logger = get_logger(__name__, '{}/{}.log'.format(LOG_DIR, __name__))


class ConnectManager:
    def __init__(self, message: Message):
        self.client = zerorpc.Client()
        self.event = threading.Event()
        self.message = message  # 实例对象
        self.state = WAITING  # 任务完成状态
        self.executor = Executor()

    def start(self):
        # 启动时，先注册，后循环发送发心跳
        self.client.connect(MASTER_URL)
        result = self.client.reg(self.message.reg())  # 注册信息，master提供reg接口
        logger.info('Agent registration successful.')

        # 循环发送心跳信息
        while not self.event.wait(HEARTBEAT_INTERVAL):
            msg = self.message.heartbeat()
            result = self.client.heartbeat(msg)  # 心跳信息，master端提供heartbeat接口
            logger.info("Send heartbeat successful. msg: {}".format(msg))

            # 领任务, 执行任务，返回结果
            if self.state == WAITING:
                self._get_task_and_execute(self.message.id)

    def _get_task_and_execute(self, agent_id):
        task = self.client.get_task(agent_id)
        if task:
            # {
            #     'task_id': task.id,
            #     'script': task.script,
            #     'timeout': task.timeout
            # }
            # 执行任务
            self.state = RUNNING
            script = task['script']  # 需要作base64编码，解码
            timeout = task['timeout']
            code, txt = self.executor.run(script, timeout)
            msg = self.message.result(task['task_id'], code, txt)
            self._send(msg)

    def _send(self, msg: dict):
        try:
            ack = self.client.result(msg)
            logger.info(ack)
        except Exception as e:
            self.event.set()
            logger.error('Failed to connect to master. Error: {}'.format(e))

    def shutdown(self):
        self.event.set()
        self.client.close()
