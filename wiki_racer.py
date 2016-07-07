from bs4 import BeautifulSoup
import urllib
import re   
import json
import time, random
import os
import json
import sys

class WikiRacer(object):
    """docstring for WikiRacer"""
    def __init__(self, start_url, end_url):
        super(WikiRacer, self).__init__()
        self.start_url = start_url
        self.end_url = end_url
        self.child_parent_urls = {}
        self.visited = set()
        self.domain = "https://en.wikipedia.org"

    def get_urls(self, url):
        # get page string
        try:
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html, "html.parser")
            # FIXME: only get hrefs in wiki content - not sure this is correct
            content = soup.find("div", {"id": "content"})
            links_html = content.find_all("a")
            urls = set()
            for link in links_html:
                if 'href' in link.attrs.keys():
                    href = link['href']
                    if not href[0] == '#': urls.add("".join([self.domain, href]))
            return urls
        except:
            return set()

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

    def add_parent_child(self, parent, child):
        self.child_parent_urls[child] = parent

    def visit(self, url):
        self.visited.add(url)
        child_urls = self.get_urls(url)
        if self.end_url in child_urls:
            self.child_parent_urls[self.end_url] = url
            return [url, True, set()]
        else:
            # REVIEW: Should there be concern about overriding existing path here?
            [self.add_parent_child(url, p) for p in child_urls]
            return [url, False, child_urls.difference(self.visited)]

    def run_race(self):
        # going to store url relationships like url: parent_url
        url_queue = [self.start_url]
        while True:
            current_url = url_queue.pop(0)
            current_child_urls = self.get_urls(current_url)
            self.visited.append(current_url)
            for url in current_child_urls:
                if url == end_url:
                    self.child_parent_urls[url] = current_url
                    return self.path(url)
                elif url not in self.visited:
                    url_queue.append(url)
                    self.child_parent_urls[url] = current_url


if __name__ == '__main__':
    # FIXME: Throw an informative error if cannot parse json start and end url
    try:
        json_str = sys.argv[1]
        urls = json.loads(json_str)
        start_url = urls['start']
        end_url = urls['end']
        racer = WikiRacer(start_url, end_url)
        print racer.run_race()
    except ValueError as e:
        print ("Encountered error during main method:\n"
            "'" + sys.argv[1] + "' \nis not a valid json string. Please run method with json string in format:\n"
            "'{\n  \"start\": \"<starting article>\",\n  \"end\": \"<ending article>\"\n}'")



