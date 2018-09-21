from multiprocessing import Process, Pipe
from MergeSortAlgorithm import MergeSortAlgorithm


class MergeSortParallel:
    def __init__(self, simpleLock):
        self._mergeSortAlg = MergeSortAlgorithm()
        self.simpleLock = simpleLock

    def testMergeSortParallel(self, array, procNumber):
        # inicjalizuje proces, przesylam mu cala liste, pipe tez zeby otrzymac odpowiedz
        pconn, cconn = Pipe()
        p = Process(target=self.mergeSortParallel, args=(array, cconn, procNumber))
        p.start()
        resultedArray = pconn.recv()

        # blokowanie na czas nieotrzymaania odpowiedzi (posortowanej listy)
        p.join()
        return resultedArray


    # dostaje liste, conn (pipe do rodzica). Robi mergesort lewej i prawej rownolegle,
    # pozniej merguje i zwraca poprzez pipe do rodzica
    def mergeSortParallel(self, array, conn, procNum):
        with self.simpleLock:
            print("mergeSortParallel procNum = ", procNum)
        if procNum <= 0 or len(array) <= 1:
            conn.send(self._mergeSortAlg.mergesort(array))
            conn.close()
            return

        ind = len(array)//2

        # inicjalizuje proces, przesylam mu lewa czesc listy, pipe tez zeby otrzymac odpowiedz
        pconnLeft, cconnLeft = Pipe()
        leftProc = Process(target=self.mergeSortParallel, args=(array[:ind], cconnLeft, procNum - 1))

        # inicjalizuje proces, przesylam mu prawa czesc listy, pipe tez zeby otrzymac odpowiedz
        pconnRight, cconnRight = Pipe()
        rightProc = Process(target=self.mergeSortParallel, args=(array[ind:], cconnRight, procNum - 1))

        # startuje procesy
        leftProc.start()
        rightProc.start()

        conn.send(self._mergeSortAlg.merge(pconnLeft.recv(), pconnRight.recv()))
        conn.close()

        # czekam na te dwa procesy jak sie zakoncza
        leftProc.join()
        rightProc.join()