from bs4 import BeautifulSoup
import urllib
import re   
import json
import time, random
import os
import json
import sys
import urllib
import Queue
import threading
import urlparse
import argparse

def is_absolute(url):
     return bool(urlparse.urlparse(url).netloc)

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, urls_to_crawl_queue, crawled_pages_queue):
        threading.Thread.__init__(self)
        self.urls_to_crawl_queue = urls_to_crawl_queue
        self.crawled_pages_queue = crawled_pages_queue

    def run(self):
        while True:
            #grabs host from urls_to_crawl_queue
            url = self.urls_to_crawl_queue.get()

            #grabs urls of hosts and then grabs chunk of webpage
            page = urllib.urlopen(url)
            chunk = page.read()

            #place chunk into out urls_to_crawl_queue
            self.crawled_pages_queue.put([url, chunk])

class DatamineThread(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, urls_to_crawl_queue, crawled_pages_queue):
        threading.Thread.__init__(self)
        self.urls_to_crawl_queue = urls_to_crawl_queue
        self.crawled_pages_queue = crawled_pages_queue
        self.visited = set()
        self.child_parent_urls = {}

    def path(self, url):
        path = [url]
        current_url = url
        children = self.child_parent_urls.keys()
        while True:
            if current_url in children:
                parent = self.child_parent_urls[current_url]
                path.insert(0, parent)
                current_url = parent
            else:
                break
        return path

    def run(self):
        while True:
            #grabs host from urls_to_crawl_queue
            url, chunk = self.crawled_pages_queue.get()
            self.visited.add(url)

            #parse the chunk
            soup = BeautifulSoup(chunk, "html.parser")
            # FIXME: only get hrefs in wiki content - not sure this is correct
            content = soup.find("div", {"id": "content"})
            links_html = content.find_all("a")
            for link in links_html:
                if 'href' in link.attrs.keys():
                    href = link['href']
                    if not href[0] == '#' and not is_absolute(href):
                        new_url = "".join([domain, href])
                        self.child_parent_urls[new_url] = url
                        if new_url == end_url:
                            print self.path(end_url)
                            os._exit(1)
                        if new_url not in self.visited: urls_to_crawl_queue.put(new_url)


urls_to_crawl_queue = Queue.Queue()
crawled_pages_queue = Queue.Queue()
domain = "https://en.wikipedia.org"

start = time.time()
def main():
    #spawn a pool of threads, and pass them urls_to_crawl_queue instance
    for i in range(5):
        t = ThreadUrl(urls_to_crawl_queue, crawled_pages_queue)
        t.setDaemon(True)
        t.start()

    for i in range(5):
        dt = DatamineThread(urls_to_crawl_queue, crawled_pages_queue)
        dt.setDaemon(True)
        dt.start()

    #wait on the urls_to_crawl_queue until everything has been processed
    urls_to_crawl_queue.join()
    crawled_pages_queue.join()

if __name__ == '__main__':
    # FIXME: Throw an informative error if cannot parse json start and end url
    try:
        parser = argparse.ArgumentParser(description='Description of your program')
        parser.add_argument('-r','--raw', help='Description for foo argument', required=True)
        args = vars(parser.parse_args())
        raw = args['raw']
        urls = json.loads(raw)
        start_url = urls['start']
        end_url = urls['end']
        urls_to_crawl_queue.put(start_url)
        main()
    except ValueError as e:
        print ("Encountered error during main method:\n"
            "'" + sys.argv[1] + "' \nis not a valid json string. Please run method with json string in format:\n"
            "'{\n  \"start\": \"<starting article>\",\n  \"end\": \"<ending article>\"\n}'")

print "Elapsed Time: %s" % (time.time() - start)
