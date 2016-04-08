import tweepy
import requests
import json
import boto3

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.coordinates and status.lang == 'en':
            print status.text
            payload = {}
            payload['username'] = status.user.screen_name
            payload['text'] = status.text
            payload['location'] = status.coordinates['coordinates']
            payload['created_at'] = str(status.created_at)
            response = queue.send_message(MessageBody=json.dumps(payload))
            print(response.get('MessageId'))
            #r = requests.post('http://52.1.34.124:9200/tweetmaps/tweets', json = payload)
            #print r.text
            # Create a new message
            
            # The response is NOT a resource, but gives you a message ID and MD5
            

auth = tweepy.OAuthHandler('16sqGDlBINwZEzYM4c9f3eAi4', 'X8p4wB3jsjZ5sfr77XJNEzjuVFMmAJsGEmQl7xsYizqjX5X9fc')
auth.set_access_token('703609657177317376-JWFD6pff2C3rdULb9zMoSEoMzR0jI5b', '0olnQXZxYMORagTz88B7SwZYnH4oallYJhAuqQoTnTnfb')

api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName='tweets')

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))

while True:
	try:
		myStream.filter(track=["cloud", "snow", "election", "NBA"])
	except:
		continue