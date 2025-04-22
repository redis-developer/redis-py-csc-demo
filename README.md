# Python client-side caching demo

A simple demo application that showcases client-side caching with `redis-py`.


## Requirements

You need to use the following components to run the demo:

* Python 3.9 or higher is recommended
* Pip as the package installer
* Redis Cloud with a databaase that uses the Redis API version 7.4 or higher


## How to run

* Edit the file `redis-csc/config.py` and enter your Redis connection details.
```
DB_CONFIG = {
    'host': '<host>',
    'port': <port>,
    'password' : '<password>',
}
```

* Ensure that you install the dependencies via `pip`.
```
pip install -r requirements.txt
```

* Run the simple demo via `python`.
```
cd redis-csc
python simple_demo.py
```

* Modify some test constants in the `perf_demo,py` script.

* Run the application via `python`.
```
python perf_demo.py
```
