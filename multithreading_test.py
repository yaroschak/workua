import time
import threading
from workers import worker

#GIL
if __name__ == "__main__":
    start_time = time.time()
    size = 10000000
    threads = 10 
    jobs = []
    for i in range(0, threads):
        out_list = list()
        thread = threading.Thread(target=worker, args=(size,out_list))
        jobs.append(thread)

    for j in jobs:
            j.start()

    for j in jobs:
            j.join()

    print ("List processing complete.")
    end_time = time.time()
    print("multithreading time=", end_time - start_time)
    