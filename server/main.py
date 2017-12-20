from flask import Flask, request
from json import dumps

from push import push

app = Flask(__name__)

@app.route('/push_root', methods=['POST'])
def push_root():
	assert request.method == 'POST'
	assert 'hash' in request.values.keys()
	hash = request.values['hash']
	txhash = push(hash)

	return dumps({"txhash": txhash})
	

if __name__ == "__main__":
	app.run(debug=True)