
from threading import _Timer, Event

class PWTimer(_Timer):      # PowerTimer class
    """
    Creates a PWTimer object.
    PWTimer are improved Timer objects that are able to call a function after certaint conditions are accomplished.
    The class can "time" in an endless loop or a defined ammount of times. It can also be restarted and used again with
    new values if wanted.
    """
    def __init__(self, interval, function, loop=1, time_unit='seconds'):
        """

        :param interval: Time the timer has to "time" before executing the selected function.
        :param function: The function that is going to be triggered after the timeout happens.
        :param loop: The number of intervals the timer is going to be executed.
                     loop = 1 (default): The timer will count only one loop and execute the function after the
                     timeout happens.
                     loop = 0: The timer will run forever and execute the function after the timeout  is reached
                     (it means the self.stop() method will never be called and the user has to take care of that).
        :param time_unit: The unit of time (secods, minutes) the interal is applied. By defaut 'seconds'.
        """
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
        self.loop_counter = self.loop
        self.loopEvent = Event()
        self.__set_loop_behavior(self.loop)
        self.__actual_count = 0
        self.remaining_interval = self.__interval - self.__actual_count
        super(PWTimer, self).__init__(self.__interval, self.function, args=[], kwargs={})

    def run(self):
        """
        This is run() method called when the timer is initialized with the start(). It overwrites the original run()
        from the parent class _Timer.
        :return: nothing
        """
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

    def stop(self):
        """
        Sets the finished event to True. It has the same functionality like the cancel() method but it sounds more
        natural to me to call a stop() method rather than the cancel(). Anyway, the cancel is not overwriten so it can
        be used also.
        :return: nothing
        """
        self.finished.set()

    def pause(self):
        """
        Set the paused event to True. After the event is set the "while" loop in the run() method will be triggered and
        the timer will wait until it's released.
        :return: nothing
        """
        self.paused.set()

    def resume(self):
        """
        Set the paused event to False.
        :return: nothing
        """
        self.paused.clear()

    def __update_loop(self):
        """
        Private method to update the loop counters and set the loopEvent() if necesary.
        :return: nothing
        """
        if not self.__loopAlways:
            if self.loop_counter > 0:
                self.loop_counter -= 1
                self.__reset_counters()
                self.finished.clear()
                self.paused.clear()
            elif self.loop_counter == 0:
                self.loopEvent.set()

        elif self.__loopAlways:
            self.__reset_counters()
            self.finished.clear()
            self.paused.clear()

    def __reset_counters(self): #TODO: Find a proper name for the function, something like reset_interval_counters or so
        """
        Private method to reset the interval counters to its initial state.
        :return: nothing
        """
        self.__actual_count = 0
        self.remaining_interval = self.__interval - self.__actual_count

    def __set_loop_behavior(self, loop_value):
        if loop_value == 0:
            self.__loopAlways = True
        elif loop_value > 0:
            self.__loopAlways = False

    def restart(self, interval=None, loop=None):
        """
        Method to restart the timer when is already finished or at runtime. It can restart the timer with its old values
        or apply new ones when they are given.
        :param interval: The new interval value for the timer. If not given will restart with the old value
        :param loop: The new loop value for the timer. If not given will restart the timer with the old value
        :return: nothing
        """
        if interval is not None:
            self.__interval = self.__multiplier * interval

        if loop is not None:
            self.loop = loop
            self.__set_loop_behavior(self.loop)
            self.__update_loop()

        self.loop_counter = self.loop - 1

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

def dummy():
    print "sacabo"

from time import sleep

my_timer = PWTimer(5, dummy, loop=6)
my_timer.start()
sleep(6)
my_timer.restart(loop=1)