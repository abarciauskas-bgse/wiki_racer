# WikiRacer Design

`wiki_racer.py` contains a brute force approach. The brute force approach is to use a queue of urls to visit, keep track of pages visited so far, and keep track of the path using a dictionary, `child_parent_urls`. Keys in `child_parent_urls` are urls and values are urls of the page where the respective url key was found. This facilitates reconstruction of the path used to find the endpoint without requiring maintenance of each unique path, which would be explosive.

For each url on the queue, the process is as follows:

1. Dequeue the first url from the url queue (`current_url`).
2. Fetch the wiki page located at `current_url`.
3. Iterate through wikipedia urls on the retrieved wiki page: Add or update `child_parent_urls[url] = current_url`. If the url is equal to the endpoint, return the path used to reach the endpoint. If the url is not equal to the endpoint and has not already been visited, append the url to the queue.

For the multi-threaded version, the logic is similar, but with important modifications:

* A pool of threads is used to do steps 1 and 2 and dumps the url plus its html contents on a queue for processing. This parallelizes the network calls.
* A pool of threads parses each page and does the work in step 3. This parallelizes the work of parsing urls from html and checking for the endpoint.

# Future Times

* Tests for multi-threaded version
* If the race is to be run many times, it may be useful to develop some heuristics that speed up the process; for example focusing on pages which may be "hubs", such that it is more likely to find remote pages from the current page. Delay urls which are more likely to be irrelevant because they are some very specific topic. This is trickey because it is also possible this is what is needed. Perhaps look at the similarity between the contents of the start and end pages and determine if these pages are going to be `near` or `far` from each other in the wiki graph.
* Determing if concurrency via multiple processes delivers substantial performance gains. This could be relatively easy by simple partitioning the first set of page urls into the number of cores available and then running `wiki_racer_multi` in each process
* Add options for diagnosing bottlenecks (e.g. threadprofiler)
* Add options for benchmarking performance (e.g. timer)

