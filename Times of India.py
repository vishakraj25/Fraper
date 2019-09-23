import feedparser
import itertools
import requests
import schedule
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import pandas as pd

feeds = {
    'Home':"https://timesofindia.indiatimes.com/rss.cms",
    'Top stories':"https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    'Most Recent Stroies':"https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    'India':"https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
    'NRI':"https://timesofindia.indiatimes.com/rssfeeds/296589292.cms",
    'Business':"https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
    'Cricket':"https://timesofindia.indiatimes.com/rssfeeds/4719161.cms",
    'Sports':"https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
    'Health':"https://timesofindia.indiatimes.com/rssfeeds/3908999.cms",
    'Science':"https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms",
    'Environment':"https://timesofindia.indiatimes.com/rssfeeds/2647163.cms",
    'Tech':"https://timesofindia.indiatimes.com/rssfeeds/5880659.cms",
    'Education':"https://timesofindia.indiatimes.com/rssfeeds/913168846.cms",
    'Mumbai':"https://timesofindia.indiatimes.com/rssfeeds/-2128838597.cms",
    'Delhi':"https://timesofindia.indiatimes.com/rssfeeds/-2128839596.cms",		
    'Bangalore':"https://timesofindia.indiatimes.com/rssfeeds/-2128833038.cms",		
    'Hyderabad':"https://timesofindia.indiatimes.com/rssfeeds/-2128816011.cms",
    'Chennai':"https://timesofindia.indiatimes.com/rssfeeds/2950623.cms",
    'Ahemdabad':"https://timesofindia.indiatimes.com/rssfeeds/-2128821153.cms",
    'Allahabad':"https://timesofindia.indiatimes.com/rssfeeds/3947060.cms",
    'Bhubaneswar':"https://timesofindia.indiatimes.com/rssfeeds/4118235.cms",
    'Coimbatore':"https://timesofindia.indiatimes.com/rssfeeds/7503091.cms",
    'Gurgaon':"https://timesofindia.indiatimes.com/rssfeeds/6547154.cms",
    'Guwahati':"https://timesofindia.indiatimes.com/rssfeeds/4118215.cms",
    'Hubli':"https://timesofindia.indiatimes.com/rssfeeds/3942695.cms",
    'Kanpur':"https://timesofindia.indiatimes.com/rssfeeds/3947067.cms",
    'Kolkata':"https://timesofindia.indiatimes.com/rssfeeds/-2128830821.cms",
    'Ludhiana':"https://timesofindia.indiatimes.com/rssfeeds/3947051.cms",
    'Mangalore':"https://timesofindia.indiatimes.com/rssfeeds/3942690.cms",
    'Mysore':"https://timesofindia.indiatimes.com/rssfeeds/3942693.cms",
    'Noida':"https://timesofindia.indiatimes.com/rssfeeds/8021716.cms",
    'Pune':"https://timesofindia.indiatimes.com/rssfeeds/-2128821991.cms",
    'Goa':"https://timesofindia.indiatimes.com/rssfeeds/3012535.cms",
    'Chandigarh':"https://timesofindia.indiatimes.com/rssfeeds/-2128816762.cms"	,
    'Lucknow':"https://timesofindia.indiatimes.com/rssfeeds/-2128819658.cms",
    'Patna':"https://timesofindia.indiatimes.com/rssfeeds/-2128817995.cms",
    'Jaipur':"https://timesofindia.indiatimes.com/rssfeeds/3012544.cms",
    'Nagpur':"https://timesofindia.indiatimes.com/rssfeeds/442002.cms",
    'Rajkot':"https://timesofindia.indiatimes.com/rssfeeds/3942663.cms",
    'Ranchi':"https://timesofindia.indiatimes.com/rssfeeds/4118245.cms",
    'Surat':"https://timesofindia.indiatimes.com/rssfeeds/3942660.cms",
    'Vadodara':"https://timesofindia.indiatimes.com/rssfeeds/3942666.cms",
    'Varanasi':"https://timesofindia.indiatimes.com/rssfeeds/3947071.cms",
    'Thane':"https://timesofindia.indiatimes.com/rssfeeds/3831863.cms",
    'Thiruvananthapuram':"https://timesofindia.indiatimes.com/rssfeeds/878156304.cms",
    'US':"https://timesofindia.indiatimes.com/rssfeeds/30359486.cms",
    'NRI':"https://timesofindia.indiatimes.com/rssfeeds/7098551.cms",
    'Pakistan':"https://timesofindia.indiatimes.com/rssfeeds/30359534.cms",
    'South Asia':"https://timesofindia.indiatimes.com/rssfeeds/3907412.cms",
    'UK':"https://timesofindia.indiatimes.com/rssfeeds/2177298.cms",
    'Europe':"https://timesofindia.indiatimes.com/rssfeeds/1898274.cms",
    'China':"https://timesofindia.indiatimes.com/rssfeeds/1898184.cms",
    'Middle East':"https://timesofindia.indiatimes.com/rssfeeds/1898272.cms",
    'Rest of World':"https://timesofindia.indiatimes.com/rssfeeds/671314.cms",
}

all_links=[]
all_category=[]
all_labels=[]

# Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 
    
# Function grabs the rss feed headlines (titles) and returns them as a list
def get( rss_url ):
    global all_links 
    global all_category
    feed = parseRSS( rss_url )
    for newsitem in feed['items']:
        all_links.append(newsitem['link'])
        all_category.append(newsitem['title'])


# Iterate over the feed urls
 
for key,url in feeds.items():
    get(url)
for a in range(len(all_category)):
    all_labels.append("REAL")


content=[]
for x in all_links:
    r = requests.get(x,verify=False) # Some of website does not have the certificate
    soup = BeautifulSoup(r.content, 'lxml')
    print(x)
    body=[]
    try:
        for i in soup.findAll("div", {"class": "_3WlLe clearfix  "}):
            if(i.get_text()) not in ['','\xa0']:
                body.append(i.get_text())

    except:
            continue
    
    if(len(body)) == 0:
        try:
            for i in soup.findAll("div", {"class": "Normal"}):
                if(i.get_text()) not in ['','\xa0']:
                    body.append(i.get_text())
        except:
            continue
                    
    body= ''.join(body)
    content.append(body)

list_of_tuples = list(zip(all_links, content, all_category, all_labels))  
                
df = pd.DataFrame(list_of_tuples, columns=['all_links','text','title','label'])
df.to_excel("times of india.xlsx",index=False)
