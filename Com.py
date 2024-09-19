from threading import Thread, Semaphore
from pyeventbus3.pyeventbus3 import *
from time import sleep
from Message import *

class Com(Thread):
    def __init__(self, clock, process) -> None:
        Thread.__init__(self)
        self.alive = True
        self.setName(process.myId)
        PyBus.Instance().register(self, self)

        self.owner = process.myId
        self.clock = clock
        self.process = process
        self.clock_lock = Semaphore()
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

    def get_name(self):
        return self.process.name

    def broadcast(self, payload : object):
        self.__inc_clock()
        for p in self.process.processes:
            if p != self.process:
                PyBus.Instance().post(BroadcastMessage(obj=payload, from_process=self.get_name(), horloge=self.clock))

    
    def sendTo(self, payload, dest: str):
        self.__inc_clock()
        PyBus.Instance().post(MessageTo(obj=payload, from_process=self.get_name(), to_process=dest, horloge=self.clock))

    @subscribe(threadMode=Mode.PARALLEL, onEvent=MessageTo)
    def onReceive(self, event):
        if event.to_process == self.getName():
            self.clock = max(self.clock, event.horloge) + 1
            self.mailbox.append(event)
            print(f"Message reçu par {self.get_name()} : {event.getObject()}")

    def requestSC(self):
        self.process

    

    

        