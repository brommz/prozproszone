#!/usr/bin/python
from threading import Thread


def hello(napis):
    print(napis)

class HelloThread(Thread):

    def run(self):
        print("1 Watek wita serdecznie !")


if __name__ == '__main__':
    t = HelloThread()
    t.start()
    print("1 Watek uruchomiony !")
    t.join()

    t = Thread(target=hello, args=("2 start",))
    t.start()
    print("222ny !")
    t.join()
    #opcjonaln