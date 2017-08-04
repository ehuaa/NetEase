import time

class StateSnapshot(object):
    def __init__(self, snapshotnum):
        super(StateSnapshot, self).__init__()
        self.snapshotnum = snapshotnum
        self.timestamp = time.time()