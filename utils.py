from bs4 import BeautifulSoup
import json
import os
import urllib
import urlparse
import argparse

def get_url_args():
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-r','--raw', help='Description for foo argument', required=True)
    args = vars(parser.parse_args())
    raw = args['raw']
    return json.loads(raw)

def is_absolute(url):
     return bool(urlparse.urlparse(url).netloc)

def path(object, url):
    path = [url]
    current_url = url
    children = object.child_parent_urls.keys()
    while True:
        if current_url in children:
            parent = object.child_parent_urls[current_url]
            path.insert(0, parent)
            current_url = parent
        else:
            break
    return path

def visit(object, url, chunk):
    object.visited.add(url)
    # Parse the chunk
    soup = BeautifulSoup(chunk, "html.parser")
    # Only get hrefs in wiki content
    content = soup.find("div", {"id": "content"})
    links_html = content.find_all("a")
    for link in links_html:
        if 'href' in link.attrs.keys():
            href = link['href']
            if not href[0] == '#' and not is_absolute(href):
                new_url = "".join([object.domain, href])
                object.child_parent_urls[new_url] = url
                if new_url == object.end_url:
                    print json.dumps({
                        'start': object.start_url,
                        'end': object.end_url,
                        'path': path(object, object.end_url)}, indent=4)
                    os._exit(1)
                if new_url not in object.visited:
                    object.urls_to_crawl_queue.put(new_url)
