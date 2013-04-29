import unittest
from crawler import Balerian

class TestBalarian(unittest.TestCase):
    def setUp(self):
        self.bela = Balerian('http://rohitjangid.com')
    
    def test_functioning(self):
        self.assertEqual(27, self.bela.crawl())
        
if __name__ == '__main__':
    unittest.main()
