from .store import Store
from .utils import get_logger
from .config import LOG_DIR


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



