import feedparser
import itertools
import requests
import schedule
#import re
import schedule
import time


try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import pandas as pd


# Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
        return feedparser.parse( rss_url ) 

    # Function grabs the rss feed headlines (titles) and returns them as a list
def get( rss_url ):
        all_links=[]
        all_category=[]
        feed = parseRSS( rss_url )
        for newsitem in feed['items']:
            all_links.append(newsitem['link'])
            all_category.append(newsitem['title'])
        return(all_links, all_category)

def fakenewsgenerator():

    all_labels=[]

    # Iterate over the feed urls
    all_links, all_category = get('http://www.fakingnews.com/feed')
    print(all_links)
    content=[]
    for x in all_links:
        r = requests.get(x,verify=False)
        soup = BeautifulSoup(r.content, 'lxml')
        print(x)
        body=[]
        try:
            for i in soup.findAll("div", {"class": "article-content"}):
                if(i.get_text()) not in ['','\xa0']:
                    body.append(i.get_text())

        except:
                continue

        
        body= ''.join(body)
        content.append(body)
        print(body)

    for a in range(len(all_category)):
        all_labels.append("FAKE")


    list_of_tuples = list(zip(all_links, content, all_category, all_labels))  
    df = pd.DataFrame(list_of_tuples, columns=['all_links','text','title','label'])
    df.to_excel("fakenewsgenerator.xlsx",index=False)

    
fakenewsgenerator()