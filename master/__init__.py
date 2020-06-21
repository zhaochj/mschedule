import zerorpc
from .config import SERVER_URL
from .cm import ConnectManager


class Master:
    def __init__(self):
        self.server = zerorpc.Server(ConnectManager())
        self.server.bind(SERVER_URL)

    def start(self):
        self.server.run()

    def stop(self):
        self.server.close()

