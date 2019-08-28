#the hindu 
import feedparser
import itertools
import requests
import re
import json
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import pandas as pd


# List of RSS feeds that we will fetch and combine
feeds = {
    ' Home':           'https://www.thehindu.com/feeder/default.rss',
    'News':       'https://www.thehindu.com/news/feeder/default.rss',
    'National':        'https://www.thehindu.com/news/national/feeder/default.rss',
    'International':        'https://www.thehindu.com/news/international/feeder/default.rss',
    'States':        'https://www.thehindu.com/news/states/feeder/default.rss',
    'Andhra Pradesh':        'https://www.thehindu.com/news/national/andhra-pradesh/feeder/default.rss',
    'Karnataka':        'https://www.thehindu.com/news/national/karnataka/feeder/default.rss',
    'Kerala':        'https://www.thehindu.com/news/national/kerala/feeder/default.rss',
    'Tamil Nadu':        'https://www.thehindu.com/news/national/tamil-nadu/feeder/default.rss',
    'Telangana':        'https://www.thehindu.com/news/national/telangana/feeder/default.rss',
    'Other States':        'https://www.thehindu.com/news/national/other-states/feeder/default.rss',
    'Cities':        'https://www.thehindu.com/news/cities/feeder/default.rss',
    'Bengaluru':        'https://www.thehindu.com/news/cities/bangalore/feeder/default.rss',
    'Chennai':        'https://www.thehindu.com/news/cities/chennai/feeder/default.rss',
    'Coimbatore':        'https://www.thehindu.com/news/cities/Coimbatore/feeder/default.rss',
    'Delhi':        'https://www.thehindu.com/news/cities/Delhi/feeder/default.rss',
    'Hyderabad':        'https://www.thehindu.com/news/cities/Hyderabad/feeder/default.rss',
    'Kochi':        'https://www.thehindu.com/news/cities/Kochi/feeder/default.rss',
    'Kolkata':        'https://www.thehindu.com/news/cities/kolkata/feeder/default.rss',
    'Mumbai':        'https://www.thehindu.com/news/cities/mumbai/feeder/default.rss',
    'Kozhikode':        'https://www.thehindu.com/news/cities/kozhikode/feeder/default.rss',
    'Madurai':        'https://www.thehindu.com/news/cities/Madurai/feeder/default.rss',
    'Mangaluru':        'https://www.thehindu.com/news/cities/Mangalore/feeder/default.rss',
    'Puducherry':        'https://www.thehindu.com/news/cities/puducherry/feeder/default.rss',
    'Thiruvananthapuram':        'https://www.thehindu.com/news/cities/Thiruvananthapuram/feeder/default.rss',
    'Tiruchirapalli':        'https://www.thehindu.com/news/cities/Tiruchirapalli/feeder/default.rss',
    'Vijayawada':        'https://www.thehindu.com/news/cities/Vijayawada/feeder/default.rss',
    'Visakhapatnam':        'https://www.thehindu.com/news/cities/Visakhapatnam/feeder/default.rss',
    'Opinion':        'https://www.thehindu.com/opinion/feeder/default.rss',
    'Cartoon':        'https://www.thehindu.com/opinion/cartoon/feeder/default.rss',
    'Columns':        'https://www.thehindu.com/opinion/columns/feeder/default.rss',
    'Editorial':        'https://www.thehindu.com/opinion/editorial/feeder/default.rss',
    'Interview':        'https://www.thehindu.com/opinion/interview/feeder/default.rss',
    'Lead':        'https://www.thehindu.com/opinion/lead/feeder/default.rss',
    'Readers Editor':        'https://www.thehindu.com/opinion/Readers-Editor/feeder/default.rss',
    'Comment':        'https://www.thehindu.com/opinion/op-ed/feeder/default.rss',
    'Open Page':        'https://www.thehindu.com/opinion/open-page/feeder/default.rss',
    'Letters':        'https://www.thehindu.com/opinion/letters/feeder/default.rss',
    'Business':        'https://www.thehindu.com/business/feeder/default.rss',
    'Agri-Business':        'https://www.thehindu.com/business/agri-business/feeder/default.rss',
    'Industry':        'https://www.thehindu.com/business/Industry/feeder/default.rss',
    'Economy':        'https://www.thehindu.com/business/Economy/feeder/default.rss',
    'Budget':        'https://www.thehindu.com/business/budget/feeder/default.rss',
    'Sport':        'https://www.thehindu.com/sport/feeder/default.rss',
    'Cricket':        'https://www.thehindu.com/sport/cricket/feeder/default.rss',
    'Football':        'https://www.thehindu.com/sport/football/feeder/default.rss',
    'Hockey':        'https://www.thehindu.com/sport/hockey/feeder/default.rss',
    'Tennis':        'https://www.thehindu.com/sport/tennis/feeder/default.rss',
    'Athletics':        'https://www.thehindu.com/sport/athletics/feeder/default.rss',
    'Motorsport':        'https://www.thehindu.com/sport/motorsport/feeder/default.rss',
    'Races':        'https://www.thehindu.com/sport/races/feeder/default.rss',
    'Other Sports':        'https://www.thehindu.com/sport/other-sports/feeder/default.rss',
    'Cricket':        'https://www.thehindu.com/sport/cricket/feeder/default.rss',
    'Crossword':        'https://www.thehindu.com/crossword/feeder/default.rss',
    'Entertainment':        'https://www.thehindu.com/entertainment/feeder/default.rss',
    'Art':        'https://www.thehindu.com/entertainment/art/feeder/default.rss',
    'Dance':        'https://www.thehindu.com/entertainment/dance/feeder/default.rss',
    'Movies':        'https://www.thehindu.com/entertainment/movies/feeder/default.rss',
    'Music':        'https://www.thehindu.com/entertainment/music/feeder/default.rss',
    'Reviews':        'https://www.thehindu.com/entertainment/reviews/feeder/default.rss',
    'Theatre':        'https://www.thehindu.com/entertainment/theatre/feeder/default.rss',
    'Life & Style':        'https://www.thehindu.com/life-and-style/feeder/default.rss',
    'Fashion':        'https://www.thehindu.com/life-and-style/fashion/feeder/default.rss',
    'Fitness':        'https://www.thehindu.com/life-and-style/fitness/feeder/default.rss',
    'Food':        'https://www.thehindu.com/life-and-style/food/feeder/default.rss',
    'Motoring':        'https://www.thehindu.com/life-and-style/motoring/feeder/default.rss',
    'Travel':        'https://www.thehindu.com/life-and-style/travel/feeder/default.rss',
    'Homes and gardens':        'https://www.thehindu.com/life-and-style/homes-and-gardens/feeder/default.rss',
    'Luxury':        'https://www.thehindu.com/life-and-style/luxury/feeder/default.rss',
    'thREAD':        'https://www.thehindu.com/thread/feeder/default.rss',
    
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
        all_category.append(newsitem['category'])


# Iterate over the feed urls
for key,url in feeds.items():
    get( url )
    
for a in range(len(all_category)):
    all_labels.append("REAL")


content=[]
for x in all_links:
    r = requests.get(x)
    soup = BeautifulSoup(r.content, 'lxml')
    print(x)
    body=[]
    try:
        for i in soup.select_one('[id^=content-body]').get_text().split('\n'):
            if i not in ['','\xa0']:
                body.append(i)
    except:
                continue
    body= ''.join(body)
    content.append(body)

   
list_of_tuples = list(zip(content, all_category, all_labels))  
                
df = pd.DataFrame(list_of_tuples, columns=['text','category','label'])
df.to_excel("thehindu1.xlsx",index=False)
