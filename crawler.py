import re
import urllib.request
print("enter the seed target")
seed_target = input()
level = 1
MAX_FETCH = 100
link_exp = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
req = urllib.request.Request(seed_target)
while(True):
    try:
        response = urllib.request.urlopen(req)
        f = open('level_'+ str(level), 'w')
        html_content = response.read().decode('utf-8')
        links = link_exp.findall(html_content)
        for link in links:
            f.write(link + '\n')
        f.close()
    except urllib.error.HTTPError as e:
        print(e.code)
    break