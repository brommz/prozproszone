from threading import Thread, Semaphore
from time import sleep


class producent(Thread):
    def __init__(self, buf, niepusty):
        self.buf = buf
        self.niepusty = niepusty
        Thread.__init__(self)
    def produkuj(self):
        print("\tProducent produkuje:")
        return 12
    def run(self):
        obiekt = None
        while 1:
            obiekt = self.produkuj()
            self.buf.append(obiekt)
            self.niepusty.release()
            sleep(1)



class konsument(Thread):
    def __init__(self, buf, niepusty):
        self.buf = buf
        self.niepusty = niepusty
        Thread.__init__(self)
    def konsumuj(self, obiekt):
        print("\tKonsument konsumuje:", obiekt)
    def run(self):
        i = 0
        while 1:
            self.niepusty.acquire()
            obiekt = self.buf[i]
            i += 1
            self.konsumuj(obiekt)


if __name__ == "__main__":
    bufor = []
    sem_niepusty = Semaphore(0)
    prod = producent(bufor, sem_niepusty)
    kons = konsument(bufor, sem_niepusty)
    prod.start()
    kons.start()
