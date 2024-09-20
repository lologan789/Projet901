from threading import Thread, Semaphore
from pyeventbus3.pyeventbus3 import *
from time import sleep
from Message import *
from State import State

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
        self.cptSync = 0
        self.messageReceived = False
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
                PyBus.Instance().post(BroadcastMessage(src=self.get_name(), payload=payload, stamp=self.clock))

    
    def sendTo(self, payload, dest: str):
        self.__inc_clock()
        PyBus.Instance().post(DestinatedMessage(src=self.get_name(), payload=payload, dest=dest, stamp=self.clock))

    @subscribe(threadMode=Mode.PARALLEL, onEvent=DestinatedMessage)
    def onReceive(self, event: DestinatedMessage):
        if event.dest == self.getName():
            self.clock = max(self.clock, event.stamp) + 1
            self.mailbox.append(event)
            print(f"Message reçu par {self.get_name()} : {event.payload}")

    def requestSC(self):
        self.process.state = State.REQUEST
        while self.process.state != State.SC:
            sleep(1)

    def releaseSC(self):
        self.process.state = State.RELEASE

    def synchronize(self):
        Pybus.Instance().post(Synchronization(src=self.get_name(), stamp=self.clock))
        while self.cptSync > 0:
            sleep(1)
        self.cptSync = len(self.owner.annuaire)

    def broadcastSync(self, _from: int, payload: object = None):
        if self.owner.numero == _from:
            if payload is not None:
                self.__inc_clock()
                PyBus.Instance().post(BroadcastMessageSync(src=_from, payload=payload, stamp=self.clock))
            print('broadcastSync')
            self.synchronize()
        else:
            while not self.messageReceived:
                sleep(1)
            self.messageReceived = False

    

    

        