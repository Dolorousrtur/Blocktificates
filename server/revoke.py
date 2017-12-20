from json import load, dump

def check_revoked(certificate_id):
	with open('revoked.json', 'r') as f:
		revoked_list = load(f)

	if certificate_id in revoked_list.keys():
		revoked = True
		reason = revoked_list[certificate_id]['reason']

	else:
		revoked = False
		reason = None

	return {'revoked': revoked,
			'reason': reason}



def revoke(certificate_id, reason=None):
	with open('revoked.json', 'r') as f:
		revoked_list = load(f)

	revoked_list[certificate_id]  = {'reason': reason}

	with open('revoked.json', 'w') as f:
		dump(revoked_list, f)