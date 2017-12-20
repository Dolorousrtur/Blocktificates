from blockcypher import get_transaction_details

from secret import key

def check(txhash, hash):
	txdetails = get_transaction_details(txhash, coin_symbol='btc-testnet')
	outputs = txdetails['outputs']
	for output in outputs:
		try:
			if output['data_hex'] == hash:
				return True

		except KeyError:
			pass

	return False