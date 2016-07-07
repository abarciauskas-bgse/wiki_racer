import re
import unittest
execfile('wiki_racer.py')

class TestWikiRacerMethods(unittest.TestCase):
    def test_init(self):
        # it should throw an error if start or end url is not a valid url
        with self.assertRaises(TypeError) as context:
            WikiRacer()

    def test_get_urls(self):
        racer = WikiRacer("test_start_url", "test_end_url")
        # it should return an empty list if the url is bad
        self.assertEqual(racer.get_urls(""), set())
        simp_url = "https://en.wikipedia.org/wiki/Simplicial_approximation_theorem"
        # FIXME: This is a brittle test, depends on page, should use a wiki page stub
        expected_url = "".join([racer.domain, "/wiki/Mathematics"])
        self.assertTrue(expected_url in racer.get_urls(simp_url))

    def test_path(self):
        racer = WikiRacer("test_start_url", "test_end_url")
        racer.child_parent_urls = {'url2': 'url1', 'url3': 'url1', 'url4': 'url2', 'url5': 'url2', 'url6': 'url3', 'url1': 'test_start_url', 'test_end_url': 'url6'}
        self.assertEqual(racer.path('test_end_url'), ['test_start_url', 'url1', 'url3', 'url6', 'test_end_url'])


if __name__ == '__main__':
    unittest.main()    
