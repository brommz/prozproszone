from MasterWorker import MasterWorker
# from SlaveWorker import SlaveWorker

if __name__ == "__main__":
    mainWorker = MasterWorker()
    mainWorker.init(0)
    mainWorker.run(50, None) #[10,9,8,7,6,5,4,3,2,1]
