from .cm import ConnectManager
from .msg import Message
import threading
from .utils import get_logger
from .config import LOG_DIR


logger = get_logger(__name__, '{}/{}.log'.format(LOG_DIR, __name__))


class Agent:
    def __init__(self):
        self.msg = Message()
        self.cm = ConnectManager(self.msg)
        self.event = threading.Event()

    def start(self):
        while not self.event.is_set():  # 实现agent重连机制
            try:
                logger.info("Reading start agent.")
                self.cm.start()  # start方法里是一个死循环，只有当有异常时在这里捕获，执行关闭操作，3秒后尝试再次start()
            except Exception as e:
                logger.error('Agent connect master failed. Error: {}'.format(e))
            self.event.wait(3)

    def shutdown(self):
        self.event.set()
        self.cm.shutdown()






