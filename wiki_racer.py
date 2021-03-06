execfile('imports.py')

class WikiRacer(object):
    """docstring for WikiRacer"""
    def __init__(self, start_url, end_url):
        super(WikiRacer, self).__init__()
        self.start_url = start_url
        self.end_url = end_url
        self.child_parent_urls = {}
        self.visited = set()
        self.domain = "https://en.wikipedia.org"
        self.urls_to_crawl_queue = Queue.Queue()
        self.urls_to_crawl_queue.put(start_url)

    def run_race(self):
        # going to store url relationships like url: parent_url
        while True:
            current_url = self.urls_to_crawl_queue.get()
            chunk = urllib.urlopen(current_url).read()
            utils.visit(self, current_url, chunk)

if __name__ == '__main__':
    try:
        urls = utils.get_url_args()
        start_url = urls['start']
        end_url = urls['end']
        racer = WikiRacer(start_url, end_url)
        racer.run_race()
    except ValueError as e:
        print ("Encountered error during main method:\n"
            "'" + sys.argv[1] + "' \nis not a valid json string. Please run method with json string in format:\n"
            "'{\n  \"start\": \"<starting article>\",\n  \"end\": \"<ending article>\"\n}'")



