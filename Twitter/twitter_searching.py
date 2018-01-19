# coding=utf8
# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Loading keys from hidden textfile, in order to protect my keys from misuse
file = open("keys.txt", "r") 
keys = file.readlines()

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = keys[0].strip()
ACCESS_SECRET = keys[1].strip()
CONSUMER_KEY = keys[2].strip()
CONSUMER_SECRET = keys[3].strip()

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)

file.close()
file = open("search_terms.txt")
search_terms = file.readlines()

# Search tweets
for term in search_terms:
    print("Searching on term: ", term)
    twitter_search = twitter.search.tweets(q=term.strip('\n'), lang='no', until='2018-01-10', count=100)

    # post-process results: [date, tweet]
    temp_text = ''
    for result in twitter_search.get('statuses'):
        if temp_text == result.get('text'): # remove duplicate tweets
            continue
        temp_text = result.get('text')

        print(result.get('created_at'))
        if len(result.get('user').get('location')) > 0:
            print(result.get('user').get('location'))
        else:
            print('None')
        
        print(result.get('text'))
        print("----------------------------------------------------------------------------\n")

#print("\n", twitter_search)
file.close()