import unittest
from crawler import Balerian

class TestBalarian(unittest.TestCase):
    def setUp(self):
        self.bela = Balerian('http://www.dmoz.org/', 1)
    
    def test_functioning(self):
        self.assertEqual(81, self.bela.crawl())
        
if __name__ == '__main__':
    unittest.main()
