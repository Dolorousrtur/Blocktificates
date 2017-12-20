from signatures import generate_keys, sign, verify
from MHT import MerkTree
from utils import hash_msg
import json, requests

class Validator:
    def __init__(self, public_key, prefix):
        self.public_key = public_key
        self.prefix = prefix

    def validate(self, certificate, hashpath, transaction, signature):
        root = self._calculate_root(certificate, hashpath)
        if self._check_position(root, transaction) == True and self._check_signature(root, signature) == True and self._check_revoked() == True:
            return True
        else:
            return False

    def _calculate_root(self, certificate, hashpath):
        message = str(certificate)

        node_hash = hash_msg(message)
        for (hash, side) in hashpath:
            if side == 'r':
                node_hash = hash_msg(node_hash + hash)
            else:
                node_hash = hash_msg(hash + node_hash)

        return node_hash

    def _check_position(self, root, transaction):
        response = requests.post(self.base_url + "check_root",
                                 data={"hash": root,
                                       "txhash": transaction}).json()

        if response['valid']:
            return True

        return False



    def _check_signature(self, root, signature):
        return verify(root, signature, self.public_key)

    def _check_revoked(self, certificate):
        response = requests.post(self.base_url + "check_root",
                                 data={"certificate_id": certificate.id}).json()

        if response['revoked']:
            return True

        return False

class BatchIssuer:
    def __init__(self, certificates, prefix):
        self.prefix = prefix
        self.certificates = {prefix + str(c.id) : c for c in certificates}
        self.private_key, self.public_key = generate_keys()
        self.base_url = 'http://janky.satyarth.me:5000/'


        certificates_strings = [str(c) for c in certificates]
        self.mht = MerkTree(certificates_strings)
        self.mht.create_tree()

        self.mht_root = self.mht.Get_Root_leaf()

        self.signature = sign(self.mht_root, self.private_key)

        self.transaction = None


    def publish(self):
        response = requests.post(self.base_url + "push_root",
                                 data={"hash": self.mht_root}).json()
        self.transaction = response['txhash']

    def _get_tansaction(self):
        return self.transaction

    def distribute_data(self):
        data = dict()

        for key in self.certificates:
            certificate = self.certificates[key]
            data[certificate.id] = {"certificate" : str(certificate), \
                                    "position"    : self.transaction, \
                                    "hashpath"    : self.mht.get_hashpath(str(certificate)), \
                                    "signature"   : self.signature}
        return data

    def create_validator(self):
        return Validator(self.public_key, self.prefix)

    def revoke(self, student_id, reason=None):
        requests.post(self.base_url + "revoke", data={"certificate_id": self.prefix + student_id, "reason": reason})



from creator import Certificate

with open('certificates.json', 'r') as f:
    certificates = json.load(f)

c = Certificate.from_json(certificates[0])


certificates_instances = [Certificate.from_json(c) for c in certificates]
issuer = BatchIssuer(certificates_instances, 'SK2107')
issuer.publish()
data = issuer.distribute_data()