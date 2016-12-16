from flask import Flask,jsonify,abort
import json
app = Flask(__name__)
users = []
with open("allUsers.json") as f:
	users = json.load(f)

@app.route('/users',methods=['GET'])
def get_users():
	return jsonify({'users':users})

@app.route('/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
	user = [user for user in users if user['id'] == user_id]
	if len(user)==0:
		abort(404)
	else:
		return jsonify({'user':user[0]})
if __name__ == "__main__":
	app.run(debug=True)