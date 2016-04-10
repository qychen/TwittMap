from flask import Flask, render_template, request
import requests
import json

application = Flask(__name__)

@application.route('/')
def main_page():
    return render_template('index.html') 

@application.route('/search')
def search():
	keyword = request.args.get('keyword')
	
	payload = {"size":1000,'query':{'match_phrase':{'text':keyword}}}
	r = requests.get('http://52.200.219.3:9200/tweetmaps/tweets/_search', json = payload)
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
	r = requests.get('http://52.200.219.3:9200/tweetmaps/tweets/_search', json = payload)
	return r.text

@application.route('/sns', methods=['POST'])
def sns():
	a = eval(request.data)
	req = json.loads(a)
	print req['location']
	print type(req['location'])
	print json.loads(eval(request.data))
	r = requests.post('http://52.200.219.3:9200/tweetspart2/tweets', json = json.loads(eval(request.data)))
	print r.text
	return ('', 200)

if __name__ == '__main__':
	application.debug = True
	application.run()




