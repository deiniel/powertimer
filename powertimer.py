
from threading import _Timer, Event

class PWTimer(_Timer):      # PowerTimer class
    """
    Creates a PWTimer object.
    PWTimer are improved Timer objects that are able to call a function after certaint conditions are accomplished.

    interval: time the timer has to "time" before executing the selected function
    function: the function that is going to be triggered after the timeout happeds
    loop: the number of intervals the timer is going to be executed
        loop = 1 (default): the timer will count only one loop and execute the function after the timeout happens
        loop = 0: the timer will run forever and execute the function after the timeout is reached (it means the
        self.stop() method will never be called and the user has to take care of that)
    time_unit: the unit of time (secods, minutes) the interal is applied. By defaut 'seconds'
    """
    def __init__(self, interval, function, loop = 1, time_unit='seconds'):
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
        self.loop = loop
        self.loopEvent = Event()
        if self.loop == 0:
            self.loopAlways = True
        elif self.loop > 0:
            self.loopAlways = False
        self.__actual_count = 0
        self.remaining_interval = self.interval - self.__actual_count
        super(PWTimer, self).__init__(self.interval, self.function, args=[], kwargs={})

    def run(self):          # overwrites the original run() from _Timer so PWTimer can return the current timer counter
        while not self.loopEvent.is_set():
            while not self.finished.is_set():
                while self.paused.is_set():
                    pass        #TODO: more elegant way to wait when the timer is paused
                self.__actual_count += 1
                self.finished.wait(1)
                self.remaining_interval = self.interval - self.__actual_count
                if self.interval - self.__actual_count == 0:
                    self.finished.set()
                    self.function(*self.args, **self.kwargs)
            self.update_loop()

    def stop(self):         # does the same as cancel() in the _Timer class but the name is more natural
        self.finished.set()

    def pause(self):        # pauses the timer so you can resume it later
        self.paused.set()

    def resume(self):       # resumes a paused timer
        self.paused.clear()

    def update_loop(self):
        if not self.loopAlways:
            if self.loop > 0:
                self.loop -= 1
            elif self.loop == 0:
                self.loopEvent.set()

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
    pass

def dummy():
    print 'hola!'

my_timer = PWTimer(5, dummy, loop=0)
my_timer.start()