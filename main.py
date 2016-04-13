
from powertimer import *

def dummy_trigger():
    print "Hi, I am a dummy"

my_timer = PWTimer(10, dummy_trigger)
my_timer.start()
