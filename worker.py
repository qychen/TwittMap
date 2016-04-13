import json
import boto3
import urllib2
import urllib
import threading
import requests

# Get the service resource
sqs = boto3.resource('sqs')


class workerThread(threading.Thread):
    def __init__(self, message, tobedeleted):  
        threading.Thread.__init__(self)  
        self.message = message
        self.tobedeleted = tobedeleted
        self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put the function here  
        while not self.thread_stop:  
            data = {}
            #data['apikey'] = 'd8d93e94d6a8f768cf2fb1c14cf24c7f3812f121'
            #data['apikey'] = 'a52143eb1c30afba87bd891a49862e698ef72d3f'
            data['apikey'] = '31cee1ecc78de13ca4020d3a45387decf2e3e638'
            data['text'] = self.message
            data['outputMode'] = 'json'
            
            url = 'http://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment'
            post_data = urllib.urlencode(data)
            req = urllib2.urlopen(url, post_data)
            
            content = req.read()
            print content
            
            decode = json.loads(content)
            sentiment = str(decode['docSentiment']['type'])
            print sentiment
            
            Ansdata = json.loads(message.body)
            Ansdata['sentiment'] = sentiment
            
            Ans = json.dumps(Ansdata)
            print Ans
            url = 'http://04da0beb.ngrok.io/sns'
            r = requests.post(url, json = Ans)
            print r.text

            self.thread_stop = True
                                          
    def stop(self):  
        self.thread_stop = True  

# Get the queue
queue = sqs.get_queue_by_name(QueueName='tweets')

while True:
	# Process messages by printing out body and optional author name
    try:
    	message = queue.receive_messages(MessageAttributeNames=['Author'])[0]
    	print message.body
    	messageJson = json.loads(message.body)
    	messageStr = messageJson['text'].encode('unicode_escape')

    	t1 = workerThread(messageStr, message)
    	t1.start()
    	message.delete()
    except:
    	continue



