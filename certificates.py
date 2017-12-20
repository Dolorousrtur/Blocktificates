from signatures import generate_keys, sign, verify
from MHT import MerkTree
from utils import hash_msg
import json

class Validator:
    def __init__(self, public_key, prefix):
        self.public_key = public_key
        self.prefix = prefix

    def validate(self, certificate, hashpath, transaction, signature):
        return True

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
        return True

    def _check_signature(self, root, signature):
        return verify(root, signature, self.public_key)

    def _check_revoked(self):
        return True

class BatchIssuer:
    def __init__(self, certificates, prefix):
        self.prefix = prefix
        self.certificates = {prefix + c.id : c for c in certificates}
        self.private_key, self.public_key = generate_keys()


        certificates_strings = [str(c) for c in certificates]
        self.mht = MerkTree(certificates_strings)
        self.mht.create_tree()

        self.mht_root = self.mht.Get_Root_leaf()

        self.signature = sign(self.mht_root, self.private_key)

        self.transaction = None


    def publish(self):
        pass

    def _get_tansaction(self):
        return self.transaction

    def distribute_data(self):
        return None

    def create_validator(self):
        return Validator(self.public_key, self.prefix)

    def revoke(self, student_id):
        pass

