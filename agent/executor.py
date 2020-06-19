from subprocess import Popen, PIPE


class Executor:
    """
    脚本执行类
    """
    def __init__(self, script):
        self.script = script

    def run(self):
        p = Popen(self.script, stdout=PIPE, shell=True)
        p.wait()
        text = p.stdout.read()
        return p.returncode, text

