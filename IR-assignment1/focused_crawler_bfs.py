#Task2-A
#Focused crawling implementing BFS traversal
import urllib
import re
import time
from collections import deque
from bs4 import BeautifulSoup

#Queue to implement BFS traversal
frontier = deque([])
#maintain the set of urls visited
visited_url = set()
#maintains the same url set as that of frontier to ensure duplicate links are not added.
urls_from_frontier=set()
#The specified number of urls to crawl
NO_URLS_TO_CRAWL = 1000;
DEPTH_SIZE=5
SEED_URL = "https://en.wikipedia.org/wiki/Sustainable_energy"
PREFIX = "https://en.wikipedia.org"
FILENAME="Task2-A.txt"
KEYWORD="solar"

#UrlInfo Class stores url info: url and depth
class UrlInfo(object):
    url = 0
    depth = 0

    def __init__(self,url,depth):
        self.url=url
        self.depth=depth

def make_UrlInfo(url,depth):
    url_info = UrlInfo(url,depth)
    return url_info

#extracts all links which are in the given url web page
#The images and administrative pages are scraped
def extract_links(next_url):
    depth=next_url.depth+1
    page = urllib.urlopen(next_url.url)
    #time.sleep(1)
    if len(visited_url) + len(frontier) < NO_URLS_TO_CRAWL and depth<DEPTH_SIZE:
        page_source = page.read()
        #store_page(seed_url, page_source)
        soup = BeautifulSoup(page_source)
        urls=fetch_urls_with_beautiful_soup(next_url.url)
        for url in urls:
            if len(visited_url) + len(frontier) < NO_URLS_TO_CRAWL:
                if filter_url_with_keyword(url['href']) is not None:
                    link = filter_url_with_keyword(url['href'])
                    if link not in urls_from_frontier and link not in visited_url and link is not None:
                        add_to_frontier(link,depth)

def fetch_urls_with_beautiful_soup(url):
    time.sleep(1)
    page = urllib.urlopen(url)
    page_source = page.read()
    #store_page(seed_url, page_source)
    soup = BeautifulSoup(page_source)
    url1 = soup.find("div", {"id": "bodyContent"}).findAll('a',href=re.compile('/wiki/', re.IGNORECASE))
    url2 = soup.find("div", {"id": "bodyContent"}).findAll('a',href=re.compile('/wiki/', re.IGNORECASE),
                                                               text=re.compile(KEYWORD, re.IGNORECASE))
    url = url1+url2
    return url

def filter_url_with_keyword(url):
    if KEYWORD in str(url).lower() and ":" not in url:
            every_url = str(url).split("#")[0]
            link = PREFIX + every_url
            return link

def add_to_frontier(link,depth):
    frontier.append(make_UrlInfo(link,depth))
    urls_from_frontier.add(link)

def get_file_name(url):
    return url.split("/")[-1]

def store_page(url, source):
    fil = open(get_file_name(url), "w")
    fil.write(source)
    fil.close()

#function to crawl which appends urls to visited_url_list[]
def focus_crawl(url):
    visited_url.add(url.url)
    if len(visited_url) >= NO_URLS_TO_CRAWL:
        return
    #extracts the links within given url
    extract_links(url)

#Recursively calls crawl function to crawl the next url from the frontier
def crawl_links_from_frontier():
    while len(visited_url) < NO_URLS_TO_CRAWL and frontier:
        next_url = frontier.popleft()
        urls_from_frontier.remove(next_url.url)
        #print str(len(visited_url)+1)+"|"+str(next_url.depth)+"|"+str(next_url.url)
        start = time.time()
        focus_crawl(next_url)
        difference = time.time() - start
        time.sleep(float(1000 - difference) / 1000)


frontier.append(make_UrlInfo(SEED_URL, 1))
urls_from_frontier.add(SEED_URL)
visited_url.add(SEED_URL)
crawl_links_from_frontier()

# Print list of visited pages

fil = open(FILENAME, "w")
for i in visited_url:
        fil.write(i+"\n")
fil.close()
