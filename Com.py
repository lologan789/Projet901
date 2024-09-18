from threading import Thread, Semaphore
from pyeventbus3.pyeventbus3 import *
from time import sleep
from Message import *

class Com(Thread):
    def __init__(self, clock, process) -> None:
        Thread.__init__(self)
        self.alive = True

        PyBus.Instance().register(self, self)

        self.clock = clock
        self.process = process
        self.clock_lock = Semaphore(1)
        self.mailbox = []
        self.start()

    def stop(self):
        self.alive = False
        self.join()
    
    def __inc_clock(self):
        self.clock_lock.acquire()
        try:
            self.clock += 1
        finally:
            self.clock_lock.release()

    def broadcast(self, message: BroadcastMessage):
        self.__inc_clock()
        for p in self.process.processes:
            if p != self.process:
                PyBus.Instance().post(MessageTo(p, message, self.clock))

    
    def sendTo(self, process, message: Message):
        self.__inc_clock()
        PyBus.Instance().post(MessageTo(process, message, self.clock))

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageTo)
    def onReceive(self, event: MessageTo):
        self.mailbox.append(event)
        print(f"Message reçu : {event.object} avec horloge {event.horloge}")

    

    

        