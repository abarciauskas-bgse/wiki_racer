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

    def run_race(self):
        # going to store url relationships like url: parent_url
        while True:
            current_url = urls_to_crawl_queue.get()
            chunk = urllib.urlopen(current_url).read()
            utils.visit(self, current_url, chunk)

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
        racer = WikiRacer(start_url, end_url)
        racer.run_race()
    except ValueError as e:
        print ("Encountered error during main method:\n"
            "'" + sys.argv[1] + "' \nis not a valid json string. Please run method with json string in format:\n"
            "'{\n  \"start\": \"<starting article>\",\n  \"end\": \"<ending article>\"\n}'")



