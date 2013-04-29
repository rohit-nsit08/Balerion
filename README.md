Balerion
========

"because crawlers are awesome"

##Balerion is a very basic crawler that does the following stuff.

1. Take a given input url and fetch all the links on that page into a repository of links.
2. Take a random url from existing repository and repeat step 1 recursively.
3. Stop when all the links have been fetched / previously set limit of max fetch is reached.

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


