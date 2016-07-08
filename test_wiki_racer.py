import unittest
import utils
execfile('wiki_racer.py')

class TestWikiRacerMethods(unittest.TestCase):
    def test_path(self):
        racer = WikiRacer("test_start_url", "test_end_url")
        racer.child_parent_urls = {'url2': 'url1', 'url3': 'url1', 'url4': 'url2', 'url5': 'url2', 'url6': 'url3', 'url1': 'test_start_url', 'test_end_url': 'url6'}
        self.assertEqual(utils.path(racer, 'test_end_url'), ['test_start_url', 'url1', 'url3', 'url6', 'test_end_url'])

    def test_visit(self):
        racer = WikiRacer("test_start_url", "test_end_url")
        simp_url = "https://en.wikipedia.org/wiki/Simplicial_approximation_theorem"
        new_url = "https://en.wikipedia.org/wiki/Mathematics"
        chunk = urllib.urlopen(simp_url)
        utils.visit(racer, simp_url, chunk)
        self.assertEqual(new_url, racer.urls_to_crawl_queue.get())
        self.assertTrue(simp_url in racer.visited)


if __name__ == '__main__':
    unittest.main()    
