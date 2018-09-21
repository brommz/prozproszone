from MergeSortAlgorithm import MergeSortAlgorithm

class Worker():

    def __init__(self):
        self.mergeAlg = MergeSortAlgorithm()
        self.workerNumber = None
        self.context = None
        self.push = None
        self.pull = None
        self.killer = None
        self.worker_result = None
        self.poller = None

    def merge(self, part1, part2, workerNumber):
        print "Funkcja Merge, workerNumber = ", workerNumber
        print "\t" + "part1: ", part1
        print "\t" + "part2: ", part2
        return self.mergeAlg.merge(part1, part2)

    def init(self, workerNumber):
        pass

    def run(self, arraySize):
        pass