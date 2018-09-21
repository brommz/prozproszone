import sys

from SlaveWorker import SlaveWorker

if __name__ == "__main__":
    arg = None
    if(len(sys.argv) == 1):
        print "Blad"
        arg = 1
    else:
        arg = sys.argv[1]

    print "RunnerStart slave worker: ", arg

    slaveWorker = SlaveWorker()
    slaveWorker.init(sys.argv[0])
    slaveWorker.run()