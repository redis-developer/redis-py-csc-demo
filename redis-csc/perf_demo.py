from config import *
from tqdm import tqdm
import time
from redis import Redis
from redis.cache import CacheConfig
import random
import string

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


'''
Mix some reads and writes with a ratio of 1:2

1. Operate on 10K keys
2. Perform a write to a String
3. Perform two read operations on the same String££
'''
def run_sequential_workload_1_to_2(r_write, r_read, num_keys, value_size):
    for i in tqdm(range(num_keys), desc="Running workload"):
        r_write.set("key:{}".format(i), random_string(value_size))
        r_read.get("key:{}".format(i))
        r_read.get("key:{}".format(i))


if __name__ == "__main__":

    NUM_KEYS = 10000
    VALUE_SIZE = 50
    CACHE_SIZE = 1000

    r_uncached = Redis(host=DB_CONFIG['host'], port=DB_CONFIG['port'], password=DB_CONFIG['password'])
    r_cached = Redis(host=DB_CONFIG['host'], port=DB_CONFIG['port'], password=DB_CONFIG['password'],
                        protocol=3, cache_config=CacheConfig(max_size=CACHE_SIZE))

    print("Running the workload with an uncached connection ...")
    r_uncached.flushdb()
    stopwatch(run_sequential_workload_1_to_2, r_uncached, r_uncached, NUM_KEYS, VALUE_SIZE)

    print("Running the workload with a cached connection ...")
    r_uncached.flushdb()
    stopwatch(run_sequential_workload_1_to_2, r_uncached, r_cached, NUM_KEYS, VALUE_SIZE)




