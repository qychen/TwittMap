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
	
	payload = {'query':{'match_phrase':{'text':keyword}}}
	r = requests.get('http://52.1.34.124:9200/tweetmaps/tweets/_search', json = payload)
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
	r = requests.get('http://52.1.34.124:9200/tweetmaps/tweets/_search', json = payload)
	return r.text

if __name__ == '__main__':
	application.debug = True
	application.run()