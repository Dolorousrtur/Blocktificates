from utils import hash_msg


def merkle_root(message, hashes):
    """
    message: certificate of a student
    hashes: consequent nodes of MHT
    """
    node_hash = hash_msg(message)
    for (hash, side) in hashes:
        if side == 'r':
            node_hash = hash_msg(node_hash + hash)
        else:
            node_hash = hash_msg(hash + node_hash)

    return node_hash

def check_position(root, position):
    return True