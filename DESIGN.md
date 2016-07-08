# WikiRacer Design

`wiki_racer.py` contains the single-threaded approach. The single-threaded approach keeps track of: a queue of urls to visit, a set of pages visited so far, and a dictionary of child-parent url relations, `child_parent_urls`. The latter facilitates reconstruction of the path used to find the endpoint without requiring maintenance of each unique path.

For each url on the queue, the process is as follows:

1. Dequeue a url from the url queue (`current_url`). Fetch the wiki page located at `current_url`.
2. Iterate through wikipedia urls on the retrieved wiki page: Add or update `child_parent_urls[url] = current_url`. If the url is equal to the endpoint, return the path used to reach the endpoint. If the url is not equal to the endpoint and has not already been visited, append the url to the queue.

`wiki_racer_multi.py` contains a multi-threaded approach. The logic and book-keeping is the same as for the single-threaded version, but with important modifications:

* A pool of threads is used to do step 1, each dumping the url plus its html contents on a queue for processing. This parallelizes the network calls.
* A pool of threads parses each page and does the work in step 2. This parallelizes the work of parsing urls from html and checking for the endpoint.

# Results

I timed results using the unix [`time`](https://developer.apple.com/legacy/library/documentation/Darwin/Reference/ManPages/man1/time.1.html) command on the same pair of urls to evaluate performance gains from using multiple threads. Times reported are total time elapsed as reported by `time`. E.g. `118.29s user 31.51s system 117% cpu 2:07.70 total`, 2:07.70 is reported.

| start_url (https://en.wikipedia.org/wiki/)                                          | end_url                                        | time single threaded | path single threaded | time multi threaded | path multi threaded |
|-----------------------------------------------------|------------------------------------------------|----------------------|----------------------|---------------------|---------------------|
| /Binomial_distribution | /Machine_learning | 6.034                | 5                    | 3.820               | 5                   |
| /French_fries          | /Beer             | 8.985                | 2                    | 4.922               | 2                   |
| /Binomial_distribution | /Beer             | 10:37.06             | 4                    | 2:07.70             | 4                   |


It is clear that a multi-threaded approach outperforms the single-threaded approach.


# Future Improvements

## Functionality

* Develop some heuristics to speed up the process using a priority queue and prioritize pages which are more likely to lead to the end_url. For example, it may help to use a priority queue which prioritizes pages which are likely to be "hubs" and de-prioritize urls which are more likely to be irrelevant because they are very specific. For example, it seems reasonable more general pages are linked to early in the article. This is trickey because it is also possible this is what is needed. Part of the this process may be to evaluate the similarity between the contents of the start and end pages and determine if these pages are going to be `near` or `far` from each other in the wiki graph.
* Evaluate if multiple processes delivers substantial performance gains. The implementation could be to partition the first set of page urls into the number of cores available and then running `wiki_racer_multi` on each available cpu.
* Diagnose bottlenecks (e.g. use a threadprofiler).

## Technical Improvements

* Refactor code such that the command to execute wiki_racer is always the same with the option for multiple threads as an argument.
* Write automated integration tests for `wiki_racer` and `wiki_racer_multi`.
* Write unit tests for any functionality in `utils.py` which is missing from existing unit tests.
* Add arg for input / output as json file.
* Fix `os._exit(1)` in `utils.py`. Need to exit from all threads when one finds the end_url. See [possible solution](http://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python). Note, however this would only stop the thread finding the path, so would need to store a globalvar of a stopping boolean and have all threads check it. This will delay termination of the program, but the impact should be small.

