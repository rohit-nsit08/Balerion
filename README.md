Balerion
========

"because crawlers are awesome"

##Balerion is a very basic crawler that does the following stuff.

1. Take a given input url and fetch all the links using regest match on that page into a repository of links.
2. Take a random url from existing repository and repeat step 1 recursively.
3. Stop when all the links have been fetched / previously set limit of max fetch is reached.

##Working :
    # python crawler.py [root-url] [external-allowed] [redirect allowed] [max-limit]
    # 1 => allowed | 0 => not allowed
    python http://rohitjangid.com 1 1 100
    # test suite
    python test.py
    

Basic algorithm:

1. take input seed url
2. if seed url is valid .. push it into the queue with 0 priority. proceed 
3. while queue is not empty or max-limit not reached. pop next-url
3.a read the page and extract the http-links  
3.b normalize them and store in a priority queue which maintaines unique links only using help of hashtable.   internal links given priority 1. external given 2  
3.c repeat  

##pylint score
10/10 for crawler.py  


###credits: 
* [blog.mischel.com](http://blog.mischel.com/2011/12/26/writing-a-web-crawler-queue-management-part-1/) 
* [theanti9-pycrawler](https://github.com/theanti9/PyCrawler)
* [wrttnwrd-cmcrawler](https://github.com/wrttnwrd/cmcrawler)
* [block8437-python-spyder](https://github.com/block8437/python-spyder)
* [oocities](http://www.oocities.org/foranuj/Ai/chrisdoc/swarch.htm)
* [bbrodriges-pholcidae](https://github.com/bbrodriges/pholcidae/)     



the making
----------------------------- 
## Identifying links in page content

###Day 1: 
1. Using urllib module to open any http link.
2. Read the response and convert into utf-8 string to allow regex search. 
3. Store found links into file. 

todos for tomorrow:
####fix errors:
1. Only accept links of the form 'http://rohitjangid.com' and not 'rohitjangid.com'
2. Store non-http links found on the website with base url prefix.

#### additions:
1. A very basic test suite.

####things to study:
1. Scrapy architecture and if using using xpath is required or not. 
2. A better way to deal with encodings.

### Day 2

major update

1. maintain a queue of ramaining links to be processes. 
2. use hashtable to keep track of old links and only add links to queue iff they are new. 
3. used beautifulsoup for html processing. 
4. filters added for checking content-type and http-header scheme. 
5. downgraded python version to 2.7.4

###next:
1. robots.txt check
2. switch for internal and external links.
3. explore multiple connections or parallel links to improve performance

### Day 3 
1. logging support added. [ yawning ... ] 

### Day 4 . lots of reading and lot to be documented
trying to solve url uniqueness problem : seems to be the most important issue for a crawler. 

standard url format : scheme://netloc/path;parameters?query#fragment.

possible strategy : url normalization followed by priorities . urls in same domain should be traversed earlier than external ones. 

### Day5. 
normalization and using priority queue allowed features of internal links only . and minimization of infinite loop situation.

### Day 6, 7 
laptop out of reach. :-/ couldn't do anything. 


