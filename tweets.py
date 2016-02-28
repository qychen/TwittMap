import tweepy

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.coordinates:
        	print status.user.screen_name, status.text, status.coordinates, status.created_at

auth = tweepy.OAuthHandler('15nFWBgQPCshWsmOGP29Fk2gb', '9c7UQNGf4T1H9jOIO7JJvSKWhiqPK6D17sFfjbbARK0gncHk6h')
auth.set_access_token('703609657177317376-JWFD6pff2C3rdULb9zMoSEoMzR0jI5b', '0olnQXZxYMORagTz88B7SwZYnH4oallYJhAuqQoTnTnfb')

api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.sample()