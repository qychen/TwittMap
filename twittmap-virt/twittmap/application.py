from flask import Flask, render_template, request, Response
import requests
import json

import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.iteritems() if k]
        
        return "%s\n\n" % "\n".join(lines)

application = Flask(__name__)
subscriptions = []

@application.route('/')
def main_page():
    return render_template('index.html') 

@application.route('/search')
def search():
	keyword = request.args.get('keyword')
	
	payload = {"size":1000,'query':{'match_phrase':{'text':keyword}}}
	r = requests.get('http://52.200.219.3:9200/tweetspart2/tweets/_search', json = payload)
	return r.text

@application.route('/surround')
def surround():
	lat = request.args.get('lat')
	lon = request.args.get('long')

	payload = {
	  "query": {
	    "filtered": {
	      "filter": {
	        "geo_distance": {
	          "distance": "200km", 
	          "location": { 
	            "lat": lat,
	            "lon": lon
	          }
	        }
	      }
	    }
	  }
	}
	r = requests.get('http://52.200.219.3:9200/tweetspart2/tweets/_search', json = payload)
	return r.text

@application.route('/sns', methods=['POST'])
def sns():
	message = eval(request.data)
	#print json.loads(eval(request.data))
	r = requests.post('http://52.200.219.3:9200/tweetspart2/tweets', json = json.loads(message))
	print r.text

	def notify():
		msg = message
		for sub in subscriptions[:]:
			sub.put(msg)

	gevent.spawn(notify)
	return ('', 200)

@application.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

if __name__ == '__main__':
	application.debug = True
	server = WSGIServer(("", 5000), application)
	server.serve_forever()




