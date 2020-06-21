from subprocess import Popen, PIPE


class Executor:
    """
    脚本执行类
    """
    @staticmethod
    def run(self, script, timeout):
        p = Popen(script, stdout=PIPE, shell=True)
        p.wait(timeout)
        text = p.stdout.read()
        return p.returncode, text

