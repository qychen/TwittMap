import json
import boto3
import urllib2
import urllib
import threading

#API KEY: d8d93e94d6a8f768cf2fb1c14cf24c7f3812f121

# Get the service resource
sqs = boto3.resource('sqs')


class workerThread(threading.Thread):
    def __init__(self, message):  
        threading.Thread.__init__(self)  
        self.message = message  
        self.thread_stop = False  
   
    def run(self): #Overwrite run() method, put the function here  
        while not self.thread_stop:  
            data = {}
            data['apikey'] = 'd8d93e94d6a8f768cf2fb1c14cf24c7f3812f121'
            data['text'] = self.message.body
            data['outputMode'] = 'json'
            
            url = 'http://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment'
            post_data = urllib.urlencode(data)
             
            req = urllib2.urlopen(url, post_data)
            
            content = req.read()
            print content
            
            decode = json.loads(content)
            sentiment = str(decode['docSentiment']['type'])
            print sentiment
            
            
            #encode
            Ansdata = {}
            Ansdata['message'] = message.body
            Ansdata['sentiment'] = sentiment
            
            Ans = json.dumps(Ansdata)
            url = 'http://a3a175ba.ngrok.io/sns'
            post_data = urllib.urlencode(Ans)
            
            req = urllib2.urlopen(url, post_data)
            
            self.thread_stop = True
                                          
    def stop(self):  
        self.thread_stop = True  


# Get the queue
queue = sqs.get_queue_by_name(QueueName='tweets')

while True:
# Process messages by printing out body and optional author name
    message = queue.receive_messages()
    print message.body
    
    t1 = workerThread(message.body)
    t1.start()
    
    message.delete()