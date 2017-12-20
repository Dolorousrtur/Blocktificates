from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature


def generate_keys():
    private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
    public_key = private_key.public_key()

    return private_key, public_key

def sign(message, private_key):
    data = bytes(message.encode())
    signature = private_key.sign(data, ec.ECDSA(hashes.SHA256()))
    return signature

def verify(message, signature, public_key):
    data = bytes(message.encode())
    try:
        public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
    except InvalidSignature:
        return False

    return True



# message = 'some certificate'
#
# private_key, public_key = generate_keys()
#
# signature = sign(message, private_key)
#
# print(verify(message, signature, public_key))