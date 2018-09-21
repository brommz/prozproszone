from multiprocessing import Process, Pipe
from MergeSortAlgorithm import MergeSortAlgorithm
from threading import Lock
import sys

class MergeSortMultiprocess:
    def __init__(self):
        self._mergeSortAlg = MergeSortAlgorithm()

    def testMergeSort(self, array, procNumber):
        # inicjalizuje proces, przesylam mu cala liste, pipe tez zeby otrzymac odpowiedz
        pconn, cconn = Pipe()

        lock = Lock()
        p = Process(target=self.mergeSortProcess, args=(array, cconn, procNumber, lock, sys.stdout))
        p.start()

        resultedArray = pconn.recv()

        # blokowanie na czas nieotrzymaania odpowiedzi (posortowanej listy)
        p.join()
        return resultedArray


    # dostaje liste, conn (pipe do rodzica). Robi mergesort lewej i prawej rownolegle,
    # pozniej merguje i zwraca poprzez pipe do rodzica
    def mergeSortProcess(self, array, conn, procNum, lock, stream):
        with lock:
            stream.write("mergeSortParallel procNum = " + str(procNum) + ", array: " + str(array) + '\n')
        if procNum <= 0 or len(array) <= 1:
            conn.send(self._mergeSortAlg.mergesort(array))
            conn.close()
            return

        ind = len(array)//2

        # inicjalizuje proces, przesylam mu lewa czesc listy, pipe tez zeby otrzymac odpowiedz
        pconnLeft, cconnLeft = Pipe()
        leftProc = Process(target=self.mergeSortProcess, args=(array[:ind], cconnLeft, procNum - 1, lock, stream))

        # inicjalizuje proces, przesylam mu prawa czesc listy, pipe tez zeby otrzymac odpowiedz
        pconnRight, cconnRight = Pipe()
        rightProc = Process(target=self.mergeSortProcess, args=(array[ind:], cconnRight, procNum - 1, lock, stream))

        # startuje procesy
        leftProc.start()
        rightProc.start()

        conn.send(self._mergeSortAlg.merge(pconnLeft.recv(), pconnRight.recv()))
        conn.close()

        # czekam na te dwa procesy jak sie zakoncza
        leftProc.join()
        rightProc.join()