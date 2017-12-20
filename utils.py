import hashlib, json, sys

def hash_msg(msg=""):
    # For convenience, this is a helper function that wraps our hashing algorithm
    if type(msg)!=str:
        msg = json.dumps(msg,sort_keys=True)  # If we don't sort keys, we can't guarantee repeatability!
        
    if sys.version_info.major == 2:
        return hashlib.sha1(msg).hexdigest().encode()
    else:
        return hashlib.sha1(str(msg).encode('utf-8')).hexdigest()