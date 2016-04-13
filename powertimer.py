
from threading import _Timer, Event
from time import sleep

class PWTimer(_Timer):      # PowerTimer class
    def __init__(self, interval, function, time_unit='seconds'):
        self.time_unit = time_unit
        if self.time_unit == 'seconds':
            multiplier = 1
        elif self.time_unit == 'minutes':
            multiplier = 60
        elif self.time_unit == 'hours':
            multiplier = 3600
        elif self.time_unit == 'light_years':
            pass        # ok, you implement this one :P
        self.paused = Event()
        self.interval = multiplier * interval
        self.function = function
        self.remaining_interval = 0
        self._actual_count = 0
        super(PWTimer, self).__init__(self.interval, self.function, args=[], kwargs={})

    def run(self):          # overwrites the original run() from _Timer so PWTimer can return the current timer counter
        while not self.finished.is_set():
            while self.paused.is_set():
                pass        #TODO: more elegant way to wait when the timer is paused
            self.finished.wait(1)
            self._actual_count += 1
            self.remaining_interval = self.interval - self._actual_count
            if self.interval - self._actual_count == 0:
                self.function(*self.args, **self.kwargs)
                self.finished.set()

    def stop(self):         # does the same as cancel() in the _Timer class but the name is more natural
        self.finished.set()

    def pause(self):        # pauses the timer so you can resume it later
        self.paused.set()

    def resume(self):       # resumes a paused timer
        self.paused.clear()

    def restart(self):      # restarts the timer at "runtime" or when is already finished
        pass                # TODO: Los 'Threads' solo se pueden iniciar una vez... a ver como te lo montas XD



class PWCounter(object):    # PowerCounter class
    pass

