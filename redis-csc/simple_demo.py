from config import *
import time
from redis import Redis
from redis.cache import CacheConfig


def simple_demo():
    # Add a key via a control connection
    r_control = Redis(host=DB_CONFIG['host'], port=DB_CONFIG['port'], password=DB_CONFIG['password'])
    r_control.flushdb()
    r_control.hset("usr:dmaier", mapping={'first_name': 'David', 'last_name': 'Maier'})

    # The default policy is LRU
    cache_config = CacheConfig(max_size=10000)
    r_cached = Redis(host=DB_CONFIG['host'], port=DB_CONFIG['port'], password=DB_CONFIG['password'],
                     protocol=3, cache_config=cache_config)

    print('Reading from the Redis server ...')
    r_cached.hgetall("usr:dmaier")
    cache = r_cached.get_cache()
    print('The cache has {} elements'.format(cache.size))
    print('Executing the same read command again ...')
    user = r_cached.hgetall("usr:dmaier")
    print('Fetched entry from local cache: {}'.format(user))
    print('Invalidating the data by adding a property ...')
    r_control.hset("usr:dmaier", mapping={'age': 44})
    time.sleep(0.1)
    print('Executing the same read command again ...')
    user = r_cached.hgetall("usr:dmaier")
    print('Fetched entry from local cache: {}'.format(user))


if __name__ == "__main__":
    simple_demo()
