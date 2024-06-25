class FakeGPIO:
    BCM = 'BCM'
    BOARD = 'BOARD'
    OUT = 'OUT'
    IN = 'IN'
    HIGH = True
    LOW = False

    def setwarnings(self, flag):
        pass

    def setmode(self, mode):
        pass

    def setup(self, channel, mode, initial=LOW):
        pass

    def output(self, channel, state):
        pass

    def input(self, channel):
        return self.LOW

    def cleanup(self):
        pass

    def __getattr__(self, name):
        def no_op(*args, **kwargs):
            pass
        return no_op
