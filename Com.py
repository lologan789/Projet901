from threading import Thread, Semaphore
from pyeventbus3.pyeventbus3 import *
from time import sleep
from Message import *

class Com(Thread):
    def __init__(self, clock, process) -> None:
        Thread.__init__(self)

        PyBus.Instance().register(self, self)

        self.clock = clock
        self.process = process
        self.clock_lock = Semaphore(1)
        self.mailbox = []
        self.start()
    
    def __inc_clock(self):
        self.clock += 1
        