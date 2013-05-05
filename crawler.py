"""

front facing module for crawler. 
format: python crawler.py [root_url] [ALLOW_EXTERNAL] [ALLOW_REDIRECTS]

"""

import sys
import robotparser
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
import logging, logging.config
import urlparse
from bs4 import BeautifulSoup
from logs import LOGGING
from urlnorm import url_normalize
from utils import PriorityQueue, BalerionRedirectHandler, AttrDict

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger("crawler_logger")
ROBOT = robotparser.RobotFileParser()

class Balerion(object):
    """
        Once the largest dragon in westeros, also the name this simple python web crawler :-) .
    """
    def __init__(self, link, allow_external, allow_redirects, max_limit = 10):
        self.root = link
        self.unparsed_urls = PriorityQueue()
        self.allow_external = allow_external
        self.allow_redirects = allow_redirects
        self.domain = None
        self.max_limit = max_limit
        self.opener = None
        self.create_opener()
    
    def pre_process(self):
        """
        placeholder
        """
        if(self.allowed_for_processing(self.root)):
            self.unparsed_urls.add(self.root, priority = 0)
            parsed_url = urlparse.urlparse(self.root)
            self.domain = parsed_url.netloc
        else:
            LOGGER.warning("Non followable root: %s " % self.root)
            exit()
    
    def process_page(self, response) :
        """
            override this method to do any kind of processing on the page. 
        """
        pass
    
    def create_opener(self):
        """
            creates http-link opener based on options choosen
        """
        self.opener = urllib2.build_opener()
        if not self.allow_redirects:
            self.opener = urllib2.build_opener(BalerionRedirectHandler)    
    
    @classmethod
    def allowed_for_processing(cls, next_url):
        """
        placeholder
        """
        parsed_url = urlparse.urlparse(next_url)
        if(parsed_url.scheme != 'http'):
            LOGGER.warning("Non followable URl: %s " % next_url)
            return False
        ROBOT.set_url(parsed_url.scheme + parsed_url.netloc + "/robots.txt")
        if not ROBOT.can_fetch('Balerion', next_url.encode('ascii', 'replace')):
            LOGGER.warning("Url disallowed by robots.txt: %s " % next_url)
            return False
        return True
        
    def process_page_links(self, raw_html, url):
        """
        placeholder
        """
        beautiful_html = BeautifulSoup(raw_html)
        
        links = [a.get('href') for a in beautiful_html.find_all('a')]
        links = [link for link in links if link is not None]
        
        for link in links:
            link_info = urlparse.urlparse(link)
            
            if not link_info.scheme and not link_info.netloc:
                link = urlparse.urljoin(url, link)
                link_info = urlparse.urlparse(link)
            
            if('http' not in link_info.scheme) : continue
            
            if self.domain not in link_info.netloc:
                if not self.allow_external :
                    continue  # throwing out external link
                else:
                    priority = 2  # insert external link with low priority
            else:
                priority = 1
            self.unparsed_urls.add(link, priority)
    
    def fetch_url(self, url):
        """
        placeholder
        """
        page = AttrDict()
        try:
            # getting response from given URL
            resp = self.opener.open(unicode(url))
            page = AttrDict({
                'body': resp.read(),
                'url': resp.geturl(),
                'headers': AttrDict(dict(resp.headers.items())),
                'status': resp.getcode()
            })
        except urllib2.HTTPError, err :
            if err.code == 404:
                page = AttrDict({'status': 404})
                LOGGER.exception("page not found : %s at %s" % (err.code, url))
            elif err.code == 403:
                page = AttrDict({'status': 403})
                LOGGER.error("access denied : %s at %s " % (err.code, url))
            else:
                page = AttrDict({'status': 500}) #choosing 500 as default bad access code
                LOGGER.error("something bad happened : %s at %s " % (err.code, url)) 
        
        except urllib2.URLError, err:
            page = AttrDict({'status': 500})
            LOGGER.error("server error %s at %s " % (err.reason, url))
        
        return page
            
    def crawl(self):
        """
            placeholder
        """
        self.pre_process()
        LOGGER.info("starting at (%s)... "% self.root)
        count = 0
        while self.unparsed_urls.heap and count < self.max_limit:
            # getting link to get
            url = self.unparsed_urls.get()
            count += 1
            # fetching page
            page = self.fetch_url(url)
            if page.status not in [404, 403, 500] and 'text/html' in page.headers['content-type']:
                LOGGER.info("visited: %s " % (url))
                self.process_page(page)
                self.process_page_links(page.body, page.url)   
        return count
if __name__ == '__main__':
    
    try:
        INPUT_URL = sys.argv[1]
        ALLOW_EXTERNAL  = sys.argv[2]
        ALLOW_REDIRECTS = sys.argv[3]
        MAX_LIMIT = sys.argv[3]
    except IndexError:
        LOGGER.info("Error: Incorrect start url / external options were passed")
        exit()
    
    BELA = Balerion(url_normalize(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    BELA.crawl()
        
        
