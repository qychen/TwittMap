from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html') 

@app.route('/search')
def search():
	keyword = request.args.get('keyword')
	
	payload = {'query':{'match_phrase':{'text':keyword}}}
	r = requests.get('http://localhost:9200/tweetmaps/tweets/_search', json = payload)
	return r.text

@app.route('/surround')
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
	r = requests.get('http://localhost:9200/tweetmaps/tweets/_search', json = payload)
	return r.text

if __name__ == '__main__':
	app.debug = True
	app.run()