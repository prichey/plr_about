import os, oauth2, time, urllib, urllib2, json
from flask import Flask, url_for, render_template

app = Flask(__name__)

OP_ACCESS = "DBCU5RGLOXVNZXIYPYMLVTCBRE"
OP_SECRET = "5U76P54YG7482CAE8W5971GPZ949EV6UJT1OXNA9QMF60WN415XJE27MF6BQ2VQ8"
OP_URL = "https://openpaths.cc/api/1"

@app.route('/')
def hello():
	lat, lon = get_location()
	#print location
	return render_template('plr_about.html', lat=lat, lon=lon)

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