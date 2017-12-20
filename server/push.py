from blockcypher import embed_data
from secret import key

def push(data):
    print("Pushing...")
    txhash = embed_data(to_embed=data,
             api_key=key,
             data_is_hex=True,
             coin_symbol='btc-testnet')['hash']

    return txhash