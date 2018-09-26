# wordcount
PySpark wordcount example with logging from driver as well as executors/workers to remote log management service (Loggly)


## Problem
When writing Spark program in Python, logging from driver works fine.
However, logging from any map function is hard because it runs in separate machine.

Basically, Spark is distributed computing framework but `logging` module is single machine/process library.

## Solution
Solution for this problem are two steps:

* Use remote log management service (can be cloud, Loggly in this example)
* Configure `logging` module in both master node and worker nodes using same configuration

## Try this example

* `git clone git@github.com:chhantyal/wordcount.git && cd wordcount`
* `pip install -r requirements.txt`
* `spark-submit --py-files loggly_conf.py  wordcount.py -i samples/input.txt -k [LOGGLY_CUSTOMER_KEY]`
