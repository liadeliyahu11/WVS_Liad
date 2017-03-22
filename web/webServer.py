from flask import Flask, jsonify, abort, render_template, current_app, request, redirect, url_for
import json
import hashlib
from scan.dbWrapper import *
import subprocess

app = Flask(__name__)
db = dbWrapper()


def message(msg):
	"""
	gets message and redirect to send_message function pass the message as argument.
	"""
	return redirect(url_for('send_message', message = msg))


@app.route('/')
def get_index():
	"""
	returns the index page.
	"""
	return current_app.send_static_file('index.html')


@app.route('/message')
def send_message():
	"""
	gets message as argument and render page for the user with the given message.
	"""
	message = ''
	if request.args.get('message'):
		message = request.args['message']

	return render_template('message.html', message=message)



@app.route('/scanDomain', methods=['POST'])
def check_details():
	"""
	scan a given domain (the domain is form parameter).
	"""

	link = request.form['domain']
	hash_str = hashlib.sha256(link).hexdigest().lower()
	if link:
		try:
			db.remove_if_exist(hash_str)
			subprocess.Popen("python scan\main.py -c cookies.txt -u " + link + ' -s ' + hash_str)
			return redirect('/results/' + hash_str)
		
		except Exception as ex:
			print ex
			results = "error"
			pass
		return results

@app.route('/results/<string:hash_str>', methods=['GET'])
def get_results(hash_str):
	"""
	gets hash string and returns rendered page with the hash string associated results(html with realtime update).
	"""
	return render_template('result.html', hash_str = hash_str)


@app.route('/scans/<string:hash_str>', methods = ['GET'])
def get_scan(hash_str):
	"""
	gets hash string and returns json version of the hash string associated scan.
	"""
	scan = db.get_scan_by_hash(hash_str.lower())
	if not scan:
		abort(404)
	else:
		scan['_id'] = str(scan['_id'])
		return jsonify(scan)

if __name__ == "__main__":
	app.run(host = '0.0.0.0', debug = True,)
