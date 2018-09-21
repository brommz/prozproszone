#!/usr/bin/python
from threading import Thread, Condition

wypelniona = 0
tab = []


class Czytacz(Thread):
    def run(self):
        global tab, wypelniona
        global zm_war
        print("Czytelnik")

        zm_war.acquire()

        while (wypelniona == 0): #chroni przed przedwczesnym budzeniem, nie stosować if!!!
            print("czekanie...")
            zm_war.wait() #otwiera atomowo zamek
        zm_war.release()
        for i in range(0, 10):
            print(i, ": tab = ", tab[i])

class Piszacz(Thread):
    def run(self):
        global tab, wypelniona
        global zm_war
        print("Pisarz wlasnie pisze")
        for i in range(1, 11):
            tab.append(1.0 / i / i)
            print(i, "Piszetab = ", 1.0 / i / i)
        zm_war.acquire()
        wypelniona = 1
        zm_war.notify()
        zm_war.release()

if __name__ == "__main__":
    zm_war = Condition()
    czyt = Czytacz()
    pisz = Piszacz()
    czyt.start()
    pisz.start()
