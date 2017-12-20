from flask import Flask, request
from json import dumps

from push import push
from check import check
from revoke import revoke, check_revoked

app = Flask(__name__)

@app.route('/push_root', methods=['POST'])
def push_root():
	assert 'hash' in request.values.keys()
	hash_ = request.values['hash']
	txhash = push(hash_)

	return dumps({"txhash": txhash})

@app.route('/check_root', methods=['POST'])
def check_root():
	assert 'txhash' in request.values.keys()
	assert 'hash' in request.values.keys()
	hash_ , txhash = request.values['hash'], request.values['txhash']

	if check(txhash, hash_):
		return dumps({"valid": True})

	else:
		return dumps({"valid": False})



@app.route('/revoke', methods=['POST'])
def invalidate():
	assert 'certificate_id' in request.values.keys()
	certificate_id = request.values['certificate_id']

	if 'reason' in request.values.keys():
		reason = request.values['reason']

	else:
		reason = None

	revoke(certificate_id, reason)

	return "All good :D", 200

@app.route('/check_revoked', methods=['POST'])
def verify():
	assert 'certificate_id' in request.values.keys()
	certificate_id = request.values['certificate_id']

	result = check_revoked(certificate_id)
	return dumps({'revoked': result['revoked'], 'reason': result['reason']})

if __name__ == "__main__":
	app.run(debug=True)