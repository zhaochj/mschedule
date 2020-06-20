import uuid
import socket
import ipaddress
import netifaces
from .config import UUID_FILE_PATH, LOG_DIR
import os
from .utils import get_logger


logger = get_logger(__name__, '{}/{}.log'.format(LOG_DIR, __name__))


class Message:
    def __init__(self):
        self.busy = False

        if os.path.exists(UUID_FILE_PATH):
            with open(UUID_FILE_PATH) as f:
                self.id = f.readline().strip()
        else:
            self.id = uuid.uuid4().hex
            with open(UUID_FILE_PATH, 'w') as f:
                f.write(self.id)

    @property
    def _get_ips(self):
        """获取本地接口的Ip地址"""
        ips = []
        interfaces = netifaces.interfaces()
        for interface in interfaces:
            interface_info = netifaces.ifaddresses(interface)
            if 2 in interface_info.keys():
                for ip_info in interface_info[2]:
                    ip = ip_info['addr']
                    ip = ipaddress.ip_address(ip)  # 验证地址
                    if ip.version != 4 or ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_reserved:
                        # 非ipv4地址，回环地址，169.254开头地址，多播地址，保留地址，全部跨过
                        continue
                    ips.append(str(ip))
        return ips

    def reg(self):
        """注册信息"""
        return {
            "type": "register",
            "payload": {
                "id": self.id,
                "hostname": socket.gethostname(),
                "ip": str(self._get_ips)
            }
        }

    def heartbeat(self):
        """心跳信息"""
        return {
            "type": "heartbeat",
            "payload": {
                "id": self.id,
                "hostname": socket.gethostname(),
                "ip": str(self._get_ips),
                "busy": self.busy
            }
        }
