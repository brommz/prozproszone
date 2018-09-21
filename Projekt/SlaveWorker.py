import zmq
import time
from Worker import Worker

class SlaveWorker(Worker):
    def __init__(self):
        Worker.__init__(self)

    def init(self, workerNumber):
        self.workerNumber = workerNumber

        self.context = zmq.Context()

        # zdefiniowanie gniazda PULL do odbierania wynikow
        self.pull = self.context.socket(zmq.PULL)
        self.pull.connect("ipc:///tmp/push")#tcp://localhost:5556

        # zdefiniowanie gniazda SUB do odbierania info zeby zakonczyc dzialanie
        self.killer = self.context.socket(zmq.SUB)
        self.killer.connect("ipc:///tmp/killer")
        self.killer.setsockopt(zmq.SUBSCRIBE, "")#tcp://localhost:5557

        # zdefiniowanie gniazda PUSH do przesylania wynikow
        self.worker_result = self.context.socket(zmq.PUSH)
        self.worker_result.connect("ipc:///tmp/worker_result") #tcp://localhost:5558

        # poller pozwala nasluchiwac na roznych gniazdkach w tym samym watku
        self.poller = zmq.Poller()
        self.poller.register(self.pull, zmq.POLLIN)
        self.poller.register(self.killer, zmq.POLLIN)

    def run(self):
        while True:
            socks = dict(self.poller.poll())

            if self.pull in socks and socks[self.pull] == zmq.POLLIN:
                part1, part2 = self.pull.recv_pyobj()
                time.sleep(1)
                self.worker_result.send_pyobj(self.merge(part1, part2, self.workerNumber))

            if self.killer in socks and socks[self.killer] == zmq.POLLIN:
                print "MASTER SENT KILL"
                self.init(self.workerNumber) #reinicjalizacja gniazdek
