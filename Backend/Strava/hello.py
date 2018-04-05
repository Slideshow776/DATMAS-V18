import requests

API_BASE_URL = 'https://www.strava.com/api/v3/'
MY_ATHLETE_NUMBER = '27861418' # TODO: delete this

# Loading keys from hidden textfile, in order to protect my keys from misuse
FILE = open("keys.txt", "r")
KEYS = FILE.readlines()
CLIENT_SECRET = KEYS[0].strip()
ACCESS_TOKEN = KEYS[1].strip()

EXTRA_HEADERS = {'Authorization' : 'Bearer %s' % ACCESS_TOKEN}

# requesting a single athlete
print('Single athlete:')
reply = requests.get(API_BASE_URL + 'athletes/' + MY_ATHLETE_NUMBER + '?access_token=' + ACCESS_TOKEN)
print(reply.status_code)
print(reply.headers['content-type'])
print(reply.encoding)
#print(reply.text)
print(reply.json())
print()

# requesting segment exploration
print('Segment exploration:')
reply2 = requests.get(API_BASE_URL + 'segments/explore?bounds=[58.949903, 5.697621, 58.975345, 5.745511]' + '"Authorization: Bearer [[' + ACCESS_TOKEN + ']]')
print(reply2.status_code)
print(reply2.headers['content-type'])
print(reply2.encoding)
#print(reply.text)
print(reply2.json())
print()