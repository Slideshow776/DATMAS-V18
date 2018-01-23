"""
    Bruker twitter sitt REST-API for å søke etter nøkkelord.
    Nye tweets blir lagt til på slutten av output filen.

    search_terms.txt:   Sett av nøkkelord du vil søke på, skriv nytt ord på ny linje
    keys.txt:           Sett av twitterkonto api keys, i rekkefølge på ny linje: ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET
    twitter_data:       tweets funnet, format: id, dato, lokasjon, tweet, ----------------------------------------------------------------------------

    @author Sandra Moen
"""

from twitter import Twitter, OAuth

# Loading keys from hidden textfile, in order to protect my keys from misuse
FILE = open("keys.txt", "r")
KEYS = FILE.readlines()

# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = KEYS[0].strip()
ACCESS_SECRET = KEYS[1].strip()
CONSUMER_KEY = KEYS[2].strip()
CONSUMER_SECRET = KEYS[3].strip()

OAUTH = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter REST API
TWITTER = Twitter(auth=OAUTH)

# Load the search terms
FILE.close()
FILE = open("search_terms.txt")
SEARCH_TERMS = FILE.readlines()

FILE = open("twitter_data.txt", "r+", encoding='utf-8')

def get_all_ids_in_file():
    file_data = FILE.readlines()
    FILE.seek(0)
    ids_in_file = []
    temp = []
    if file_data:
        for i in range(0, len(file_data)-1):
            if file_data[i] == '----------------------------------------------------------------------------\n':
                ids_in_file.append(file_data[i+1])
            elif i == 0:
                ids_in_file.append(file_data[i])
        temp = []
        for dates in ids_in_file:
            temp.append(dates.strip('\n'))
    return temp

def get_all_texts_in_file(): # gets the first line of all texts in file
    file_text = FILE.readlines()
    FILE.seek(0)
    ids_in_file = []
    temp = []
    if file_text:
        for i in range(0, len(file_text)):
            if file_text[i] == '----------------------------------------------------------------------------\n':
                ids_in_file.append(file_text[i-1])
        temp = []
        for dates in ids_in_file:
            temp.append(dates.strip('\n'))
    return temp

def convert_date(date):
    temp = date.split()
    year = temp[-1] + "-" #latest_date[-4:] + "-"
    month = temp[1]
    if month == "Jan":
        month = "01"
    elif month == "Feb":
        month = "02"
    elif month == "Mar":
        month = "03"
    elif month == "Apr":
        month = "04"
    elif month == "May":
        month = "05"
    elif month == "Jun":
        month = "06"
    elif month == "Jul":
        month = "07"
    elif month == "Aug":
        month = "08"
    elif month == "Sep":
        month = "09"
    elif month == "Oct":
        month = "10"
    elif month == "Nov":
        month = "11"
    elif month == "Des":
        month = "12"
    day = "-" + temp[2]
    if len(day) == 1:
        day = "0" + day
    return year + month + day

texts_in_file = get_all_texts_in_file()
ids_in_file = get_all_ids_in_file()

# Search tweets
tweet_count, i = 0, 0
latest_date = ""
while i < len(SEARCH_TERMS):
    if tweet_count == 100:
        tweet_count = 0
        i = i-1
        twitter_search = TWITTER.search.tweets(
            q=SEARCH_TERMS[i].strip('\n'),
            tweet_mode='extended',
            lang='no',
            count=100,
            until=latest_date
            )
    else:        
        print("Searching on term: ", SEARCH_TERMS[i], end="")
        twitter_search = TWITTER.search.tweets(
            q=SEARCH_TERMS[i].strip('\n'),
            tweet_mode='extended',
            lang='no',
            count=100
            )
    i = i+1

    #print(twitter_search.get('statuses'))
    for result in twitter_search.get('statuses'):
        tweet_count += 1
        ids = result.get('id_str')
        created_at = result.get('created_at')
        location = result.get('user').get('location')
        text = result.get('full_text')

        if not ids in ids_in_file:
            if not text in texts_in_file: # ignore duplicate tweets in search and file
                FILE.write(ids + '\n')
                FILE.write(created_at + '\n')
                if location:
                    FILE.write(location + '\n')
                else:
                    FILE.write('None\n')

                FILE.write(text)
                FILE.write("\n----------------------------------------------------------------------------\n")
        latest_date = convert_date(created_at)

#print("\n", twitter_search)
FILE.close()
