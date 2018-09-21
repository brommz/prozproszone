from threading import Thread, Lock;

licz_watkow = 2
N = 4 * 360e4
suma = 0
zamek = Lock()


class dodawacz(Thread):
    def __init__(self, nr):
        self.nr = nr
        Thread.__init__(self)

    def run(self):
        global N
        global suma
        ile = int(N / licz_watkow)
        s = 0
        for i in range((self.nr - 1) * ile, self.nr * ile, 1):
            s += 1
        with zamek:
            suma += s

watki = []
for i in range(0, licz_watkow, 1):
    watki.append(dodawacz(i))
    watki[i].start()
for watek in watki:
    watek.join()
print("wynik = ", suma)
