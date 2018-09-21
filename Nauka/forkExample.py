from os import fork, getpid, wait
from sys import exit

if __name__ == '__main__':
    wynik = fork()

if wynik == -1:
    exit(-1)
elif wynik == 0:
    print("Jestem dzidziusiem, moj pid to: ", getpid())
else:
    print("Zostalem tatusiem, moj pid to: ", getpid(), ", a mojego dziecka: ", wynik)
    wait()
