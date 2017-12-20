from flask import Flask, request
from json import dumps

from push import push
from check import check

app = Flask(__name__)

@app.route('/push_root', methods=['POST'])
def push_root():
	assert request.method == 'POST'
	assert 'hash' in request.values.keys()
	hash_ = request.values['hash']
	txhash = push(hash_)

	return dumps({"txhash": txhash})

@app.route('/check_root', methods=['POST'])
def check_root():
	assert request.method == 'POST'
	assert 'txhash' in request.values.keys()
	assert 'hash' in request.values.keys()
	hash_ , txhash = request.values['hash'], request.values['txhash']

	if check(txhash, hash_):
		return dumps({"valid": True})

	else:
		return dumps({"valid": False})



if __name__ == "__main__":
	app.run(debug=True)