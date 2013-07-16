# -*- coding: utf-8 -*- 

import os, oauth2, time, urllib, urllib2, json
from flask import Flask, url_for, render_template
import pylast

app = Flask(__name__)

@app.route('/')
def main():
	def lastfm():

		API_KEY = "d2e1283a31bd5b2c450f7ed61cf9ab2e" # this is a sample key
		API_SECRET = "39aa505b402710fb60d8176a702f3acf"

		username = "prichey"
		password_hash = pylast.md5("blackbird")

		network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
		    API_SECRET, username = username, password_hash = password_hash)

		me = pylast.User("prichey", network)
		np = me.get_now_playing()
		last = me.get_recent_tracks(limit=2)

		if np:
			status = u"♫ now playing:"
			track = str(np)
			print last[0]
		else:
			status = u"last played:"
			track = str(last[0][0])
		return status, track

	OP_ACCESS = "DBCU5RGLOXVNZXIYPYMLVTCBRE"
	OP_SECRET = "5U76P54YG7482CAE8W5971GPZ949EV6UJT1OXNA9QMF60WN415XJE27MF6BQ2VQ8"
	OP_URL = "https://openpaths.cc/api/1"

	def build_auth_header(url, method):
		params = {
		'oauth_version': "1.0",
		'oauth_nonce': oauth2.generate_nonce(),
		'oauth_timestamp': int(time.time()),
		}
		consumer = oauth2.Consumer(key=OP_ACCESS, secret=OP_SECRET)
		params['oauth_consumer_key'] = consumer.key
		request = oauth2.Request(method=method, url=url, parameters=params)
		signature_method = oauth2.SignatureMethod_HMAC_SHA1()
		request.sign_request(signature_method, consumer, None)
		return request.to_header()

	def get_location():
		now = time.time()
		params = {'num_points': 1}
		query = "%s?%s" % (OP_URL, urllib.urlencode(params))
		try:
			request = urllib2.Request(query)
			request.headers = build_auth_header(OP_URL, 'GET')
			connection = urllib2.urlopen(request)
			data = json.loads(''.join(connection.readlines()))
			return data[0]["lat"], data[0]["lon"]
		except urllib2.HTTPError as e:
			return (e.read())

	try:
		lat, lon = get_location()
		status, track = lastfm()
		return render_template('main.html', lat=lat, lon=lon, status=status, track=track)

	except:
		return render_template('error.html')

@app.route('/recs')
def recs():
	return render_template('recs.html')

if __name__ == "__main__":
    app.run(debug=True)