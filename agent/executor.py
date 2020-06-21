from subprocess import Popen, PIPE
from .utils import get_logger
from .config import LOG_DIR

logger = get_logger(__name__, '{}/{}.log'.format(LOG_DIR, __name__))


class Executor:
    """
    脚本执行类
    """
    def run(self, script, timeout):
        print(script, timeout)
        p = Popen(script, stdout=PIPE, shell=True)
        p.wait(timeout)
        text = p.stdout.read()
        code = p.returncode
        logger.info("Script execution completed. code:{} txt:{}".format(code, text))
        return code, text

