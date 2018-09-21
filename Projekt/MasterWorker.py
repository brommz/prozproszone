import zmq
import random
import sys
from Worker import Worker


class MasterWorker(Worker):
    def __init__(self):
        Worker.__init__(self)

    def init(self, workerNumber):
        self.workerNumber = workerNumber

        self.context = zmq.Context()

        # zdefiniowanie gniazda PUSH do wysylania
        self.push = self.context.socket(zmq.PUSH)
        self.push.bind("ipc:///tmp/push") #tcp://*:5556

        # zdefiniowanie gniazda PUB do broadcastowego wysykania
        self.killer = self.context.socket(zmq.PUB)
        self.killer.bind("ipc:///tmp/killer")#tcp://*:5557

        # zdefiniowanie gniazda PULL do odbierania wynikow
        self.worker_result = self.context.socket(zmq.PULL)
        self.worker_result.bind("ipc:///tmp/worker_result")#tcp://*:5558

    def run(self, arraySize, definedArray):
        if definedArray != None:
            array = definedArray
        else:
            array = [random.randint(0, arraySize) for _ in xrange(arraySize)]
        arrayIterator = array.__iter__()
        results = []

        # poller pozwala nasluchiwac na roznych gniazdkach w tym samym watku
        self.poller = zmq.Poller()
        self.poller.register(self.worker_result, zmq.POLLIN)
        self.poller.register(self.push, zmq.POLLOUT)

        print "Glowny ruszyl, tablica:", array
        while True:
            socks = dict(self.poller.poll())

            if self.worker_result in socks and socks[self.worker_result] == zmq.POLLIN:
                result = self.worker_result.recv_pyobj()
                if len(result) == arraySize:
                    self.killer.send_pyobj("KILL") # ktorys wezel zwrocil cala tablice czyli koniec wszystkim mozna rozeslac
                    assert result == sorted(result)
                    print "Wynik: ", result
                    sys.exit(0)
                    break
                else:
                    print "Otrzymano:", result
                    results.append(result)
                    if len(results) == 2:
                        print "\n", "Wysylam ", results, "\n"
                        self.push.send_pyobj(results)
                        results = []

            if self.push in socks and socks[self.push] == zmq.POLLOUT:
                try:
                    part1 = [arrayIterator.next()]
                    part2 = [arrayIterator.next()]
                    print "\n", "Wysylam", part1, "...", part2, "\n"
                    self.push.send_pyobj((part1, part2))
                except StopIteration:
                    print "Stop"
                    self.poller.unregister(self.push)
