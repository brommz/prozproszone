import sys
import os
import random
import zmq
from MergeSortAlgorithm import MergeSortAlgorithm


class MergeSortDistributed:
    def __init__(self):
        self._mergeAlg = MergeSortAlgorithm()

    def merge(self, part1, part2, workerNumber):
        print("Worker ", workerNumber, ": ", part1, ", ", part2)
        return self._mergeAlg.merge(part1, part2)

    def spawn_worker(self, workerNumber):
        if os.fork() == 0:
            context = zmq.Context()

            pull = context.socket(zmq.PULL)
            pull.connect("ipc:///tmp/push")
            killer = context.socket(zmq.SUB)
            killer.connect("ipc:///tmp/killer")
            killer.setsockopt(zmq.SUBSCRIBE, "")
            worker_result = context.socket(zmq.PUSH)
            worker_result.connect("ipc:///tmp/worker_result")

            poller = zmq.Poller()
            poller.register(pull, zmq.POLLIN)
            poller.register(killer, zmq.POLLIN)
            while True:
                socks = dict(poller.poll())
                if pull in socks and socks[pull] == zmq.POLLIN:
                    part1, part2 = pull.recv_pyobj()
                    worker_result.send_pyobj(self.merge(part1, part2, workerNumber))
                if killer in socks and socks[killer] == zmq.POLLIN:
                    print "KILL"
                    sys.exit(0)

    def testDistributed(self, arrayNumber, workersNumber):
        context = zmq.Context()

        push = context.socket(zmq.PUSH)
        push.bind("ipc:///tmp/push")
        killer = context.socket(zmq.PUB)
        killer.bind("ipc:///tmp/killer")
        worker_result = context.socket(zmq.PULL)
        worker_result.bind("ipc:///tmp/worker_result")

        for w in range(workersNumber):
            self.spawn_worker(w)
        gen = [random.randint(0, arrayNumber) for _ in xrange(arrayNumber)].__iter__()

        poller = zmq.Poller()
        poller.register(worker_result, zmq.POLLIN)
        poller.register(push, zmq.POLLOUT)
        results = []
        while True:
            socks = dict(poller.poll())
            if worker_result in socks and socks[worker_result] == zmq.POLLIN:
                result = worker_result.recv_pyobj()
                if len(result) == arrayNumber:
                    killer.send_pyobj("KILL")
                    assert result == sorted(result)
                    print ("Wynik: ", sorted(result))
                    break
                else:
                    results.append(result)
                    if len(results) == 2:
                        push.send_pyobj(results)
                        results = []
            if push in socks and socks[push] == zmq.POLLOUT:
                try:
                    push.send_pyobj(([gen.next()], [gen.next()]))
                except StopIteration:
                    poller.unregister(push)



