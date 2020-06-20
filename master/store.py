
class Store:
    """
    存储客户端
    """
    def __init__(self):
        self.agents = {}

    def agent_handler(self, payload: dict):
        self.agents[payload['id']] = {
            'hostname': payload['hostname'],
            'ip': payload['ip'],
            'busy': payload['busy']  # agent目前是否繁忙
        }
        # print(1111, self.agents)





