import time
from workers import worker

if __name__ == "__main__":
 



    start_time = time.time()
    # print(start_time)
    size = 10000000 
    n_exec = 10
    for i in range(0, n_exec):
        out_list = list()
        worker(size, out_list)
  

     
    print ("List processing complete.")
    end_time = time.time()
    print("serial time=", end_time - start_time)


