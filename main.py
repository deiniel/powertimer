
from time import sleep
from powertimer import *
from threading import Thread

def print_interval(pwtimer):
    while True:
        print pwtimer.remaining_interval
        sleep(0.5)

def finish():
    print "done!"

my_timer = PWTimer(10, finish)
th = Thread(target=print_interval, args=(my_timer, ))
th.start()
my_timer.start()
sleep(3)
my_timer.pause()
sleep(5)
my_timer.resume()
