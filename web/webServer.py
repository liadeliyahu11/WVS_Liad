from flask import Flask,jsonify,abort,render_template,current_app,request,redirect,url_for
import json
import hashlib
import os
from scan.dbWrapper import *

app = Flask(__name__)
temps = {}
db = dbWrapper()


def message(msg):
	return redirect(url_for('send_message', message=msg))

def get_link_by_hash(hash_str):
	global temps
	for key in temps.keys():
		if key == hash_str:
			return temps[hash_str]
	return None

@app.route('/')
def get_index():
	return current_app.send_static_file('index.html')

@app.route('/message')
def send_message():
	message = ''
	if request.args.get('message'):
		message = request.args['message']
	return render_template('message.html',message=message)

@app.route('/scans',methods=['GET'])
def get_scans():
	return "error"

@app.route('/checkDetails',methods=['POST'])
def check_details():
	global temps
	hash_str = request.form['key'].lower()
	link = get_link_by_hash(hash_str)
	if not link:
		for k in temps.keys():
			if k == hash_str:
				link = temps[k]
				break
	if link:
		try:
			os.system("python scan\main.py -u "+link+' -s '+hash_str)
			#runScan(link,hash_str)#needed to run command not from here
			return redirect('/results/'+hash_str)
		except Exception as ex:
			print ex
			results = "error"
			pass
		return results
	return message("this key not exist in the known keys")#

@app.route('/results/<string:hash_str>',methods=['GET'])
def get_results(hash_str):
	return render_template('result.html',hash_str=hash_str)

@app.route('/generateKey',methods=['POST'])
def generate_key():
	global temps
	domain = request.form['domain']
	hash_str = hashlib.sha256(domain).hexdigest()
	if not get_link_by_hash(hash_str):
		temps[hash_str] = domain
		return  message("your hash is :\n" + hash_str)
	return message("this hash was already exist\n" + hash_str)


@app.route('/scans/<string:hash_str>',methods=['GET'])
def get_scan(hash_str):
	scan = db.get_scan_by_hash(hash_str.lower())	
	if not scan:
		abort(404)
	else:
		scan['_id'] = str(scan['_id'])
		return jsonify(scan)
if __name__ == "__main__":
	app.run(debug=True)