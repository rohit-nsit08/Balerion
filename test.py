import unittest
from crawler import Balerion

class TestBalarion(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_full_functioning(self):
        self.bela = Balerion('http://rohitjangid.com', 1, 1)
        self.assertEqual(10, self.bela.crawl())
    
    def test_no_external(self):
        self.bela = Balerion('http://rohitjangid.com', 0, 1)
        self.assertEqual(10, self.bela.crawl())
    
    def test_no_external_no_redirect(self):
        self.bela = Balerion('http://rohit-nsit08.github.com', 0, 0)
        self.assertEqual(1, self.bela.crawl())
    
    def test_external_no_redirect(self):
        self.bela = Balerion('http://rohit-nsit08.github.com', 1, 0)
        self.assertEqual(1, self.bela.crawl())
        
if __name__ == '__main__':
    unittest.main()
