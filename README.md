Balerion
========

"because crawlers are awesome"

##Balerion is a very basic crawler that does the following stuff.

1. Take a given input url and fetch all the links using regest match on that page into a repository of links.
2. Take a random url from existing repository and repeat step 1 recursively.
3. Stop when all the links have been fetched / previously set limit of max fetch is reached.

##Working :
    # initiate the crawler and enter the url to crawl
    python crawler.py http://rohitjangid.com 1 
    # test suite [ bug identified. don't run ]
    python test.py
    
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
