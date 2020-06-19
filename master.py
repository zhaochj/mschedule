import zerorpc


class Master:

    def reg(self, msg):
        return 'ok {}'.format(msg)

    def heartbeat(self, msg):
        return 'heartbeat {}'.format(msg)


s = zerorpc.Server(Master())
s.bind("tcp://0.0.0.0:9000")
s.run()
