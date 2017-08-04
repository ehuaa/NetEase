# -*- coding: GBK -*-

import heapq
import time


class CallLater(object):
    """Calls a function at a later time.
	"""

    def __init__(self, seconds, target, *args, **kwargs):
        super(CallLater, self).__init__()

        self._delay = seconds
        self._target = target
        self._args = args
        self._kwargs = kwargs

        self.cancelled = False
        self.timeout = time.time() + self._delay

    def __le__(self, other):
        return self.timeout <= other.timeout

    def call(self):
        try:
            self._target(*self._args, **self._kwargs)
        except (KeyboardInterrupt, SystemExit):
            print "call error"
            pass
        return False

    def cancel(self):
        self.cancelled = True


class CallEvery(CallLater):
    """Calls a function every x seconds.
	"""

    def __init__(self, delay, func, *args, **kwargs):
        super(CallEvery, self).__init__(delay, func, *args, **kwargs)
        self.timeout = time.time()

    def call(self):
        try:
            self._target(*self._args, **self._kwargs)
        except (KeyboardInterrupt, SystemExit):
            print "call error"
            pass
        self.timeout = time.time() + self._delay
        return True


class TimerManager(object):
    def __init__(self):
        super(TimerManager, self).__init__()
        self.tasks = []
        self.cancelled_num = 0

    def add_timer(self, delay, func, *args, **kwargs):
        timer = CallLater(delay, func, *args, **kwargs)
        heapq.heappush(self.tasks, timer)

    def add_repeat_timer(self, delay, func, *args, **kwargs):
        timer = CallEvery(delay, func, *args, **kwargs)
        heapq.heappush(self.tasks, timer)

    def scheduler(self):
        now = time.time()
        while self.tasks and now >= self.tasks[0].timeout:
            call = heapq.heappop(self.tasks)
            if call.cancelled:
                self.cancelled_num -= 1
                continue
            repeated = call.call()
            if repeated:
                heapq.heappush(self.tasks, call)

    def cancel(self, timer):
        if timer not in self.tasks:
            return
        timer.cancel()
        self.cancelled_num += 1
        if float(self.cancelled_num) / len(self.tasks) > 0.25:
            self.remove_cancelled_tasks()

    def remove_cancelled_tasks(self):
        tmp_tasks = []
        for t in self.tasks:
            if not t.cancelled:
                tmp_tasks.append(t)

        self.tasks = tmp_tasks
        heapq.heapify(self.tasks)
        self.cancelled_num = 0
