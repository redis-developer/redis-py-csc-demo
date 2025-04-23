from config import *
from tqdm import tqdm
import time
import threading
from enum import Enum
from redis import Redis
from redis.cache import CacheConfig
import random
import string


''' 
Available workloads
'''
class Workload(Enum):
    OTHER_WORKLOAD = 0
    SEQUENTIAL_WR_1_TO_2 = 1


'''
Generate a random string of a given length
'''
def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


'''
Measure the time that the execution of a given function takes
'''
def stopwatch(func, *args, **kwargs):
    start_time = time.perf_counter()
    func(*args, **kwargs)
    end_time = time.perf_counter()
    print("The function '{}' took {:.4f} seconds.".format(func.__name__, end_time - start_time))



'''
Warm the keyspace up with a number of keys
'''
def warmup(r, num_keys, value_size):
    for i in range(num_keys):
        print(i)
        r.set("key:{}".format(i), random_string(value_size))



def run_workload(workload, num_workers, r_write, r_read, num_keys, value_size):
    workers = []
    keys_per_thread = int(num_keys / num_workers)
    keys_rest = num_keys - (num_keys * num_workers)

    for worker_id in range(num_workers):
        num_keys = keys_per_thread
        if worker_id == num_workers - 1:
            num_keys += keys_rest

        if workload.value == Workload.SEQUENTIAL_WR_1_TO_2.value:
            worker = threading.Thread(target=run_sequential_workload_1_to_2, args=(worker_id, r_write, r_read, num_keys, value_size))
            workers.append(worker)
            worker.start()

    # Wait until all workers are done
    for w in workers:
        w.join()
'''
Mix some reads and writes with a ratio of 1:2

1. Operate on 10K keys
2. Perform a write to a String
3. Perform two read operations on the same String££
'''
def run_sequential_workload_1_to_2(worker_id, r_write, r_read, num_keys, value_size):
    for i in range(num_keys):
        r_write.set("key:{}:{}".format(worker_id, i), random_string(value_size))
        r_read.get("key:{}:{}".format(worker_id, i))
        r_read.get("key:{}:{}".format(worker_id, i))




if __name__ == "__main__":

    NUM_KEYS = 10000
    VALUE_SIZE = 50
    CACHE_SIZE = 1000
    NUM_THREADS = 20
    WORKLOAD = Workload.SEQUENTIAL_WR_1_TO_2

    r_write = Redis(host=DB_CONFIG['host'], port=DB_CONFIG['port'], password=DB_CONFIG['password'])
    r_uncached = Redis(host=DB_CONFIG['host'], port=DB_CONFIG['port'], password=DB_CONFIG['password'])
    r_cached = Redis(host=DB_CONFIG['host'], port=DB_CONFIG['port'], password=DB_CONFIG['password'],
                        protocol=3, cache_config=CacheConfig(max_size=CACHE_SIZE))

    r_uncached.flushdb()
    print("Running the workload with an uncached connection ...")
    stopwatch(run_workload, WORKLOAD, NUM_THREADS, r_write, r_uncached, NUM_KEYS, VALUE_SIZE)

    print("Enabling caching ...")
    time.sleep(5)

    print("Running the workload with a cached connection ...")
    stopwatch(run_workload, WORKLOAD, NUM_THREADS, r_uncached, r_cached, NUM_KEYS, VALUE_SIZE)




