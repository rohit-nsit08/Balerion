import re, sys
import robotparser
import urllib2
import traceback
import logging, logging.config
from urllib2 import Request
from collections import deque
import urlparse
from bs4 import BeautifulSoup
from settings import LOGGING
from urlnorm import url_normalize
from utils import Priority_Queue, BalerianRedirectHandler, AttrDict

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("crawler_logger")
robot = robotparser.RobotFileParser()

class Balerian(object):
    """
        Once the largest dragon in westeros, also the name this simple python web crawler :-) .
    """
    def __init__(self, link, allow_external, allow_redirects):
        self.root = link
        self.unparsed_urls = Priority_Queue()
        self.allow_external = allow_external
        self.allow_redirects = allow_redirects
        self.domain = None
        self.max_limit = 500
        self.seen = 1
        self.create_opener()
    
    def pre_process(self):
        if(self.allowed_for_processing(self.root)):
            self.unparsed_urls.add(self.root, priority = 0)
            parsedUrl = urlparse.urlparse(self.root)
            self.domain = parsedUrl.netloc
        else:
            logger.warning("Non followable URl: %s " % next_url)
            exit()
    
    def process_page(self, response) :
        """
            override this method to do any kind of processing on the page. 
        """
        pass
    
    def create_opener(self):
        
        self.opener = urllib2.build_opener()
        if not self.allow_redirects:
            self.opener = urllib2.build_opener(BalerianRedirectHandler)    
    
    def allowed_for_processing(self, next_url):
        parsedUrl = urlparse.urlparse(next_url)
        if(parsedUrl.scheme != 'http'):
            logger.warning("Non followable URl: %s " % next_url)
            return False
        robot.set_url(parsedUrl.scheme + parsedUrl.netloc + "/robots.txt")
        if not robot.can_fetch('Balerian', next_url.encode('ascii', 'replace')):
        		logger.warning("Url disallowed by robots.txt: %s " % next_url)
        		return False
        return True
        
    def process_page_links(self, raw_html, url):

        beautiful_html = BeautifulSoup(raw_html)
        
        links = [a.get('href') for a in beautiful_html.find_all('a')]
        links = filter(None, links)
        
        for link in links:
            self.seen += 1
            link_info = urlparse.urlparse(link)
            
            if not link_info.scheme and not link_info.netloc:
                link = urlparse.urljoin(url, link)
                link_info = urlparse.urlparse(link)
            
            # print self.domain, link_info.netloc
            
            if self.domain not in link_info.netloc:
                if not self.allow_external :
                    continue  # throwing out external link
                else:
                    priority = 2  # insert external link with low priority
            else:
                    priority = 1
            self.unparsed_urls.add(link, priority)
    
    def fetch_url(self, url):
            
        page = AttrDict()
        try:
            # getting response from given URL
            resp = self.opener.open(url)
            page = AttrDict({
                'body': resp.read(),
                'url': resp.geturl(),
                'headers': AttrDict(dict(resp.headers.items())),
                'status': resp.getcode()
            })
        except:
            # drop invalid page with 500 HTTP error code
            page = AttrDict({'status': 500})
        return page
            
    def crawl(self):

        self.pre_process()
        logger.info("starting (%s)... "% sys.argv[1])
        count = 0
        while self.unparsed_urls.heap and count < self.max_limit:
            # getting link to get
            priority, url = self.unparsed_urls.get()
            count += 1
            # fetching page
            page = self.fetch_url(url)
            if page.status not in [500, 404, 502] and 'text/html' in page.headers['content-type']:
                logger.info("visited: %s %s %s" % (url, count, self.seen))
                self.process_page(page)
                self.process_page_links(page.body, page.url)
        logger.info("finished, total urls encountered: %s " % (str(self.seen)))   

if __name__ == '__main__':
    
    try:
        input_url = sys.argv[1]
        allow_external  = sys.argv[2]
        allow_redirects = sys.argv[3]
    except IndexError:
        logger.info("Error: Incorrect start url / external options were passed")
        exit()
    
    bela = Balerian(url_normalize(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    bela.crawl()
        
        
