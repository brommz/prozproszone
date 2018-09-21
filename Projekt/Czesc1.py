import random
from threading import Lock
from MergeSortParallel import MergeSortParallel


def main():
    # user ustala wielkosc tablicy i liczbe procesow
    N = int(raw_input('Podaj wielkosc tablicy: '))
    procNumber = int(raw_input('Podaj liczbe procesow: '))

    # generujemy losowa tablice
    array = [random.randint(1,1000) for x in range(N)]

    simpleLock = Lock()
    tester = MergeSortParallel(simpleLock)
    sortedArray = tester.testMergeSortParallel(array, procNumber)

    print("Tablica: ", array)
    print("Tablica posortowana: ", sortedArray)

def isSorted(lyst):
    for i in range(1, len(lyst)):
        if lyst[i] < lyst[i-1]:
            return False
    return True

if __name__ == '__main__':
    main()
