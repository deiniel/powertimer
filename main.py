
from time import sleep
from powertimer import *
from threading import Thread

def print_interval(pwtimer):
    pwtimer.start()
    while True:
        sleep(1)
        print pwtimer.remaining_interval

def finish():
    print "done!"

my_timer = PWTimer(10, finish)
th = Thread(target=print_interval, args=(my_timer, ))
th.start()
sleep(3)
my_timer.pause()
sleep(5)
my_timer.resume()
