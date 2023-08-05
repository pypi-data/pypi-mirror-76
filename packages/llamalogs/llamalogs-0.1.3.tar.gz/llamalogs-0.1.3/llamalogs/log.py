from llamalogs.helpers import ms_time

class Log:
    def __init__(self):
        self.sender = ''
        self.receiver = ''
        self.timestamp = ms_time()
        self.message = ''
        self.initialMessage = True
        self.account = ''
        self.graph = ''
        self.isError = False
        self.elapsed = 0