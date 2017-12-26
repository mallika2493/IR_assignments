#Task2-B
#Focused crawling implementing DFS traversal
import urllib
import re
import time
from bs4 import BeautifulSoup

#maintain the set of urls visited
visited_url = set()
#The specified number of urls to crawl
NO_URLS_TO_CRAWL = 1000;
#max depth the crawler should reach
DEPTH_SIZE=5
SEED_URL = "https://en.wikipedia.org/wiki/Sustainable_energy"
PREFIX = "https://en.wikipedia.org"
FILENAME="Task2-B.txt"
KEYWORD="solar"

#recursively calls dfs function to perform Depth First Traversal
def dfs(url,depth):
    if depth==DEPTH_SIZE or len(visited_url)==NO_URLS_TO_CRAWL:
        return
    else:
        #fetchs the urls which start with "/wiki" and contain solar in the content
        all_links=fetch_urls_with_beautiful_soup(url)
        #Iterates all the links (with its depth incremented from its parent) from its parent url
        for every_link in all_links:
                    link = filter_url_with_keyword(every_link['href'])
                    if link is not None and link not in visited_url:
                            #marks the link visited
                            visited_url.add(link)
                            #print str(len(visited_url)+1)+"|"+str(depth+1)+"|"+str(link)
                            #recursive call to dfs with link and depth+1
                            dfs(link,depth+1)

#fetches all links using beautiful soup
def fetch_urls_with_beautiful_soup(url):
    start = time.time()
    time.sleep(1)
    page = urllib.urlopen(url)
    #difference = time.time() - start
    #time.sleep(float(1000 - difference) / 1000)
    page_source = page.read()
    # store_page(seed_url, page_source)
    soup = BeautifulSoup(page_source)
    url1 = soup.find("div", {"id": "bodyContent"}).findAll('a',href=re.compile('/wiki/', re.IGNORECASE))
    url2 = soup.find("div", {"id": "bodyContent"}).findAll('a',href=re.compile('/wiki/', re.IGNORECASE),
                                                               text=re.compile('solar', re.IGNORECASE))
    url = url1+url2
    return url

#filers the url with keyword, ':' and "#" and returns the complete link with prefix added
def filter_url_with_keyword(url):
    if KEYWORD in str(url).lower() and ":" not in url:
            every_url = str(url).split("#")[0]
            link = PREFIX + every_url
            return link
    else: return None

def get_file_name(url):
    return url.split("/")[-1]

def store_page(url, source):
    fil = open(get_file_name(url), "w")
    fil.write(source)
    fil.close()

visited_url.add(SEED_URL)
dfs(SEED_URL,1)


# Print list of visited pages
fil = open(FILENAME, "w")
for i in visited_url:
        print i
        fil.write(i+"\n")
fil.close()
