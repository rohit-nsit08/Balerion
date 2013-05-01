import re, sys
import robotparser
import urllib2
import logging, logging.config
from urllib2 import Request
from collections import deque
from urlparse import urlparse
from bs4 import BeautifulSoup
from settings import LOGGING
import traceback

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("crawler_logger")
    
class Balerian(object):
    """
        single class crawler
    """
    def __init__(self, link, external):
        self.root = link
        self.queue = deque([link])
        self.queue.append(0)
        self.visited = {}
        self.level = 0
        self.count = 0
        self.external = external
    
    
    def allowed_for_processing(self, next_url):
        parsedUrl = urlparse(next_url)
        if(parsedUrl.scheme != 'http'):
            return False
        return True
        
    def crawl(self) :
        logger.info("starting (%s)... "% sys.argv[1])
        while(self.queue and self.count <= 100):
            next_url = self.queue.popleft()     

            if(next_url == 0):
                self.level += 1
                self.queue.append(0) 
                continue
                
            if(not self.allowed_for_processing(next_url)): continue

            self.visited[next_url] = True
        
            req = Request(next_url)
            try:
                response = urllib2.urlopen(req)
            except:
                logger.warning("Unfollowable link found at %s " % next_url)
                continue
            header = response.info()
            if('text/html' not in header['Content-Type']) : continue
            
            # print "read "+ next_url + " at level = "+str(self.level)
            logger.info("visited: %s at level %d" % (next_url, self.level))
            self.count += 1
            
            data = response.read()
            soup = BeautifulSoup(data)
            ahrefs = soup.find_all('a')
            links = [a.get('href') for a in ahrefs]
            for link in links:
                if(link not in self.visited and link != None):
                    self.queue.append(link)
            
            
if __name__ == '__main__':
    
    try:
        input_url = sys.argv[1]
        external  = sys.argv[2]
    except IndexError:
        logger.info("Error: Incorrect start url / external options were passed")
        exit()
    
    bela = Balerian(sys.argv[1], sys.argv[2])
    bela.crawl()
        
        
