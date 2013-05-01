import re
import robotparser
from urllib2 import Request
import urllib2
from collections import deque
from urlparse import urlparse
from bs4 import BeautifulSoup

class Balerian(object):
    """
        single class compiler
    """
    def __init__(self, link):
        self.root = link
        self.queue = deque([link])
        self.queue.append(0)
        self.visited = {}
        self.level = 0
        self.count = 0
    
    
    def allowed_for_processing(self, next_url):
        parsedUrl = urlparse(next_url)
        if(parsedUrl.scheme != 'http'):
            return False
        return True
        
    def crawl(self) :
        while(self.queue and self.count <= 100):
            next_url = self.queue.popleft()     
            
            if(next_url == 0):
                self.level += 1
                self.queue.append(0) 
                continue
                
            if(not self.allowed_for_processing(next_url)): continue

            self.visited[next_url] = True
        
            req = Request(next_url)
            response = urllib2.urlopen(req)
            header = response.info()
            if('text/html' not in header['Content-Type']) : continue
            
            print "read "+ next_url + " at level = "+str(self.level)
            self.count += 1
            
            data = response.read()
            soup = BeautifulSoup(data)
            ahrefs = soup.find_all('a')
            links = [a.get('href') for a in ahrefs]
            for link in links:
                if(link not in self.visited and link != None):
                    self.queue.append(link)
            
            
if __name__ == '__main__':
    print("enter the root url")
    input_url = raw_input()
    bela = Balerian(input_url)
    bela.crawl()
        
        
