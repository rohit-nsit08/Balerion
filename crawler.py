import re
import urllib.request

class Balerian(object):
    
    def __init__(self, input_url):
        self.seed_target = input_url
        self.level = 1
        self.MAX_FETCH = 1000
    
    def crawl(self):
        link_exp = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
        req = urllib.request.Request(self.seed_target)
        while(True):
            try:
                response = urllib.request.urlopen(req)
                f = open('level_'+ str(self.level), 'w')
                html_content = response.read().decode('utf-8')
                links = link_exp.findall(html_content)
                for link in links:
                    f.write(link + '\n')
                f.close()
            except urllib.error.HTTPError as e:
                print(e.code)
            break
        return len(links) #temporary behaviour for testing

if __name__ == '__main__':
    print("enter the url to crawl")
    input_url = input()
    bela = Balerian(input_url)
    bela.crawl()