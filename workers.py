import random

def worker(count, out_list):
  for _ in range(count):
    out_list.append(random.random())

