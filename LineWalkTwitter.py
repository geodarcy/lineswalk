import twitter
import json
from geojson import Feature, Point, FeatureCollection
import geojson
from dateutil import parser
import platform
import os
import numpy as np

CONSUMER_KEY = '1rOtJNRrQ2UVLU2qmQUg'
CONSUMER_SECRET = 'CSaZDwHeeMc2ZnVvvuEDf60IUkmlzwJRi2jqq3II0w'
OAUTH_TOKEN = '15410243-GVm4aeHbw2UIXRRBSKhqOwklFUNUOheXBBJmFuA6z'
OAUTH_TOKEN_SECRET = 'sIzbJaCdKbwLakuo6potfqCifXrcLCxYoTDlrJmM'
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

if platform.system() == 'Windows':
  path = 'S:/developer/Darcy/github'
elif platform.system() == 'Darwin':
  path = '/Users/Darcy/Documents/github'

print("Base path is {}".format(path))

## collect data as a stream
try:
  featureDict
  print("Already loaded featureDict")
except(NameError):
  print("Haven't loaded featureDict")
  try:
    with open(os.path.join(path, 'lineswalk/featureDict.txt'), 'r') as fd:
      featureDict = json.load(fd)
    print("Read featureDict from file")
  except:
    print("Couldn't read featureDict so making a blank one.")
    featureDict = {}

tweets = twitter_api.statuses.user_timeline(screen_name='lineperron')
for tweet in tweets:
  if tweet['coordinates'] or tweet['place'] is not None:
    try:
      picURL = [tweet['extended_entities']['media'][x]['media_url'] for x in range(len(tweet['extended_entities']['media']))]
    except:
      picURL = None
    if tweet['coordinates']:
      coordinates = tweet['coordinates']['coordinates']
    else:
      xCoord = np.mean(np.array(tweet['place']['bounding_box']['coordinates'][0])[:,0])
      yCoord = np.mean(np.array(tweet['place']['bounding_box']['coordinates'][0])[:,1])
      coordinates = [xCoord, yCoord]
    featureDict[str(tweet['id'])] = Feature(geometry=Point(coordinates), properties={'user': tweet['user']['name'], 'tweet': tweet['text'], 'date': parser.parse(tweet['created_at']).strftime("%a, %d %b %Y at %H:%M"), 'picture': picURL})

badIDs = ['466216835143069697', '466635406876762112', '466641320380227585', '466649563944992768', '466650889672228864', '477524611391696897']
for i in badIDs:
  try:
    del featureDict[i]
  except:
    pass

print("Tweets collected: {}".format(len(featureDict.keys())))

myFeatureCollection = FeatureCollection([x for x in featureDict.values()])
with open(os.path.join(path, 'lineswalk/twitter.json'), 'w') as fp:
  geojson.dump(myFeatureCollection, fp)

with open(os.path.join(path, 'lineswalk/featureDict.txt'), 'w') as fd:
  json.dump(featureDict, fd)