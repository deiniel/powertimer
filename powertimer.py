
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
    def __init__(self, interval, function, loop=1, time_unit='seconds'):
        self.__time_unit = time_unit
        if self.__time_unit == 'seconds':
            self.__multiplier = 1
        elif self.__time_unit == 'minutes':
            self.__multiplier = 60
        elif self.__time_unit == 'hours':
            self.__multiplier = 3600
        elif self.__time_unit == 'light_years':
            pass        # ok, you implement this one :P
        self.paused = Event()
        self.__interval = self.__multiplier * interval
        self.function = function
        self.loop = loop
        self.loopEvent = Event()
        if self.loop == 0:
            self.__loopAlways = True
        elif self.loop > 0:
            self.__loopAlways = False
        self.__actual_count = 0
        self.remaining_interval = self.__interval - self.__actual_count
        super(PWTimer, self).__init__(self.__interval, self.function, args=[], kwargs={})

    def run(self):          # overwrites the original run() from _Timer so PWTimer can return the current timer counter
        while not self.loopEvent.is_set():
            self.__update_loop()
            while not self.finished.is_set():
                while self.paused.is_set():
                    pass        #TODO: more elegant way to wait when the timer is paused
                print self.remaining_interval
                self.__actual_count += 1
                self.finished.wait(1)
                self.remaining_interval = self.__interval - self.__actual_count
                if self.__interval - self.__actual_count == 0:
                    self.finished.set()
                    self.function(*self.args, **self.kwargs)

    def stop(self):         # does the same as cancel() in the _Timer class but the name is more natural
        self.finished.set()

    def pause(self):        # pauses the timer so you can resume it later
        self.paused.set()

    def resume(self):       # resumes a paused timer
        self.paused.clear()

    def __update_loop(self):
        if not self.__loopAlways:
            if self.loop > 0:
                self.loop -= 1
                self.__reset_counters()
                self.finished.clear()
                self.paused.clear()
            elif self.loop == 0:
                self.loopEvent.set()
        elif self.__loopAlways:
            self.__reset_counters()
            self.finished.clear()
            self.paused.clear()

    def __reset_counters(self):
        self.__actual_count = 0
        self.remaining_interval = self.__interval - self.__actual_count


    def restart(self, new_interval_value=None, new_loop_value=None):      # restarts the timer at "runtime" or when is already finished
        if new_interval_value is not None:
            self.__interval = self.__multiplier * new_interval_value

        if new_loop_value is not None:
            self.loop = new_loop_value
            self.__update_loop()

        if self.remaining_interval > 0:
            self.paused.set()
            self.__reset_counters()
            self.paused.clear()

        elif self.remaining_interval == 0:
            self.__reset_counters()
            self.finished.clear()
            self.paused.clear()
            super(PWTimer, self).__init__(self.__interval, self.function, args=[], kwargs={})
            self.start()


class PWCounter(object):    # PowerCounter class
    pass
