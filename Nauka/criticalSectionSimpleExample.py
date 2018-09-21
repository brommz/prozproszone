from threading import Thread, Lock

licz_watkow = 8
zamek = Lock()


class Watek(Thread):
    def __init__(self, numer):
        self.numer = numer
        Thread.__init__(self)

    def run(self):
        #with zamek:
            print("Poczatek sekcji kryt. watku", self.numer)
            print("Koniec sekcji kryt. watku", self.numer)


watki = []
for i in range(licz_watkow):
    watki.append(Watek(i))
    watki[i].start()

for watek in watki:
    watek.join()
