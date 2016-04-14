
from time import sleep
from powertimer import *
from threading import Thread

def finish():
    print "done!"

my_timer = PWTimer(10, finish)
my_timer.start()
sleep(3)
my_timer.restart()
sleep(12)
my_timer.restart(2)