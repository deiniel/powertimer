
from threading import _Timer, Event

class PWTimer(_Timer):      # PowerTimer class
    def __init__(self, interval, function, time_unit='seconds'):
        self.time_unit = time_unit
        if self.time_unit == 'seconds':
            self.multiplier = 1
        elif self.time_unit == 'minutes':
            self.multiplier = 60
        elif self.time_unit == 'hours':
            self.multiplier = 3600
        elif self.time_unit == 'light_years':
            pass        # ok, you implement this one :P
        self.paused = Event()
        self.interval = self.multiplier * interval
        self.function = function
        self.__actual_count = 0
        self.remaining_interval = self.interval - self.__actual_count
        super(PWTimer, self).__init__(self.interval, self.function, args=[], kwargs={})

    def run(self):          # overwrites the original run() from _Timer so PWTimer can return the current timer counter
        while not self.finished.is_set():
            while self.paused.is_set():
                pass        #TODO: more elegant way to wait when the timer is paused
            self.__actual_count += 1
            self.finished.wait(1)
            self.remaining_interval = self.interval - self.__actual_count
            if self.interval - self.__actual_count == 0:
                self.finished.set()
                self.function(*self.args, **self.kwargs)

    def stop(self):         # does the same as cancel() in the _Timer class but the name is more natural
        self.finished.set()

    def pause(self):        # pauses the timer so you can resume it later
        self.paused.set()

    def resume(self):       # resumes a paused timer
        self.paused.clear()

    def restart(self, new_value=None):      # restarts the timer at "runtime" or when is already finished
        if new_value is not None:
            self.interval = self.multiplier * new_value

        if self.remaining_interval > 0:
            self.paused.set()
            self.__actual_count = 0
            self.remaining_interval = self.interval - self.__actual_count
            self.paused.clear()

        elif self.remaining_interval == 0:
            self.__actual_count = 0
            self.remaining_interval = self.interval - self.__actual_count
            self.finished.clear()
            self.paused.clear()
            super(PWTimer, self).__init__(self.interval, self.function, args=[], kwargs={})
            self.start()


class PWCounter(object):    # PowerCounter class
    def __init__(self, start_count, end_count, function, step=1):
        self.start_count = start_count
        self.end_count = end_count
        self.function = function
        self.finished = Event()
        if self.start_count <= self.end_count:
            self.step = -step
            self.remaining_counts = self.end_count - self.start_count
        elif self.start_count > self.end_count:
            self.step = step
            self.remaining_counts = self.start_count - self.end_count
        self.function_triggered = Event()

    def update(self):
        if not self.finished.is_set():
            self.remaining_counts += self.step
            if self.remaining_counts <= 0:
                self.finished.set()

        elif self.finished.is_set() and not self.function_triggered.is_set():
            self.function()
            self.function_triggered.set()

    def restart(self):
        self.function_triggered.clear()
        self.finished.clear()
        if self.start_count <= self.end_count:
            self.remaining_counts = self.end_count - self.start_count
        elif self.start_count > self.end_count:
            self.remaining_counts = self.start_count - self.end_count


def dummy():
    print "I am a dummy"

counter = PWCounter(0, 3, dummy)
for i in range(0, 5):
    i += 1
    counter.update()
print counter.remaining_counts
counter.update()
counter.restart()
print counter.remaining_counts