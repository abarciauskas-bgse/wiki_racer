execfile('imports.py')

class CrawlThread(threading.Thread):
    """Open wiki urls"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.urls_to_crawl_queue = urls_to_crawl_queue
        self.crawled_pages_queue = crawled_pages_queue

    def run(self):
        while True:
            #grabs host from urls_to_crawl_queue
            url = self.urls_to_crawl_queue.get()
            #grabs urls of hosts and then grabs chunk of webpage
            try:
                page = urllib.urlopen(url)
                chunk = page.read()
                #place chunk into out urls_to_crawl_queue
                self.crawled_pages_queue.put([url, chunk])
            except IOError as e:
                print "rescued ioerror while trying to read: " + url

class ParsePagesThread(threading.Thread):
    """Parse wiki pages"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.urls_to_crawl_queue = urls_to_crawl_queue
        self.crawled_pages_queue = crawled_pages_queue
        self.visited = visited
        self.child_parent_urls = child_parent_urls
        self.domain = "https://en.wikipedia.org"
        self.end_url = end_url
        self.start_url = start_url

    def run(self):
        while True:
            #grabs host from urls_to_crawl_queue
            url, chunk = self.crawled_pages_queue.get()
            utils.visit(self, url, chunk)

def main():
    #spawn a pool of threads, and pass them urls_to_crawl_queue instance
    for i in range(5):
        t = CrawlThread()
        t.daemon = True
        t.start()

    for i in range(5):
        dt = ParsePagesThread()
        dt.daemon = True
        dt.start()

    #wait on the urls_to_crawl_queue until everything has been processed
    urls_to_crawl_queue.join()
    crawled_pages_queue.join()

urls_to_crawl_queue = Queue.Queue()
crawled_pages_queue = Queue.Queue()
visited = set()
child_parent_urls = {}

if __name__ == '__main__':
    # FIXME: Throw an informative error if cannot parse json start and end url
    try:
        urls = utils.get_url_args()
        start_url = urls['start']
        end_url = urls['end']
        urls_to_crawl_queue.put(start_url)
        main()
    except ValueError as e:
        print ("Encountered error during main method:\n"
            "'" + sys.argv[1] + "' \nis not a valid json string. Please run method with json string in format:\n"
            "'{\n  \"start\": \"<starting article>\",\n  \"end\": \"<ending article>\"\n}'")
