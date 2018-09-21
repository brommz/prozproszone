from MergeSortDistributed import MergeSortDistributed


def main():
    tester = MergeSortDistributed()
    N = int(raw_input('Podaj wielkosc tablicy: '))
    workersNumber = int(raw_input('Podaj liczbe workerow: '))
    tester.testDistributed(N, workersNumber)

if __name__ == "__main__":
    main()