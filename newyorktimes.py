"""
Author : Vishak Raj
E-mail ID : vishak.shanmu@gmail.com

Gives and save the news from the nytimes news paper
And nytimes have limitaiton, to get full access contact the nytimes 
"""

import json
import requests

# Refer the doc - https://developer.nytimes.com/docs/articlesearch-product/1/routes/articlesearch.json/get

def nyt():
    API_ARTICLE_KEY = "" #create your api from - https://developer.nytimes.com/get-started
    API_ENDPOINT = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
    # add or delete parameter here, for more parameters refer https://developer.nytimes.com/docs/articlesearch-product/1/overview
    my_params = {
        'q':"",
        'begin_date': "",
        'end_date': "",
        'sort':"newest",
        'api-key': API_ARTICLE_KEY,

    }
    my_params['begin_date'] = "2014-01-01"
    my_params['end_date'] = "2019-08-12"
    my_params['q'] = "football"
    my_params['sort'] = "relevance"

    resp = requests.get(API_ENDPOINT, my_params) # call is made for the set of parameters
    print(resp.url)
    data=resp.json()
    current_page = 1
    total_pages = 200 # As default from the documentation, total page does not exceed 200 

    while current_page <= total_pages:
                print("...page", current_page)
                my_params['page'] = current_page
                resp = requests.get(API_ENDPOINT, my_params) # call is made for the set of parameters
                print(resp.url)
                data = resp.json()
                print(data)
                print("\n")
                current_page += 1
                # access data by calling the "data" variable as list. Like data["status"] which prints status of the call


# schedule the api at specified time
schedule.every().day.at("17:21").do(nyt) 

while True:
    schedule.run_pending()
    time.sleep(1) 

                



                
