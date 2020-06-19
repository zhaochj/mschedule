import zerorpc
import threading
from .config import HEARTBEAT_INTERVAL, MASTER_URL, LOG_DIR
from .msg import Message
from .utils import get_logger


logger = get_logger(__name__, '{}/{}.log'.format(LOG_DIR, __name__))


class ConnectManager:
    def __init__(self, message: Message):
        self.client = zerorpc.Client()
        self.event = threading.Event()
        self.message = message  # 实例对象

    def start(self):
        # 启动时，先注册，后循环发送发心跳
        self.client.connect(MASTER_URL)
        self.client.reg(self.message.reg())  # 注册信息，master提供reg接口
        logger.info('Agent registration successful.')

        # 循环发送心跳信息
        while not self.event.wait(HEARTBEAT_INTERVAL):
            self.client.heartbeat(self.message.heartbeat())  # 心跳信息，master端提供heartbeat接口
            logger.info("Send heartbeat successful.")

    def shutdown(self):
        self.event.set()
        self.client.close()
