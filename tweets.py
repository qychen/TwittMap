import tweepy
import requests
import json

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.coordinates:
        	#print status.coordinates['coordinates']
        	payload = {}
        	payload['username'] = status.user.screen_name
        	payload['text'] = status.text 
        	payload['location'] = status.coordinates['coordinates']
        	payload['created_at'] = str(status.created_at)
        	r = requests.post('http://localhost:9200/tweetmaps/tweets', json = payload)
        	#print r.text

auth = tweepy.OAuthHandler('15nFWBgQPCshWsmOGP29Fk2gb', '9c7UQNGf4T1H9jOIO7JJvSKWhiqPK6D17sFfjbbARK0gncHk6h')
auth.set_access_token('703609657177317376-JWFD6pff2C3rdULb9zMoSEoMzR0jI5b', '0olnQXZxYMORagTz88B7SwZYnH4oallYJhAuqQoTnTnfb')

api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

while True:
	try:
		myStream.filter(locations=[-170.0,-80.0,170.0,80.0])
	except:
		continue